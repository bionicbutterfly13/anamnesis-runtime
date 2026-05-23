# Tasks: Dionysus Adapter

## Phase 1: Migration map

- [ ] T001 Read Dionysus Spec 699 and Nemori feature ranking as read-only context.
- [ ] T002 Create a Spec 699 migration matrix in `specs/004-dionysus-adapter/migration-matrix.md`.
- [ ] T003 Map old Dionysus behavior to Anamnesis port, adapter, parity test, and cutover gate.

## Phase 2: Contract tests

- [ ] T010 [P] Add GraphitiAdapter contract tests in `tests/test_dionysus_adapter_contracts.py`.
- [ ] T011 [P] Add QdrantProjectionAdapter contract tests in `tests/test_dionysus_adapter_contracts.py`.
- [ ] T012 [P] Add MemoryBasinRouterAdapter contract tests in `tests/test_dionysus_adapter_contracts.py`.
- [ ] T013 [P] Add MemEvolveAdapter contract tests in `tests/test_dionysus_adapter_contracts.py`.
- [ ] T014 [P] Add SakshiGateAdapter contract tests in `tests/test_dionysus_adapter_contracts.py`.

## Phase 3: Adapter implementation location decision

- [ ] T020 Decide whether Dionysus adapters live in Dionysus, `anamnesis-dionysus`, or optional extras.
- [ ] T021 Document runtime wiring and activation gates.

## Phase 4: Verification

- [ ] T030 Run import-boundary tests.
- [ ] T031 Run adapter contract tests with fakes.
- [ ] T032 Defer real Dionysus cutover to a Dionysus-owned feature branch.

