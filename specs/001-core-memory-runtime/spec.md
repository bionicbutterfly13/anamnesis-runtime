# Feature Specification: Core Memory Runtime

**Feature Directory**: `specs/001-core-memory-runtime`  
**Status**: Ready for implementation planning  
**Created**: 2026-05-23  
**Input**: Dr. Mani wants Anamnesis Runtime to be the clean host-neutral extraction target for Dionysus memory logic.

## Summary

Anamnesis provides the host-neutral memory lifecycle for cyclic agent systems:

```text
raw messages/events -> raw episodes -> narrative episodes -> semantic priors
-> prediction -> prediction-error insights -> consolidation decisions -> recall results
```

The core package owns records, ports, orchestration, in-memory test stores, event hooks, and import-boundary rules. Host apps own concrete LLMs, vector stores, graph stores, event buses, API routes, dashboards, credentials, activation flags, and policy.

## User Scenarios & Testing

### User Story 1 - Ingest neutral messages

As an agent host, I need to send raw messages or observations into Anamnesis without adopting a Dionysus-specific event type.

Acceptance:
- Given valid messages with role/content/timestamp metadata, the runtime buffers them through a neutral interface.
- Given missing identifiers or naive timestamps, model validation fails loudly.
- Tests prove core imports do not reference Dionysus or infrastructure packages.

### User Story 2 - Run the memory lifecycle offline

As a package maintainer, I need the default runtime to run with fakes/in-memory stores so the package can be tested without external services.

Acceptance:
- Given injected partitioner, episode generator, predictor, and distiller fakes, `MemoryRuntime.flush()` produces episodes and semantic insights.
- Given prior semantic insights in the store, prediction receives retrieved priors before distillation.
- Tests pass without Graphiti, Qdrant, Redis, RabbitMQ, EventBus, FastAPI, or Dionysus imports.

### User Story 3 - Recall episodic and semantic context

As an agent loop, I need a stable recall result that separates narrative episodes from semantic insights.

Acceptance:
- Given stored episodes and insights, `MemoryRuntime.search()` returns a `NemoriRecallResult` with separate episodic and semantic collections.
- Ranking metadata and basin metadata are optional annotations, not core routing policy.

### User Story 4 - Expose extension ports

As an integration author, I need protocols for stores, prediction, distillation, consolidation, gating, events, and telemetry.

Acceptance:
- Ports describe behavior without importing implementation packages.
- The public API exports stable core records and ports.
- Host-specific adapters can be written outside the package against these contracts.

## Requirements

### Functional Requirements

- FR-001: Core MUST define host-neutral models for messages, content parts, raw episodes, narrative episodes, semantic priors, predictions, semantic insights, consolidation decisions, recall results, and optional routing metadata.
- FR-002: Core MUST define protocols for buffering, partitioning, episode generation, episodic storage, semantic storage, prediction, distillation, consolidation, basin/gate hooks, event publication, and telemetry.
- FR-003: Core MUST provide in-memory buffer, episodic store, and semantic store implementations for offline tests and local experiments.
- FR-004: Core MUST provide a `MemoryRuntime` orchestration surface with `add_messages`, `flush`, `search`, `health`, and `stats`.
- FR-005: Core MUST retrieve semantic priors before invoking prediction.
- FR-006: Core MUST keep consolidation decisions explicit as `new`, `merge`, or `conflict`.
- FR-007: Core MUST expose import-safe public exports from `anamnesis_runtime.__init__`.
- FR-008: Core MUST include tests that fail if forbidden host dependencies are imported by package modules.
- FR-009: Core MUST support deterministic tests through injectable dependencies.
- FR-010: Core MUST remain install-light with no runtime dependencies beyond the Python standard library unless a future spec justifies one.

### Non-Functional Requirements

- NFR-001: No direct or transitive imports from Dionysus, Elume, Autonoesis, Sakshi, LinOSS, Graphiti, Qdrant, Redis, RabbitMQ, EventBus, FastAPI, or host apps inside core modules.
- NFR-002: Tests, lint, typecheck, and build must pass before publishing or adapter work.
- NFR-003: Public contracts should be typed and documented.
- NFR-004: Core terminology should remain vocabulary-neutral; OODA/ReAct/MIDCA/active-inference naming belongs in adapters.

## Key Entities

- `NemoriMessage`
- `NemoriRawEpisode`
- `NemoriEpisode`
- `PriorMemory`
- `Prediction`
- `NemoriSemanticInsight`
- `ConsolidationDecision`
- `NemoriRecallResult`
- `MemoryRuntime`
- Store and strategy ports

## Success Criteria

- SC-001: `uv run pytest`, `uv run ruff check .`, `uv run mypy`, and `uv build` pass.
- SC-002: Core import-boundary test confirms no forbidden host dependency names in package imports.
- SC-003: Runtime test proves retrieved semantic priors are passed into prediction before distillation.
- SC-004: README and architecture docs clearly distinguish Anamnesis core from host adapters.

## Out of Scope

- Full Nemori paper parity.
- Graphiti, Qdrant, Redis, RabbitMQ, EventBus, FastAPI, Dionysus, Elume, Autonoesis, Sakshi, or LinOSS adapters.
- Benchmark harnesses.
- Production activation policy.

