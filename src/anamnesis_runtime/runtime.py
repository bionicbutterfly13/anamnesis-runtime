"""Host-neutral memory runtime orchestration."""

from __future__ import annotations

from collections.abc import Sequence

from anamnesis_runtime.buffer import InMemoryMessageBuffer
from anamnesis_runtime.models import (
    ConsolidationDecision,
    ConsolidationOperation,
    NemoriEpisode,
    NemoriMessage,
    NemoriRecallResult,
    NemoriSemanticInsight,
)
from anamnesis_runtime.ports import (
    BasinPort,
    EpisodeGenerator,
    EpisodePredictor,
    EpisodicStore,
    MessageBuffer,
    MessagePartitioner,
    PredictionErrorDistiller,
    SemanticConsolidator,
    SemanticStore,
)
from anamnesis_runtime.stores import InMemoryEpisodicStore, InMemorySemanticStore


class NewOnlyConsolidator:
    """Default consolidator for offline tests."""

    async def consolidate(
        self, insights: Sequence[NemoriSemanticInsight]
    ) -> tuple[ConsolidationDecision, ...]:
        return tuple(
            ConsolidationDecision(
                operation=ConsolidationOperation.NEW,
                insight=insight,
                reason="default-new",
            )
            for insight in insights
        )


class NoopBasinPort:
    """Host-neutral basin placeholder."""

    async def route(self, decision: ConsolidationDecision) -> None:
        del decision

    async def annotate_recall(self, result: NemoriRecallResult) -> NemoriRecallResult:
        return result


class MemoryRuntime:
    """Episodic-semantic memory formation and recall kernel."""

    def __init__(
        self,
        *,
        partitioner: MessagePartitioner,
        episode_generator: EpisodeGenerator,
        predictor: EpisodePredictor,
        distiller: PredictionErrorDistiller,
        buffer: MessageBuffer | None = None,
        episodic_store: EpisodicStore | None = None,
        semantic_store: SemanticStore | None = None,
        consolidator: SemanticConsolidator | None = None,
        basin_port: BasinPort | None = None,
        semantic_top_k: int = 20,
    ) -> None:
        self._buffer = buffer or InMemoryMessageBuffer()
        self._partitioner = partitioner
        self._episode_generator = episode_generator
        self._episodic_store = episodic_store or InMemoryEpisodicStore()
        self._semantic_store = semantic_store or InMemorySemanticStore()
        self._predictor = predictor
        self._distiller = distiller
        self._consolidator = consolidator or NewOnlyConsolidator()
        self._basin_port = basin_port or NoopBasinPort()
        self._semantic_top_k = semantic_top_k

    async def add_messages(self, user_id: str, messages: Sequence[NemoriMessage]) -> None:
        await self._buffer.add(user_id, messages)

    async def flush(self, user_id: str) -> tuple[NemoriEpisode, ...]:
        messages = await self._buffer.pop(user_id)
        if not messages:
            return ()

        raw_episodes = await self._partitioner.partition(messages)
        episodes = []

        for raw_episode in raw_episodes:
            episode = await self._episode_generator.generate(raw_episode)
            await self._episodic_store.upsert_episode(episode)

            priors = await self._semantic_store.search_priors(
                user_id=episode.user_id,
                query=episode.cue,
                top_k=self._semantic_top_k,
            )
            prediction = await self._predictor.predict(episode, priors)
            insights = await self._distiller.distill(raw_episode, episode, prediction)
            decisions = await self._consolidator.consolidate(insights)

            for decision in decisions:
                await self._semantic_store.apply_decision(decision)
                await self._basin_port.route(decision)

            episodes.append(episode)

        return tuple(episodes)

    async def search(self, user_id: str, query: str, *, top_k: int = 10) -> NemoriRecallResult:
        episodes = await self._episodic_store.search_episodes(user_id, query, top_k=top_k)
        insights = await self._semantic_store.search_insights(user_id, query, top_k=top_k)
        result = NemoriRecallResult(episodes=episodes, semantic_insights=insights)
        return await self._basin_port.annotate_recall(result)

    async def health(self) -> dict[str, str]:
        return {"status": "ok"}

    async def stats(self) -> dict[str, int]:
        return {"semantic_top_k": self._semantic_top_k}
