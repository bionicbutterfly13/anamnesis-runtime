"""Nemori strategy orchestration."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from anamnesis_runtime.buffer import InMemoryMessageBuffer
from anamnesis_runtime.models import (
    NemoriEpisode,
    NemoriMessage,
    NemoriRawEpisode,
    NemoriRecallResult,
    SourceKind,
)
from anamnesis_runtime.ports import (
    EpisodeGenerator,
    EpisodePredictor,
    EpisodicStore,
    MessageBuffer,
    MessagePartitioner,
    PredictionErrorDistiller,
    SemanticConsolidator,
    SemanticStore,
)
from anamnesis_runtime.runtime import MemoryRuntime
from anamnesis_runtime.stores import InMemoryEpisodicStore, InMemorySemanticStore
from anamnesis_runtime.strategies.nemori.consolidation import NemoriSemanticConsolidator
from anamnesis_runtime.strategies.nemori.predict_calibrate import (
    PriorAwarePredictor,
    RawEpisodePredictionErrorDistiller,
)


def _message_text(message: NemoriMessage) -> str:
    if isinstance(message.content, str):
        return message.content
    return " ".join(part.text or "" for part in message.content).strip()


def _chunked(messages: Sequence[NemoriMessage], size: int) -> tuple[tuple[NemoriMessage, ...], ...]:
    return tuple(tuple(messages[index : index + size]) for index in range(0, len(messages), size))


class MessageCountSegmenter:
    """Deterministic segmenter for offline Nemori tests.

    This is not the paper's LLM segmenter. It is the host-neutral baseline that
    proves the strategy contract can run without external services.
    """

    def __init__(self, *, max_messages: int | None = None, boundary_reason: str = "message_count"):
        if max_messages is not None and max_messages < 1:
            raise ValueError("max_messages must be positive")
        self._max_messages = max_messages
        self._boundary_reason = boundary_reason

    async def partition(self, messages: Sequence[NemoriMessage]) -> tuple[NemoriRawEpisode, ...]:
        if not messages:
            return ()

        chunks = _chunked(messages, self._max_messages or len(messages))
        return tuple(self._raw_episode(chunk) for chunk in chunks)

    def _raw_episode(self, messages: tuple[NemoriMessage, ...]) -> NemoriRawEpisode:
        first = messages[0]
        last = messages[-1]
        return NemoriRawEpisode(
            raw_episode_id=f"raw:{first.message_id}:{last.message_id}",
            user_id=first.user_id,
            agent_id=first.agent_id,
            messages=messages,
            topic=self._topic(messages),
            boundary_reason=self._boundary_reason,
            source_kind=SourceKind.CONVERSATION,
            metadata={"message_count": len(messages)},
        )

    def _topic(self, messages: Sequence[NemoriMessage]) -> str:
        text = _message_text(messages[0])
        return text[:80] if text else "untitled episode"


class NarrativeEpisodeGenerator:
    """Generate a provenance-preserving narrative episode from raw messages."""

    async def generate(self, raw_episode: NemoriRawEpisode) -> NemoriEpisode:
        narrative = "\n".join(
            f"{message.role.value}: {_message_text(message)}" for message in raw_episode.messages
        )
        source_messages = tuple(self._source_message(message) for message in raw_episode.messages)
        return NemoriEpisode(
            episode_id=f"episode:{raw_episode.raw_episode_id}",
            user_id=raw_episode.user_id,
            agent_id=raw_episode.agent_id,
            cue=raw_episode.topic,
            narrative=narrative,
            raw_episode_id=raw_episode.raw_episode_id,
            source_messages=source_messages,
            timestamp=raw_episode.timestamp,
            provenance={
                "boundary_reason": raw_episode.boundary_reason,
                "source_kind": raw_episode.source_kind.value,
            },
        )

    def _source_message(self, message: NemoriMessage) -> dict[str, Any]:
        return {
            "message_id": message.message_id,
            "role": message.role.value,
            "timestamp": message.timestamp.isoformat(),
        }


class NemoriStrategy:
    """First concrete memory strategy inside Anamnesis."""

    def __init__(
        self,
        *,
        buffer: MessageBuffer | None = None,
        segmenter: MessagePartitioner | None = None,
        episode_generator: EpisodeGenerator | None = None,
        episodic_store: EpisodicStore | None = None,
        semantic_store: SemanticStore | None = None,
        predictor: EpisodePredictor | None = None,
        distiller: PredictionErrorDistiller | None = None,
        consolidator: SemanticConsolidator | None = None,
        semantic_top_k: int = 20,
    ) -> None:
        self._active_users: set[str] = set()
        self._runtime = MemoryRuntime(
            buffer=buffer or InMemoryMessageBuffer(),
            partitioner=segmenter or MessageCountSegmenter(),
            episode_generator=episode_generator or NarrativeEpisodeGenerator(),
            episodic_store=episodic_store or InMemoryEpisodicStore(),
            semantic_store=semantic_store or InMemorySemanticStore(),
            predictor=predictor or PriorAwarePredictor(),
            distiller=distiller or RawEpisodePredictionErrorDistiller(),
            consolidator=consolidator or NemoriSemanticConsolidator(),
            semantic_top_k=semantic_top_k,
        )

    async def ingest(self, messages: Sequence[NemoriMessage]) -> None:
        if not messages:
            return
        user_ids = {message.user_id for message in messages}
        if len(user_ids) != 1:
            raise ValueError("NemoriStrategy.ingest requires messages for exactly one user")
        user_id = next(iter(user_ids))
        self._active_users.add(user_id)
        await self._runtime.add_messages(user_id, messages)

    async def flush(self, user_id: str | None = None) -> tuple[NemoriEpisode, ...]:
        resolved_user_id = self._resolve_user_id(user_id)
        episodes = await self._runtime.flush(resolved_user_id)
        self._active_users.discard(resolved_user_id)
        return episodes

    async def recall(self, user_id: str, query: str, *, top_k: int = 10) -> NemoriRecallResult:
        return await self._runtime.search(user_id, query, top_k=top_k)

    def _resolve_user_id(self, user_id: str | None) -> str:
        if user_id is not None:
            return user_id
        if len(self._active_users) == 1:
            return next(iter(self._active_users))
        raise ValueError("user_id is required when zero or multiple users have buffered messages")

