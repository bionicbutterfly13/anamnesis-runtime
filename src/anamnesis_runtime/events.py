"""Transport-neutral memory event helpers."""

from __future__ import annotations

import inspect
from collections.abc import Mapping
from datetime import datetime
from typing import Any

from anamnesis_runtime.models import MemoryEvent
from anamnesis_runtime.ports import MemoryEventHandler


def memory_event_to_dict(event: MemoryEvent) -> dict[str, Any]:
    """Serialize a memory event without transport-specific envelope fields."""

    return {
        "event_id": event.event_id,
        "event_type": event.event_type,
        "schema_version": event.schema_version,
        "occurred_at": event.occurred_at.isoformat(),
        "source": event.source,
        "correlation_id": event.correlation_id,
        "causation_id": event.causation_id,
        "payload": dict(event.payload),
        "metadata": dict(event.metadata),
    }


def memory_event_from_dict(data: Mapping[str, Any]) -> MemoryEvent:
    """Deserialize a memory event from a transport-neutral mapping."""

    occurred_at = data["occurred_at"]
    if isinstance(occurred_at, str):
        occurred_at = datetime.fromisoformat(occurred_at)

    return MemoryEvent(
        event_id=str(data["event_id"]),
        event_type=str(data["event_type"]),
        schema_version=int(data["schema_version"]),
        occurred_at=occurred_at,
        source=str(data["source"]),
        correlation_id=_optional_str(data.get("correlation_id")),
        causation_id=_optional_str(data.get("causation_id")),
        payload=dict(data["payload"]),
        metadata=dict(data.get("metadata", {})),
    )


def event_type_matches(pattern: str, event_type: str) -> bool:
    """Match exact event types and namespace wildcards such as ``memory.*``."""

    if pattern == "*":
        return True
    if pattern.endswith(".*"):
        return event_type.startswith(pattern[:-1])
    return pattern == event_type


class InMemoryEventTransport:
    """In-process publisher/subscriber for tests and local experiments."""

    def __init__(self) -> None:
        self._events: list[MemoryEvent] = []
        self._subscriptions: list[tuple[str, MemoryEventHandler]] = []

    async def publish(self, event: MemoryEvent) -> None:
        self._events.append(event)
        for pattern, handler in self._subscriptions:
            if event_type_matches(pattern, event.event_type):
                result = handler(event)
                if inspect.isawaitable(result):
                    await result

    async def subscribe(self, event_type: str, handler: MemoryEventHandler) -> None:
        self._subscriptions.append((event_type, handler))

    def replay(self, event_type: str = "*") -> tuple[MemoryEvent, ...]:
        return tuple(
            event for event in self._events if event_type_matches(event_type, event.event_type)
        )


def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)

