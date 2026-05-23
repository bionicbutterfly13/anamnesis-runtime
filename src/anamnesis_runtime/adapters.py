"""Host-neutral adapter boundary contracts.

These contracts describe what a host integration may consume or produce without
pulling host systems or infrastructure clients into Anamnesis core.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Protocol

from anamnesis_runtime.models import MemoryEvent
from anamnesis_runtime.ports import (
    MemoryEventPublisher,
    MemoryEventSubscriber,
)


class AdapterContractError(RuntimeError):
    """Raised when a host adapter cannot satisfy a neutral boundary contract."""


class GraphMutationOperation(StrEnum):
    """Graph operation requested through a neutral persistence contract."""

    UPSERT_NODE = "upsert_node"
    UPSERT_EDGE = "upsert_edge"
    DELETE_NODE = "delete_node"
    DELETE_EDGE = "delete_edge"


class EvolutionAction(StrEnum):
    """Neutral action returned by a memory-process evolution adapter."""

    NOOP = "noop"
    ADAPT = "adapt"
    REVIEW = "review"
    ESCALATE = "escalate"


@dataclass(frozen=True, slots=True)
class GraphMutation:
    """Graph-shaped memory persistence request without graph-client types."""

    mutation_id: str
    operation: GraphMutationOperation
    subject_id: str
    subject_type: str
    properties: dict[str, Any] = field(default_factory=dict)
    links: tuple[dict[str, Any], ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.mutation_id:
            raise ValueError("mutation_id is required")
        if not self.subject_id:
            raise ValueError("subject_id is required")
        if not self.subject_type:
            raise ValueError("subject_type is required")


@dataclass(frozen=True, slots=True)
class ProjectionPayload:
    """Vector-projection payload without vector-store client types."""

    projection_id: str
    record_id: str
    text: str
    vector: tuple[float, ...] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.projection_id:
            raise ValueError("projection_id is required")
        if not self.record_id:
            raise ValueError("record_id is required")
        if not self.text:
            raise ValueError("text is required")


@dataclass(frozen=True, slots=True)
class RoutingRequest:
    """Host-neutral request for memory placement or recall routing."""

    request_id: str
    record_id: str
    memory_type: str
    context: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.request_id:
            raise ValueError("request_id is required")
        if not self.record_id:
            raise ValueError("record_id is required")
        if not self.memory_type:
            raise ValueError("memory_type is required")


@dataclass(frozen=True, slots=True)
class RoutingDecision:
    """Host-neutral routing outcome for memory placement or recall."""

    request_id: str
    route: str
    confidence: float
    reason: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.request_id:
            raise ValueError("request_id is required")
        if not self.route:
            raise ValueError("route is required")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")


@dataclass(frozen=True, slots=True)
class EvolutionRequest:
    """Host-neutral request to evaluate or adapt the memory process."""

    request_id: str
    record_id: str
    signal: str
    evidence: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.request_id:
            raise ValueError("request_id is required")
        if not self.record_id:
            raise ValueError("record_id is required")
        if not self.signal:
            raise ValueError("signal is required")


@dataclass(frozen=True, slots=True)
class EvolutionResult:
    """Host-neutral result from memory-process evaluation or adaptation."""

    request_id: str
    action: EvolutionAction
    rationale: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.request_id:
            raise ValueError("request_id is required")
        if not self.rationale:
            raise ValueError("rationale is required")


@dataclass(frozen=True, slots=True)
class EventEnvelope:
    """Transport-neutral event wrapper for host-owned bridges."""

    envelope_id: str
    event: MemoryEvent
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.envelope_id:
            raise ValueError("envelope_id is required")


class GraphMutationPort(Protocol):
    async def apply_mutation(self, mutation: GraphMutation) -> None: ...


class ProjectionPort(Protocol):
    async def project(self, payload: ProjectionPayload) -> None: ...


class RoutingPort(Protocol):
    async def route(self, request: RoutingRequest) -> RoutingDecision: ...


class EvolutionPort(Protocol):
    async def evolve(self, request: EvolutionRequest) -> EvolutionResult: ...


class EventBridgePort(MemoryEventPublisher, MemoryEventSubscriber, Protocol):
    """Combined event publisher/subscriber contract for host-owned bridges."""


__all__ = [
    "AdapterContractError",
    "EventBridgePort",
    "EventEnvelope",
    "EvolutionAction",
    "EvolutionPort",
    "EvolutionRequest",
    "EvolutionResult",
    "GraphMutation",
    "GraphMutationOperation",
    "GraphMutationPort",
    "ProjectionPayload",
    "ProjectionPort",
    "RoutingDecision",
    "RoutingPort",
    "RoutingRequest",
]
