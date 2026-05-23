import asyncio
from collections.abc import Sequence
from datetime import UTC, datetime

from anamnesis_runtime import (
    InMemoryEpisodicStore,
    InMemorySemanticStore,
    MemoryRuntime,
    NemoriEpisode,
    NemoriMessage,
    NemoriRawEpisode,
    NemoriSemanticInsight,
    Prediction,
    PriorMemory,
    Role,
)


class OneEpisodePartitioner:
    async def partition(self, messages: Sequence[NemoriMessage]) -> tuple[NemoriRawEpisode, ...]:
        first = messages[0]
        return (
            NemoriRawEpisode(
                raw_episode_id="raw-1",
                user_id=first.user_id,
                agent_id=first.agent_id,
                messages=tuple(messages),
                topic="runtime extraction",
                boundary_reason="test fixture",
            ),
        )


class SimpleEpisodeGenerator:
    async def generate(self, raw_episode: NemoriRawEpisode) -> NemoriEpisode:
        return NemoriEpisode(
            episode_id="ep-1",
            user_id=raw_episode.user_id,
            agent_id=raw_episode.agent_id,
            cue=raw_episode.topic,
            narrative="Dr. Mani chooses to extract memory into a host-neutral runtime.",
            raw_episode_id=raw_episode.raw_episode_id,
            source_messages=({"message_id": raw_episode.messages[0].message_id},),
            timestamp=raw_episode.timestamp,
        )


class RecordingPredictor:
    def __init__(self) -> None:
        self.seen_priors: tuple[PriorMemory, ...] = ()

    async def predict(self, episode: NemoriEpisode, priors: Sequence[PriorMemory]) -> Prediction:
        self.seen_priors = tuple(priors)
        prior_text = " | ".join(prior.content for prior in priors)
        return Prediction(
            content=f"prediction for {episode.cue}: {prior_text}",
            priors=tuple(priors),
        )


class SimpleDistiller:
    async def distill(
        self, raw_episode: NemoriRawEpisode, episode: NemoriEpisode, prediction: Prediction
    ) -> tuple[NemoriSemanticInsight, ...]:
        return (
            NemoriSemanticInsight(
                insight_id="insight-1",
                user_id=raw_episode.user_id,
                agent_id=raw_episode.agent_id,
                content="Memory formation should live outside Dionysus host policy.",
                source_episode_id=episode.episode_id,
                prediction=prediction.content,
                prediction_error_summary="The raw episode adds a package boundary decision.",
                confidence=0.95,
            ),
        )


def test_flush_predicts_against_retrieved_semantic_priors() -> None:
    async def scenario() -> None:
        seed_prior = NemoriSemanticInsight(
            insight_id="seed-1",
            user_id="u1",
            agent_id="a1",
            content="Extracted packages must stay independently consumable.",
            source_episode_id="old-episode",
            prediction="",
            prediction_error_summary="",
            confidence=0.9,
        )
        semantic_store = InMemorySemanticStore((seed_prior,))
        predictor = RecordingPredictor()
        runtime = MemoryRuntime(
            partitioner=OneEpisodePartitioner(),
            episode_generator=SimpleEpisodeGenerator(),
            predictor=predictor,
            distiller=SimpleDistiller(),
            episodic_store=InMemoryEpisodicStore(),
            semantic_store=semantic_store,
        )
        message = NemoriMessage(
            message_id="m1",
            user_id="u1",
            agent_id="a1",
            role=Role.USER,
            content="Move memory out of Dionysus.",
            timestamp=datetime(2026, 5, 22, tzinfo=UTC),
        )

        await runtime.add_messages("u1", [message])
        episodes = await runtime.flush("u1")
        recall = await runtime.search("u1", "memory runtime")

        assert len(episodes) == 1
        assert predictor.seen_priors
        assert predictor.seen_priors[0].content == seed_prior.content
        assert any("outside Dionysus" in insight.content for insight in recall.semantic_insights)

    asyncio.run(scenario())
