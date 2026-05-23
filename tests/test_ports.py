import asyncio
from datetime import UTC, datetime

from anamnesis_runtime import (
    GateDecision,
    GateDecisionAction,
    GatePort,
    GateRequest,
    MemoryEvent,
    MemoryEventPublisher,
    MemoryEventSubscriber,
    TelemetryPort,
    TelemetryRecord,
)


def test_memory_event_contract_is_transport_neutral() -> None:
    event = MemoryEvent(
        event_id="evt-1",
        event_type="memory.consolidation_decided",
        schema_version=1,
        occurred_at=datetime(2026, 5, 23, tzinfo=UTC),
        source="anamnesis-runtime",
        payload={"decision_id": "dec-1"},
        correlation_id="corr-1",
        causation_id="evt-0",
        metadata={"adapter": "none"},
    )

    assert event.event_type == "memory.consolidation_decided"
    assert event.payload["decision_id"] == "dec-1"
    assert event.metadata["adapter"] == "none"


def test_event_publisher_and_subscriber_protocols_accept_memory_events() -> None:
    class RecordingPublisher:
        def __init__(self) -> None:
            self.events: list[MemoryEvent] = []

        async def publish(self, event: MemoryEvent) -> None:
            self.events.append(event)

    class RecordingSubscriber:
        def __init__(self) -> None:
            self.registrations: list[tuple[str, object]] = []

        async def subscribe(self, event_type: str, handler: object) -> None:
            self.registrations.append((event_type, handler))

    async def scenario() -> None:
        publisher: MemoryEventPublisher = RecordingPublisher()
        subscriber: MemoryEventSubscriber = RecordingSubscriber()
        event = MemoryEvent(
            event_id="evt-1",
            event_type="memory.message_ingested",
            schema_version=1,
            occurred_at=datetime(2026, 5, 23, tzinfo=UTC),
            source="test",
            payload={},
        )

        await publisher.publish(event)
        await subscriber.subscribe("memory.*", lambda received: received)

        assert isinstance(publisher, RecordingPublisher)
        assert publisher.events == [event]
        assert isinstance(subscriber, RecordingSubscriber)
        assert subscriber.registrations[0][0] == "memory.*"

    asyncio.run(scenario())


def test_gate_port_returns_explicit_decision() -> None:
    class AllowAllGate:
        async def review(self, request: GateRequest) -> GateDecision:
            return GateDecision(
                action=GateDecisionAction.ALLOW,
                request_id=request.request_id,
                reason="test gate allows neutral memory write",
            )

    async def scenario() -> None:
        gate: GatePort = AllowAllGate()
        request = GateRequest(
            request_id="gate-1",
            subject="semantic_insight",
            payload={"insight_id": "insight-1"},
        )

        decision = await gate.review(request)

        assert decision.action is GateDecisionAction.ALLOW
        assert decision.request_id == "gate-1"

    asyncio.run(scenario())


def test_telemetry_port_records_runtime_diagnostics() -> None:
    class RecordingTelemetry:
        def __init__(self) -> None:
            self.records: list[TelemetryRecord] = []

        async def record(self, record: TelemetryRecord) -> None:
            self.records.append(record)

    async def scenario() -> None:
        telemetry: TelemetryPort = RecordingTelemetry()
        record = TelemetryRecord(
            name="memory.priors_retrieved",
            value=3,
            occurred_at=datetime(2026, 5, 23, tzinfo=UTC),
            attributes={"strategy": "core"},
        )

        await telemetry.record(record)

        assert isinstance(telemetry, RecordingTelemetry)
        assert telemetry.records == [record]

    asyncio.run(scenario())

