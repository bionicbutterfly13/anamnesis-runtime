# Tasks: Core Memory Runtime

## Phase 1: Setup / baseline

- [X] T001 Confirm current package skeleton and public exports in `src/anamnesis_runtime/__init__.py`.
- [X] T002 Run `uv run --extra dev pytest`, `uv run --extra dev ruff check .`, `uv run --extra dev mypy`, and `uv build`.

## Phase 2: Tests first

- [X] T010 [P] Add import-boundary tests in `tests/test_import_boundaries.py`.
- [X] T011 [P] Add event/gate/telemetry port tests in `tests/test_ports.py`.
- [X] T012 Run new tests and verify RED for missing port coverage if ports are incomplete.

## Phase 3: Core implementation

- [X] T020 Add any missing host-neutral event/gate/telemetry protocols in `src/anamnesis_runtime/ports.py`.
- [X] T021 Update public exports in `src/anamnesis_runtime/__init__.py`.
- [X] T022 Update docs in `README.md` and `docs/architecture.md`.

## Phase 4: Verification

- [X] T030 Run `uv run --extra dev pytest`.
- [X] T031 Run `uv run --extra dev ruff check .`.
- [X] T032 Run `uv run --extra dev mypy`.
- [X] T033 Run `uv build`.
- [X] T034 Commit the completed core-runtime hardening slice.
