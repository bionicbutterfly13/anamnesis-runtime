# Contract: Dionysus Adapter Boundary

## Neutral Contracts

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

## Core Contract Module

Anamnesis core exposes these contracts from `anamnesis_runtime.adapters` and the
top-level `anamnesis_runtime` namespace:

- `GraphMutationPort.apply_mutation(GraphMutation) -> None`
- `ProjectionPort.project(ProjectionPayload) -> None`
- `RoutingPort.route(RoutingRequest) -> RoutingDecision`
- `EvolutionPort.evolve(EvolutionRequest) -> EvolutionResult`
- `EventBridgePort.publish(MemoryEvent) -> None`
- `EventBridgePort.subscribe(event_type, handler) -> None`

`GateRequest`, `GateDecision`, and `GatePort` remain the canonical gate
contracts from the existing core gate port.

## Adapter Responsibilities

- GraphitiAdapter: durable graph persistence.
- QdrantProjectionAdapter: vector projection payloads.
- MemoryBasinRouterAdapter: routing context and activation metadata.
- MemEvolveAdapter: memory-process evaluation and adaptation.
- SakshiGateAdapter: witness/gating/write-guard checks.
- Event bridge: EventBus, Redis Streams, RabbitMQ translation.

These are adapter responsibilities, not core implementation classes. Real
adapters live in Dionysus or an optional integration package.

## Failure Rules

- Adapter failures are loud and typed.
- Silent fallback is forbidden unless explicitly configured by the host.
- Core never catches infrastructure-specific exceptions directly.
- Core never imports Dionysus, Graphiti, Qdrant, MemoryBasinRouter, MemEvolve,
  Sakshi, EventBus, Redis, RabbitMQ, FastAPI, Elume, Autonoesis, LinOSS, or
  host-app modules.
