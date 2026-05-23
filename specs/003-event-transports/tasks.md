# Tasks: Event Transports

## Phase 1: Core event contracts

- [X] T001 Add RED tests for `MemoryEvent` in `tests/test_events.py`.
- [X] T002 Add publisher/subscriber protocol tests in `tests/test_events.py`.
- [X] T003 Implement neutral event records and ports in `src/anamnesis_runtime/events.py` and `src/anamnesis_runtime/ports.py`.

## Phase 2: Adapter conformance

- [X] T010 [P] Define EventBus bridge conformance tests with fake EventBus client in `tests/test_transport_contracts.py`.
- [X] T011 [P] Define Redis Streams conformance tests with fake Redis client in `tests/test_transport_contracts.py`.
- [X] T012 [P] Define RabbitMQ conformance tests with fake RabbitMQ client in `tests/test_transport_contracts.py`.

## Phase 3: Adapter packaging plan

- [X] T020 Document whether adapters live as extras or separate packages in `docs/architecture.md`.
- [X] T021 Add import-boundary tests that forbid concrete transport imports in core.

## Phase 4: Verification

- [X] T030 Run event and import-boundary tests.
- [X] T031 Run full pytest, ruff, mypy, and build.
