# Implementation Plan: Event Transports

**Feature**: `specs/003-event-transports/spec.md`  
**Status**: Planned after core event ports exist

## Technical Context

- Core stays stdlib-only.
- Transport adapters may become extras or separate packages later.
- Event contracts must be serializable and versioned.

## Architecture

```text
MemoryEvent
  -> MemoryEventPublisher protocol
  -> MemoryEventSubscriber protocol
  -> adapter conformance tests

Adapters outside core:
  -> EventBus bridge
  -> Redis Streams bridge
  -> RabbitMQ bridge
```

## Transport Roles

- EventBus: in-process/local runtime coordination.
- Redis Streams: lightweight distributed event log with replay and consumer groups.
- RabbitMQ: brokered routing with exchanges, queues, acknowledgements, retries, and dead-letter handling.

## Verification

```sh
uv run --extra dev pytest tests/test_events.py tests/test_transport_contracts.py
uv run --extra dev pytest tests/test_import_boundaries.py
```

