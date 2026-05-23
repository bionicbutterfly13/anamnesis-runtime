# Tasks: Nemori Strategy

## Phase 1: Preconditions

- [X] T001 Complete `specs/001-core-memory-runtime` implementation and verification.
- [X] T002 Confirm current core ports support strategy implementation in `src/anamnesis_runtime/ports.py`.

## Phase 2: Tests first

- [X] T010 [P] Add Nemori buffering/segmentation tests in `tests/test_nemori_strategy.py`.
- [X] T011 [P] Add prior-before-prediction tests in `tests/test_nemori_strategy.py`.
- [X] T012 [P] Add raw-episode calibration tests in `tests/test_nemori_strategy.py`.
- [X] T013 Add import-boundary coverage for `src/anamnesis_runtime/strategies/nemori`.

## Phase 3: Strategy implementation

- [X] T020 Create strategy package `src/anamnesis_runtime/strategies/nemori/__init__.py`.
- [X] T021 Implement buffering and segmentation behavior in `src/anamnesis_runtime/strategies/nemori/pipeline.py`.
- [X] T022 Implement prior retrieval and prediction orchestration in `src/anamnesis_runtime/strategies/nemori/predict_calibrate.py`.
- [X] T023 Implement semantic consolidation and recall behavior in `src/anamnesis_runtime/strategies/nemori/consolidation.py`.

## Phase 4: Verification

- [X] T030 Run focused Nemori strategy tests.
- [X] T031 Run full pytest, ruff, mypy, and build.
- [X] T032 Update docs to describe Nemori as a strategy, not the package identity.
