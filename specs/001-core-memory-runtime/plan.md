# Implementation Plan: Core Memory Runtime

**Feature**: `specs/001-core-memory-runtime/spec.md`  
**Package**: `anamnesis-runtime` / `anamnesis_runtime`  
**Branch**: `main` until a feature branch is created for implementation  
**Date**: 2026-05-23

## Technical Context

- Language/runtime: Python 3.11+
- Package manager: `uv`
- Build backend: Hatchling
- Test runner: pytest
- Lint/type: Ruff and mypy
- Runtime dependencies: standard library only
- Integration type: host-neutral library kernel

## Architecture

```text
MemoryRuntime
  -> MessageBuffer
  -> MessagePartitioner
  -> EpisodeGenerator
  -> EpisodicStore
  -> SemanticStore
  -> EpisodePredictor
  -> PredictionErrorDistiller
  -> SemanticConsolidator
  -> optional basin/gate/event/telemetry ports
```

The runtime is orchestration, not host policy. It coordinates injected dependencies and in-memory test stores. Adapters depend inward on contracts; core never imports adapters.

## Constitution / Boundary Check

- Host-neutral core: PASS if no forbidden imports exist under `src/anamnesis_runtime`.
- Tests-first: new behavior must begin with tests.
- Dependency discipline: core remains stdlib-only.
- Adapter boundary: host integrations are specified in later specs only.

## Implementation Phases

### Phase 1 - Public contracts

Harden current models and ports:
- add missing event/gate/telemetry protocols if needed;
- keep records frozen/typed where practical;
- document validation rules.

### Phase 2 - Runtime behavior

Harden `MemoryRuntime`:
- keep prior retrieval before prediction;
- return explicit episode and recall shapes;
- surface health/stats without host state.

### Phase 3 - Boundary verification

Add tests that scan AST imports under `src/anamnesis_runtime` and fail on forbidden package names.

### Phase 4 - Docs and packaging

Keep README, `docs/architecture.md`, and CI aligned with the public contract.

## Project Structure

```text
src/anamnesis_runtime/
  __init__.py
  models.py
  ports.py
  buffer.py
  stores.py
  runtime.py
tests/
  test_models.py
  test_runtime.py
  test_import_boundaries.py
docs/
  architecture.md
```

## Verification

```sh
uv run --extra dev pytest
uv run --extra dev ruff check .
uv run --extra dev mypy
uv build
```

