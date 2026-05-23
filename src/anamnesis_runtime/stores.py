"""In-memory store implementations for offline runtime tests."""

from __future__ import annotations

from anamnesis_runtime.models import (
    ConsolidationDecision,
    ConsolidationOperation,
    NemoriEpisode,
    NemoriSemanticInsight,
    PriorMemory,
)


class InMemoryEpisodicStore:
    def __init__(self) -> None:
        self._episodes: dict[str, NemoriEpisode] = {}

    async def upsert_episode(self, episode: NemoriEpisode) -> None:
        self._episodes[episode.episode_id] = episode

    async def search_episodes(
        self, user_id: str, query: str, *, top_k: int
    ) -> tuple[NemoriEpisode, ...]:
        del query
        matches = [episode for episode in self._episodes.values() if episode.user_id == user_id]
        return tuple(matches[:top_k])


class InMemorySemanticStore:
    def __init__(self, insights: tuple[NemoriSemanticInsight, ...] = ()) -> None:
        self._insights: dict[str, NemoriSemanticInsight] = {
            insight.insight_id: insight for insight in insights
        }

    async def search_priors(
        self, user_id: str, query: str, *, top_k: int
    ) -> tuple[PriorMemory, ...]:
        del query
        priors = [
            PriorMemory(prior_id=insight.insight_id, content=insight.content, score=1.0)
            for insight in self._insights.values()
            if insight.user_id == user_id
        ]
        return tuple(priors[:top_k])

    async def apply_decision(self, decision: ConsolidationDecision) -> None:
        if decision.operation is ConsolidationOperation.NEW:
            self._insights[decision.insight.insight_id] = decision.insight
            return

        if decision.operation is ConsolidationOperation.MERGE and decision.target_ids:
            target_id = decision.target_ids[0]
            if target_id in self._insights:
                self._insights[target_id] = decision.insight
            return

        if decision.operation is ConsolidationOperation.CONFLICT:
            self._insights[decision.insight.insight_id] = decision.insight

    async def search_insights(
        self, user_id: str, query: str, *, top_k: int
    ) -> tuple[NemoriSemanticInsight, ...]:
        del query
        matches = [insight for insight in self._insights.values() if insight.user_id == user_id]
        return tuple(matches[:top_k])

