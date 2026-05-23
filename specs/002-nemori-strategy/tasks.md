# Tasks: Nemori Strategy

## Phase 1: Preconditions

- [ ] T001 Complete `specs/001-core-memory-runtime` implementation and verification.
- [ ] T002 Confirm current core ports support strategy implementation in `src/anamnesis_runtime/ports.py`.

## Phase 2: Tests first

- [ ] T010 [P] Add Nemori buffering/segmentation tests in `tests/test_nemori_strategy.py`.
- [ ] T011 [P] Add prior-before-prediction tests in `tests/test_nemori_strategy.py`.
- [ ] T012 [P] Add raw-episode calibration tests in `tests/test_nemori_strategy.py`.
- [ ] T013 Add import-boundary coverage for `src/anamnesis_runtime/strategies/nemori`.

## Phase 3: Strategy implementation

- [ ] T020 Create strategy package `src/anamnesis_runtime/strategies/nemori/__init__.py`.
- [ ] T021 Implement buffering and segmentation behavior in `src/anamnesis_runtime/strategies/nemori/pipeline.py`.
- [ ] T022 Implement prior retrieval and prediction orchestration in `src/anamnesis_runtime/strategies/nemori/predict_calibrate.py`.
- [ ] T023 Implement semantic consolidation and recall behavior in `src/anamnesis_runtime/strategies/nemori/consolidation.py`.

## Phase 4: Verification

- [ ] T030 Run focused Nemori strategy tests.
- [ ] T031 Run full pytest, ruff, mypy, and build.
- [ ] T032 Update docs to describe Nemori as a strategy, not the package identity.

