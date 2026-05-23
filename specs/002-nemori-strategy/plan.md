# Implementation Plan: Nemori Strategy

**Feature**: `specs/002-nemori-strategy/spec.md`  
**Status**: Planned after `001-core-memory-runtime`

## Technical Context

- Build on Anamnesis core models and ports.
- Keep default implementation in-process and testable with fakes.
- Do not add production infrastructure dependencies.
- Treat Dionysus Spec 699 and its feature ranking as source context, not runtime dependency.

## Architecture

```text
NemoriStrategy
  -> MemoryBuffer
  -> Segmenter
  -> EpisodeGenerator
  -> PriorRetriever
  -> Predictor
  -> PredictionErrorDistiller
  -> SemanticConsolidator
  -> RecallRanker
```

Nemori should live under a strategy namespace such as:

```text
src/anamnesis_runtime/strategies/nemori/
```

## Design Decisions

- Strategy depends on core contracts only.
- LLM and embedding behavior remain injected ports.
- Stores remain abstract.
- Host-specific routing context is optional metadata and cannot replace semantic prior retrieval.

## Verification

```sh
uv run --extra dev pytest tests/test_nemori_strategy.py
uv run --extra dev pytest tests/test_import_boundaries.py
uv run --extra dev ruff check .
uv run --extra dev mypy
```

