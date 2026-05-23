# Feature Specification: Dionysus Adapter

**Feature Directory**: `specs/004-dionysus-adapter`  
**Status**: Planning artifact only  
**Created**: 2026-05-23

## Summary

Dionysus uses Anamnesis through adapters only. Anamnesis core remains provider-neutral and must not import Dionysus-specific or infrastructure-specific systems.

Covered adapter targets:
- Graphiti persistence
- Qdrant vector projection
- MemoryBasinRouter routing context
- MemEvolve evaluation/adaptation
- Sakshi gating/witness checks
- EventBus, Redis, and RabbitMQ bridges
- migration from Dionysus Spec 699

## User Scenarios & Testing

### User Story 1 - Dionysus calls Anamnesis through stable adapters

As Dionysus, I can call Anamnesis memory capabilities through adapter-owned integration code without changing Anamnesis core.

### User Story 2 - Core remains independent

As Anamnesis core, I provide memory contracts without importing Dionysus, Graphiti, Qdrant, MemoryBasinRouter, MemEvolve, Sakshi, EventBus, Redis, RabbitMQ, or FastAPI.

### User Story 3 - Adapter-by-adapter migration

As a migration owner, I can move Dionysus Spec 699 behavior into adapter-owned integration code one adapter at a time behind tests.

### User Story 4 - Operator control

As an operator, I can enable or disable each Dionysus adapter independently.

## Requirements

- FR-001: Anamnesis core MUST expose only neutral ports/contracts for memory writes, reads, projections, routing, evolution, gates, and events.
- FR-002: GraphitiAdapter MUST translate Anamnesis memory records/events into Graphiti-compatible graph operations.
- FR-003: QdrantProjectionAdapter MUST project eligible records into vector-store payloads without leaking Qdrant types into core.
- FR-004: MemoryBasinRouterAdapter MUST map neutral routing decisions to Dionysus basin routing behavior.
- FR-005: MemEvolveAdapter MUST consume neutral memory evolution requests and return neutral evolution results.
- FR-006: SakshiGateAdapter MUST enforce gating through a neutral gate interface.
- FR-007: EventBus/Redis/RabbitMQ bridges MUST publish and consume neutral Anamnesis events outside core.
- FR-008: Adapter failures MUST be loud, typed, and observable.
- FR-009: Migration from Dionysus Spec 699 MUST preserve behavior through adapter tests before replacing old call paths.

## Success Criteria

- SC-001: Adapter contract tests prove each adapter consumes neutral Anamnesis records.
- SC-002: Import-boundary tests prove Anamnesis core remains independent.
- SC-003: Migration matrix maps each Spec 699 call path to old behavior, new port, adapter, parity test, and cutover gate.

## Out of Scope

- Immediate Dionysus code changes.
- Pushing Dionysus branches.
- Runtime activation.
- Destructive deletion of existing Dionysus Nemori code.

