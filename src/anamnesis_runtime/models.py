"""Core host-neutral memory records."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


class Role(StrEnum):
    """Message roles accepted by the memory runtime."""

    SYSTEM = "system"
    DEVELOPER = "developer"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class SourceKind(StrEnum):
    """Source families that can produce raw episodes."""

    CONVERSATION = "conversation"
    DEVELOPMENT_EVENT = "development_event"
    DOCUMENT = "document"
    PROJECTION = "projection"


class MemoryType(StrEnum):
    """Semantic insight category."""

    SEMANTIC = "semantic"
    PROCEDURAL = "procedural"
    STRATEGIC = "strategic"
    EPISODIC = "episodic"


class ConsolidationOperation(StrEnum):
    """Operations a consolidator may request."""

    NEW = "new"
    MERGE = "merge"
    CONFLICT = "conflict"


class GateDecisionAction(StrEnum):
    """Possible outcomes from a host-neutral memory gate."""

    ALLOW = "allow"
    BLOCK = "block"
    QUARANTINE = "quarantine"
    REVIEW = "review"


@dataclass(frozen=True, slots=True)
class ContentPart:
    """Typed multimodal content placeholder.

    The runtime only stores these parts. Host packages decide whether and how to
    process non-text content.
    """

    kind: str
    text: str | None = None
    data: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class NemoriMessage:
    """Upstream-compatible message unit with explicit host provenance."""

    message_id: str
    user_id: str
    agent_id: str
    role: Role
    content: str | tuple[ContentPart, ...]
    timestamp: datetime
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.message_id:
            raise ValueError("message_id is required")
        if self.timestamp.tzinfo is None:
            raise ValueError("timestamp must be timezone-aware")


@dataclass(frozen=True, slots=True)
class BasinContext:
    """Optional routing metadata supplied by a host basin system."""

    basin_id: str | None = None
    basin_name: str | None = None
    memory_type: str | None = None
    resonance_score: float | None = None
    activation_strength: float | None = None
    source: str = "none"
    label_status: str = "canonical"


@dataclass(frozen=True, slots=True)
class NemoriRawEpisode:
    """Partitioned raw episode before narrative or semantic distillation."""

    raw_episode_id: str
    user_id: str
    agent_id: str
    messages: tuple[NemoriMessage, ...]
    topic: str
    boundary_reason: str
    source_kind: SourceKind = SourceKind.CONVERSATION
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def timestamp(self) -> datetime:
        if self.messages:
            return self.messages[0].timestamp
        return datetime.now(UTC)


@dataclass(frozen=True, slots=True)
class NemoriEpisode:
    """Narrative/provenance memory plane."""

    episode_id: str
    user_id: str
    agent_id: str
    cue: str
    narrative: str
    raw_episode_id: str
    source_messages: tuple[dict[str, Any], ...]
    timestamp: datetime
    embedding: tuple[float, ...] | None = None
    basin_metadata: BasinContext | None = None
    provenance: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class PriorMemory:
    """Semantic prior returned by a semantic store."""

    prior_id: str
    content: str
    score: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Prediction:
    """Prediction made from an episode cue plus retrieved semantic priors."""

    content: str
    priors: tuple[PriorMemory, ...]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class NemoriSemanticInsight:
    """Semantic prediction-error delta extracted from a raw episode."""

    insight_id: str
    user_id: str
    agent_id: str
    content: str
    source_episode_id: str
    prediction: str
    prediction_error_summary: str
    confidence: float
    embedding: tuple[float, ...] | None = None
    memory_type: MemoryType = MemoryType.SEMANTIC
    basin_metadata: BasinContext | None = None

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")


@dataclass(frozen=True, slots=True)
class ConsolidationDecision:
    """Nemori-owned semantic consolidation decision."""

    operation: ConsolidationOperation
    insight: NemoriSemanticInsight
    target_ids: tuple[str, ...] = ()
    consolidated_content: str | None = None
    reason: str = ""


@dataclass(frozen=True, slots=True)
class NemoriRecallResult:
    """Unified recall response."""

    episodes: tuple[NemoriEpisode, ...] = ()
    raw_episodes: tuple[NemoriRawEpisode, ...] = ()
    semantic_insights: tuple[NemoriSemanticInsight, ...] = ()
    ranking_metadata: dict[str, Any] = field(default_factory=dict)
    basin_metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class MemoryEvent:
    """Transport-neutral event emitted by the memory runtime."""

    event_id: str
    event_type: str
    schema_version: int
    occurred_at: datetime
    source: str
    payload: dict[str, Any]
    correlation_id: str | None = None
    causation_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.event_id:
            raise ValueError("event_id is required")
        if not self.event_type:
            raise ValueError("event_type is required")
        if self.schema_version < 1:
            raise ValueError("schema_version must be positive")
        if self.occurred_at.tzinfo is None:
            raise ValueError("occurred_at must be timezone-aware")
        if not self.source:
            raise ValueError("source is required")


@dataclass(frozen=True, slots=True)
class GateRequest:
    """Host-neutral request for memory write or recall review."""

    request_id: str
    subject: str
    payload: dict[str, Any]
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.request_id:
            raise ValueError("request_id is required")
        if not self.subject:
            raise ValueError("subject is required")
        if self.occurred_at.tzinfo is None:
            raise ValueError("occurred_at must be timezone-aware")


@dataclass(frozen=True, slots=True)
class GateDecision:
    """Host-neutral gate decision returned before memory is accepted or routed."""

    action: GateDecisionAction
    request_id: str
    reason: str
    decided_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.request_id:
            raise ValueError("request_id is required")
        if self.decided_at.tzinfo is None:
            raise ValueError("decided_at must be timezone-aware")


@dataclass(frozen=True, slots=True)
class TelemetryRecord:
    """Host-neutral runtime diagnostic record."""

    name: str
    value: int | float | str | bool
    occurred_at: datetime
    attributes: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("name is required")
        if self.occurred_at.tzinfo is None:
            raise ValueError("occurred_at must be timezone-aware")
