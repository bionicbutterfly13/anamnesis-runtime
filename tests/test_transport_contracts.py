import asyncio
from collections import defaultdict
from datetime import UTC, datetime

from anamnesis_runtime import MemoryEvent, MemoryEventPublisher, MemoryEventSubscriber
from anamnesis_runtime.events import (
    event_type_matches,
    memory_event_from_dict,
    memory_event_to_dict,
)


def _event(event_type: str = "memory.episode_created") -> MemoryEvent:
    return MemoryEvent(
        event_id=f"evt:{event_type}",
        event_type=event_type,
        schema_version=1,
        occurred_at=datetime(2026, 5, 23, 12, 30, tzinfo=UTC),
        source="contract-test",
        payload={"episode_id": "ep-1"},
    )


async def _assert_publisher_subscriber_contract(
    publisher: MemoryEventPublisher, subscriber: MemoryEventSubscriber
) -> None:
    received: list[MemoryEvent] = []

    async def handler(event: MemoryEvent) -> None:
        received.append(event)

    await subscriber.subscribe("memory.*", handler)
    await publisher.publish(_event())
    await publisher.publish(_event("system.health"))

    assert received == [_event()]


class FakeRedisStreamsAdapter:
    def __init__(self) -> None:
        self._stream: list[dict] = []
        self._handlers: list[tuple[str, object]] = []

    async def publish(self, event: MemoryEvent) -> None:
        encoded = memory_event_to_dict(event)
        self._stream.append(encoded)
        for pattern, handler in self._handlers:
            decoded = memory_event_from_dict(encoded)
            if event_type_matches(pattern, decoded.event_type):
                result = handler(decoded)
                if hasattr(result, "__await__"):
                    await result

    async def subscribe(self, event_type: str, handler: object) -> None:
        self._handlers.append((event_type, handler))

    def replay(self, event_type: str) -> tuple[MemoryEvent, ...]:
        return tuple(
            event
            for item in self._stream
            if event_type_matches(event_type, (event := memory_event_from_dict(item)).event_type)
        )


class FakeRabbitMQAdapter:
    def __init__(self) -> None:
        self._queues: dict[str, list[dict]] = defaultdict(list)
        self._bindings: list[tuple[str, str, object]] = []
        self.acked: list[str] = []

    async def publish(self, event: MemoryEvent) -> None:
        encoded = memory_event_to_dict(event)
        for queue, pattern, handler in self._bindings:
            if event_type_matches(pattern, event.event_type):
                self._queues[queue].append(encoded)
                decoded = memory_event_from_dict(encoded)
                result = handler(decoded)
                if hasattr(result, "__await__"):
                    await result
                self.acked.append(decoded.event_id)

    async def subscribe(self, event_type: str, handler: object) -> None:
        self._bindings.append(("anamnesis-memory", event_type, handler))


def test_fake_in_process_adapter_conforms_to_transport_ports() -> None:
    from anamnesis_runtime.events import InMemoryEventTransport

    adapter = InMemoryEventTransport()
    asyncio.run(_assert_publisher_subscriber_contract(adapter, adapter))


def test_fake_redis_streams_adapter_conforms_to_transport_ports() -> None:
    adapter = FakeRedisStreamsAdapter()
    asyncio.run(_assert_publisher_subscriber_contract(adapter, adapter))

    assert adapter.replay("memory.*") == (_event(),)


def test_fake_rabbitmq_adapter_conforms_to_transport_ports() -> None:
    adapter = FakeRabbitMQAdapter()
    asyncio.run(_assert_publisher_subscriber_contract(adapter, adapter))

    assert adapter.acked == [_event().event_id]

