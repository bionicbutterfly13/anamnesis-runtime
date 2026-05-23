from datetime import UTC, datetime

import pytest

from anamnesis_runtime import MemoryEvent
from anamnesis_runtime.events import (
    InMemoryEventTransport,
    event_type_matches,
    memory_event_from_dict,
    memory_event_to_dict,
)


def _event(event_type: str = "memory.message_ingested") -> MemoryEvent:
    return MemoryEvent(
        event_id="evt-1",
        event_type=event_type,
        schema_version=1,
        occurred_at=datetime(2026, 5, 23, 12, 0, tzinfo=UTC),
        source="test",
        payload={"message_id": "m1"},
        correlation_id="corr-1",
        causation_id="evt-0",
        metadata={"strategy": "nemori"},
    )


def test_memory_event_validates_required_transport_neutral_fields() -> None:
    with pytest.raises(ValueError, match="event_id"):
        MemoryEvent(
            event_id="",
            event_type="memory.message_ingested",
            schema_version=1,
            occurred_at=datetime(2026, 5, 23, tzinfo=UTC),
            source="test",
            payload={},
        )

    with pytest.raises(ValueError, match="schema_version"):
        MemoryEvent(
            event_id="evt-1",
            event_type="memory.message_ingested",
            schema_version=0,
            occurred_at=datetime(2026, 5, 23, tzinfo=UTC),
            source="test",
            payload={},
        )

    with pytest.raises(ValueError, match="timezone-aware"):
        MemoryEvent(
            event_id="evt-1",
            event_type="memory.message_ingested",
            schema_version=1,
            occurred_at=datetime(2026, 5, 23),
            source="test",
            payload={},
        )


def test_memory_event_serializes_to_transport_neutral_shape() -> None:
    event = _event()

    serialized = memory_event_to_dict(event)
    restored = memory_event_from_dict(serialized)

    assert serialized == {
        "event_id": "evt-1",
        "event_type": "memory.message_ingested",
        "schema_version": 1,
        "occurred_at": "2026-05-23T12:00:00+00:00",
        "source": "test",
        "correlation_id": "corr-1",
        "causation_id": "evt-0",
        "payload": {"message_id": "m1"},
        "metadata": {"strategy": "nemori"},
    }
    assert restored == event


def test_event_type_pattern_matching_supports_exact_and_namespace_wildcards() -> None:
    assert event_type_matches("memory.message_ingested", "memory.message_ingested")
    assert event_type_matches("memory.*", "memory.message_ingested")
    assert not event_type_matches("memory.recall_*", "memory.message_ingested")


def test_in_memory_event_transport_publishes_and_replays_matching_events() -> None:
    async def handler(event: MemoryEvent) -> None:
        received.append(event)

    async def scenario() -> None:
        await transport.subscribe("memory.*", handler)
        await transport.publish(_event())
        await transport.publish(_event("system.unrelated"))

    received: list[MemoryEvent] = []
    transport = InMemoryEventTransport()

    import asyncio

    asyncio.run(scenario())

    assert received == [_event()]
    assert transport.replay("memory.*") == (_event(),)

