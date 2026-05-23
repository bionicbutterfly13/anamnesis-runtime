"""Runtime dependency protocols."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

from anamnesis_runtime.models import (
    ConsolidationDecision,
    NemoriEpisode,
    NemoriMessage,
    NemoriRawEpisode,
    NemoriRecallResult,
    NemoriSemanticInsight,
    Prediction,
    PriorMemory,
)


class MessageBuffer(Protocol):
    async def add(self, user_id: str, messages: Sequence[NemoriMessage]) -> None: ...

    async def pop(self, user_id: str) -> tuple[NemoriMessage, ...]: ...


class MessagePartitioner(Protocol):
    async def partition(
        self, messages: Sequence[NemoriMessage]
    ) -> tuple[NemoriRawEpisode, ...]: ...


class EpisodeGenerator(Protocol):
    async def generate(self, raw_episode: NemoriRawEpisode) -> NemoriEpisode: ...


class EpisodicStore(Protocol):
    async def upsert_episode(self, episode: NemoriEpisode) -> None: ...

    async def search_episodes(
        self, user_id: str, query: str, *, top_k: int
    ) -> tuple[NemoriEpisode, ...]: ...


class SemanticStore(Protocol):
    async def search_priors(
        self, user_id: str, query: str, *, top_k: int
    ) -> tuple[PriorMemory, ...]: ...

    async def apply_decision(self, decision: ConsolidationDecision) -> None: ...

    async def search_insights(
        self, user_id: str, query: str, *, top_k: int
    ) -> tuple[NemoriSemanticInsight, ...]: ...


class EpisodePredictor(Protocol):
    async def predict(
        self, episode: NemoriEpisode, priors: Sequence[PriorMemory]
    ) -> Prediction: ...


class PredictionErrorDistiller(Protocol):
    async def distill(
        self, raw_episode: NemoriRawEpisode, episode: NemoriEpisode, prediction: Prediction
    ) -> tuple[NemoriSemanticInsight, ...]: ...


class SemanticConsolidator(Protocol):
    async def consolidate(
        self, insights: Sequence[NemoriSemanticInsight]
    ) -> tuple[ConsolidationDecision, ...]: ...


class BasinPort(Protocol):
    async def route(self, decision: ConsolidationDecision) -> None: ...

    async def annotate_recall(self, result: NemoriRecallResult) -> NemoriRecallResult: ...
