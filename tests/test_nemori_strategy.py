import asyncio
from collections.abc import Sequence
from datetime import UTC, datetime

from anamnesis_runtime import (
    InMemorySemanticStore,
    NemoriEpisode,
    NemoriMessage,
    NemoriSemanticInsight,
    Prediction,
    PriorMemory,
    Role,
)
from anamnesis_runtime.strategies.nemori import (
    MessageCountSegmenter,
    NarrativeEpisodeGenerator,
    NemoriStrategy,
    RawEpisodePredictionErrorDistiller,
)


def _message(message_id: str, content: str, *, minute: int = 0) -> NemoriMessage:
    return NemoriMessage(
        message_id=message_id,
        user_id="u1",
        agent_id="a1",
        role=Role.USER,
        content=content,
        timestamp=datetime(2026, 5, 23, 12, minute, tzinfo=UTC),
    )


def test_nemori_strategy_buffers_and_segments_messages() -> None:
    async def scenario() -> None:
        strategy = NemoriStrategy(segmenter=MessageCountSegmenter(max_messages=2))
        messages = (
            _message("m1", "First observation."),
            _message("m2", "Second observation.", minute=1),
            _message("m3", "Third observation.", minute=2),
        )

        await strategy.ingest(messages)
        episodes = await strategy.flush("u1")

        assert len(episodes) == 2
        assert episodes[0].raw_episode_id == "raw:m1:m2"
        assert episodes[1].raw_episode_id == "raw:m3:m3"
        recall = await strategy.recall("u1", "observation")
        assert [episode.episode_id for episode in recall.episodes] == [
            "episode:raw:m1:m2",
            "episode:raw:m3:m3",
        ]

    asyncio.run(scenario())


def test_nemori_strategy_retrieves_semantic_priors_before_prediction() -> None:
    class RecordingPredictor:
        def __init__(self) -> None:
            self.seen_priors: tuple[PriorMemory, ...] = ()

        async def predict(
            self, episode: NemoriEpisode, priors: Sequence[PriorMemory]
        ) -> Prediction:
            self.seen_priors = tuple(priors)
            return Prediction(
                content=f"predicted from {len(priors)} prior(s) for {episode.cue}",
                priors=tuple(priors),
            )

    async def scenario() -> None:
        prior = NemoriSemanticInsight(
            insight_id="prior-1",
            user_id="u1",
            agent_id="a1",
            content="Dr. Mani prefers host-neutral package boundaries.",
            source_episode_id="old-episode",
            prediction="",
            prediction_error_summary="",
            confidence=0.9,
        )
        predictor = RecordingPredictor()
        strategy = NemoriStrategy(
            semantic_store=InMemorySemanticStore((prior,)),
            predictor=predictor,
        )

        await strategy.ingest((_message("m1", "Move memory logic out of Dionysus."),))
        await strategy.flush("u1")

        assert predictor.seen_priors
        assert predictor.seen_priors[0].content == prior.content

    asyncio.run(scenario())


def test_nemori_strategy_calibrates_against_raw_episode_not_cleaned_narrative() -> None:
    class SmoothedEpisodeGenerator(NarrativeEpisodeGenerator):
        async def generate(self, raw_episode):
            episode = await super().generate(raw_episode)
            return NemoriEpisode(
                episode_id=episode.episode_id,
                user_id=episode.user_id,
                agent_id=episode.agent_id,
                cue="food preference",
                narrative="A food preference was discussed.",
                raw_episode_id=episode.raw_episode_id,
                source_messages=episode.source_messages,
                timestamp=episode.timestamp,
                embedding=episode.embedding,
                basin_metadata=episode.basin_metadata,
                provenance=episode.provenance,
            )

    async def scenario() -> None:
        strategy = NemoriStrategy(
            episode_generator=SmoothedEpisodeGenerator(),
            distiller=RawEpisodePredictionErrorDistiller(),
        )

        await strategy.ingest((_message("m1", "The user has a pineapple allergy."),))
        await strategy.flush("u1")
        recall = await strategy.recall("u1", "pineapple")

        assert recall.semantic_insights
        insight = recall.semantic_insights[0]
        assert "pineapple allergy" in insight.content
        assert "pineapple allergy" not in recall.episodes[0].narrative

    asyncio.run(scenario())

