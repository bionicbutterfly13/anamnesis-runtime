import asyncio
from datetime import UTC, datetime

from anamnesis_runtime import (
    EventBridgePort,
    EvolutionAction,
    EvolutionPort,
    EvolutionRequest,
    EvolutionResult,
    GateDecision,
    GateDecisionAction,
    GatePort,
    GateRequest,
    GraphMutation,
    GraphMutationOperation,
    GraphMutationPort,
    MemoryEvent,
    ProjectionPayload,
    ProjectionPort,
    RoutingDecision,
    RoutingPort,
    RoutingRequest,
)


def test_graph_mutation_and_projection_payload_contracts_are_neutral() -> None:
    mutation = GraphMutation(
        mutation_id="graph-mutation-1",
        operation=GraphMutationOperation.UPSERT_NODE,
        subject_id="insight-1",
        subject_type="semantic_insight",
        properties={"content": "Dr. Mani prefers host-neutral memory contracts."},
        links=({"relationship": "originated_from", "target_id": "episode-1"},),
        metadata={"source": "contract-test"},
    )
    projection = ProjectionPayload(
        projection_id="projection-1",
        record_id="insight-1",
        text="Dr. Mani prefers host-neutral memory contracts.",
        vector=(0.1, 0.2, 0.3),
        metadata={"memory_type": "semantic"},
    )

    assert mutation.operation is GraphMutationOperation.UPSERT_NODE
    assert mutation.subject_type == "semantic_insight"
    assert mutation.links[0]["relationship"] == "originated_from"
    assert projection.record_id == mutation.subject_id
    assert projection.vector == (0.1, 0.2, 0.3)


def test_routing_and_evolution_contracts_are_neutral() -> None:
    routing_request = RoutingRequest(
        request_id="route-1",
        record_id="insight-1",
        memory_type="semantic",
        context={"active_lane": "reflective"},
        metadata={"recall_boost": 0.2},
    )
    routing_decision = RoutingDecision(
        request_id=routing_request.request_id,
        route="reflective-basin",
        confidence=0.87,
        reason="active lane matched semantic context",
        metadata={"placement": "primary"},
    )
    evolution_request = EvolutionRequest(
        request_id="evolve-1",
        record_id="insight-1",
        signal="prediction_error_high",
        evidence={"new_insight_count": 3},
        metadata={"strategy": "nemori"},
    )
    evolution_result = EvolutionResult(
        request_id=evolution_request.request_id,
        action=EvolutionAction.ADAPT,
        rationale="prediction errors indicate a useful consolidation threshold change",
        metadata={"threshold_delta": -0.05},
    )

    assert routing_request.memory_type == "semantic"
    assert routing_decision.confidence == 0.87
    assert evolution_result.action is EvolutionAction.ADAPT
    assert evolution_result.request_id == evolution_request.request_id


def test_fake_graphiti_and_qdrant_objects_conform_to_neutral_ports() -> None:
    class FakeGraphiti:
        def __init__(self) -> None:
            self.mutations: list[GraphMutation] = []

        async def apply_mutation(self, mutation: GraphMutation) -> None:
            self.mutations.append(mutation)

    class FakeQdrant:
        def __init__(self) -> None:
            self.payloads: list[ProjectionPayload] = []

        async def project(self, payload: ProjectionPayload) -> None:
            self.payloads.append(payload)

    async def scenario() -> None:
        graph: GraphMutationPort = FakeGraphiti()
        projection_store: ProjectionPort = FakeQdrant()
        mutation = GraphMutation(
            mutation_id="graph-mutation-1",
            operation=GraphMutationOperation.UPSERT_NODE,
            subject_id="episode-1",
            subject_type="episode",
        )
        projection = ProjectionPayload(
            projection_id="projection-1",
            record_id="episode-1",
            text="A host app may project this record.",
        )

        await graph.apply_mutation(mutation)
        await projection_store.project(projection)

        assert isinstance(graph, FakeGraphiti)
        assert graph.mutations == [mutation]
        assert isinstance(projection_store, FakeQdrant)
        assert projection_store.payloads == [projection]

    asyncio.run(scenario())


def test_fake_basin_router_and_memevolve_objects_conform_to_neutral_ports() -> None:
    class FakeBasinRouter:
        async def route(self, request: RoutingRequest) -> RoutingDecision:
            return RoutingDecision(
                request_id=request.request_id,
                route="semantic-basin",
                confidence=0.91,
                reason="semantic memory type",
                metadata={"record_id": request.record_id},
            )

    class FakeMemEvolve:
        async def evolve(self, request: EvolutionRequest) -> EvolutionResult:
            return EvolutionResult(
                request_id=request.request_id,
                action=EvolutionAction.REVIEW,
                rationale="record requires host-side process evaluation",
                metadata={"record_id": request.record_id},
            )

    async def scenario() -> None:
        router: RoutingPort = FakeBasinRouter()
        evolution: EvolutionPort = FakeMemEvolve()

        route = await router.route(
            RoutingRequest(
                request_id="route-1",
                record_id="insight-1",
                memory_type="semantic",
            )
        )
        result = await evolution.evolve(
            EvolutionRequest(
                request_id="evolve-1",
                record_id="insight-1",
                signal="high_error",
            )
        )

        assert route.route == "semantic-basin"
        assert result.action is EvolutionAction.REVIEW

    asyncio.run(scenario())


def test_fake_sakshi_gate_uses_existing_gate_port_contracts() -> None:
    class FakeSakshi:
        async def review(self, request: GateRequest) -> GateDecision:
            return GateDecision(
                action=GateDecisionAction.ALLOW,
                request_id=request.request_id,
                reason="fake witness allows contract test",
                metadata={"subject": request.subject},
            )

    async def scenario() -> None:
        gate: GatePort = FakeSakshi()
        request = GateRequest(
            request_id="gate-1",
            subject="graph_mutation",
            payload={"mutation_id": "graph-mutation-1"},
        )

        decision = await gate.review(request)

        assert decision.action is GateDecisionAction.ALLOW
        assert decision.metadata["subject"] == "graph_mutation"

    asyncio.run(scenario())


def test_fake_event_bridge_conforms_to_neutral_event_bridge_port() -> None:
    class FakeEventBridge:
        def __init__(self) -> None:
            self.handlers: list[tuple[str, object]] = []
            self.events: list[MemoryEvent] = []

        async def publish(self, event: MemoryEvent) -> None:
            self.events.append(event)
            for event_type, handler in self.handlers:
                if event_type == event.event_type:
                    result = handler(event)
                    if hasattr(result, "__await__"):
                        await result

        async def subscribe(self, event_type: str, handler: object) -> None:
            self.handlers.append((event_type, handler))

    async def scenario() -> None:
        bridge: EventBridgePort = FakeEventBridge()
        received: list[MemoryEvent] = []
        event = MemoryEvent(
            event_id="evt-1",
            event_type="memory.graph_mutation_requested",
            schema_version=1,
            occurred_at=datetime(2026, 5, 23, tzinfo=UTC),
            source="contract-test",
            payload={"mutation_id": "graph-mutation-1"},
        )

        await bridge.subscribe("memory.graph_mutation_requested", received.append)
        await bridge.publish(event)

        assert isinstance(bridge, FakeEventBridge)
        assert received == [event]
        assert bridge.events == [event]

    asyncio.run(scenario())


def test_adapter_contracts_do_not_expose_real_host_adapter_clients() -> None:
    import anamnesis_runtime.adapters as adapter_contracts

    forbidden_real_adapters = {
        "GraphitiAdapter",
        "QdrantProjectionAdapter",
        "MemoryBasinRouterAdapter",
        "MemEvolveAdapter",
        "SakshiGateAdapter",
        "RedisBridge",
        "RabbitMQBridge",
        "EventBusBridge",
    }

    assert forbidden_real_adapters.isdisjoint(dir(adapter_contracts))
