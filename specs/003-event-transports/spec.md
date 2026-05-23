# Feature Specification: Event Transports

**Feature Directory**: `specs/003-event-transports`  
**Status**: Planning artifact only  
**Created**: 2026-05-23

## Summary

Anamnesis core defines neutral memory event contracts and publisher/subscriber ports. Transport adapters are optional and live outside core.

Adapter targets:
- in-process EventBus bridge for local runtime coordination;
- Redis Streams for lightweight distributed events, replay, and consumer groups;
- RabbitMQ for brokered routing, acknowledgements, retries, and queue topology.

## User Scenarios & Testing

### User Story 1 - Stable event contract

As an Anamnesis integrator, I need a stable `MemoryEvent` contract so memory events can move through different transports without changing core logic.

### User Story 2 - Neutral publisher

As a runtime service, I need to publish memory events through a neutral port so delivery can be in-process, Redis, RabbitMQ, or a test fake.

### User Story 3 - Neutral subscriber

As a consumer, I need to subscribe to memory events through a neutral port so handlers are independent of transport implementation.

### User Story 4 - Explicit adapter selection

As a host app, I need to wire the transport adapter explicitly so Anamnesis remains reusable across Dionysus and non-Dionysus runtimes.

## Requirements

- FR-001: Core MUST define a neutral `MemoryEvent` contract.
- FR-002: Core MUST define publisher and subscriber ports.
- FR-003: Core MUST NOT import EventBus, Redis, RabbitMQ, Dionysus, or host-app modules.
- FR-004: Events MUST include stable identifiers, event type, schema version, occurrence timestamp, source, correlation ID, causation ID, payload, and metadata.
- FR-005: Publisher ports MUST support publishing one event at a time.
- FR-006: Subscriber ports MUST support registering handlers by event type or pattern.
- FR-007: Handlers MUST receive decoded `MemoryEvent` instances, not raw transport messages.
- FR-008: EventBus adapter MUST map event types to local in-process event names.
- FR-009: Redis Streams adapter MUST support append, replay, and consumer group consumption.
- FR-010: RabbitMQ adapter MUST support exchange/routing-key/queue topology, acknowledgements, retries, and dead-letter strategy.
- FR-011: Transport errors MUST surface through explicit adapter errors without leaking transport libraries into core.

## Success Criteria

- SC-001: Core event tests pass without transport dependencies installed.
- SC-002: Adapter conformance tests can run against fake EventBus, fake Redis, and fake RabbitMQ clients.
- SC-003: Import-boundary tests prove no transport imports in core.

## Out of Scope

- Concrete Redis or RabbitMQ package dependency in the core install.
- Dionysus EventBus implementation.
- Production retry policy beyond adapter contract definition.

