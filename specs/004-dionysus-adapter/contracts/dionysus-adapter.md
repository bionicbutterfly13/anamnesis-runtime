# Contract: Dionysus Adapter Boundary

## Neutral Contracts

- `MemoryRecord`
- `MemoryEvent`
- `GraphMutation`
- `ProjectionPayload`
- `RoutingRequest`
- `RoutingDecision`
- `EvolutionRequest`
- `EvolutionResult`
- `GateRequest`
- `GateDecision`
- `EventEnvelope`

## Adapter Responsibilities

- GraphitiAdapter: durable graph persistence.
- QdrantProjectionAdapter: vector projection payloads.
- MemoryBasinRouterAdapter: routing context and activation metadata.
- MemEvolveAdapter: memory-process evaluation and adaptation.
- SakshiGateAdapter: witness/gating/write-guard checks.
- Event bridge: EventBus, Redis Streams, RabbitMQ translation.

## Failure Rules

- Adapter failures are loud and typed.
- Silent fallback is forbidden unless explicitly configured by the host.
- Core never catches infrastructure-specific exceptions directly.

