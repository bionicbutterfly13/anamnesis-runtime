# Tasks: Core Memory Runtime

## Phase 1: Setup / baseline

- [ ] T001 Confirm current package skeleton and public exports in `src/anamnesis_runtime/__init__.py`.
- [ ] T002 Run `uv run --extra dev pytest`, `uv run --extra dev ruff check .`, `uv run --extra dev mypy`, and `uv build`.

## Phase 2: Tests first

- [ ] T010 [P] Add import-boundary tests in `tests/test_import_boundaries.py`.
- [ ] T011 [P] Add event/gate/telemetry port tests in `tests/test_ports.py`.
- [ ] T012 Run new tests and verify RED for missing port coverage if ports are incomplete.

## Phase 3: Core implementation

- [ ] T020 Add any missing host-neutral event/gate/telemetry protocols in `src/anamnesis_runtime/ports.py`.
- [ ] T021 Update public exports in `src/anamnesis_runtime/__init__.py`.
- [ ] T022 Update docs in `README.md` and `docs/architecture.md`.

## Phase 4: Verification

- [ ] T030 Run `uv run --extra dev pytest`.
- [ ] T031 Run `uv run --extra dev ruff check .`.
- [ ] T032 Run `uv run --extra dev mypy`.
- [ ] T033 Run `uv build`.
- [ ] T034 Commit the completed core-runtime hardening slice.

