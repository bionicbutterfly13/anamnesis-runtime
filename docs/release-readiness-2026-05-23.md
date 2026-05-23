# Release Readiness Report - 2026-05-23

## Current State

Anamnesis Runtime is a host-neutral pre-alpha package with four stacked feature
branches:

| Order | Branch | Feature commit | Purpose |
|---|---|---|---|
| 1 | `feature/001-core-memory-runtime-ports` | `14b440a` | Core event, gate, telemetry ports and exports |
| 2 | `feature/002-nemori-strategy` | `2d9597a` | Host-neutral Nemori strategy |
| 3 | `feature/003-event-transports` | `a03c681` | Neutral memory event transports |
| 4 | `feature/004-dionysus-adapter` | `ad45c67` | Dionysus adapter boundary contracts |

The safe merge order is sequential: merge `001`, then rebase/merge `002`, then
`003`, then `004`. The branches are stacked linearly, so squashing the entire
stack into one release commit is also technically possible, but sequential PRs
preserve the Spec Kit audit trail and make regressions easier to isolate.

## Package Readiness

Ready:

- Distribution name: `anamnesis-runtime`.
- Import package: `anamnesis_runtime`.
- Runtime dependencies: none.
- Dev extra: `pytest`, `ruff`, and `mypy`.
- Type marker: `src/anamnesis_runtime/py.typed`.
- CI exists for lint, typecheck, and tests.
- Build backend: Hatchling.
- Public API exports are covered by tests.
- Import-boundary tests prohibit host and infrastructure imports in core.

Needs decision before PyPI:

- License file and `pyproject.toml` license metadata are missing.
- Release owner must decide whether this is MIT, Apache-2.0, proprietary, or
  another license.
- PyPI publication credentials/trusted publishing are not configured here.
- Version `0.1.0` should remain pre-alpha unless Dr. Mani approves a wider
  release.

Current PyPI naming check:

- `anamnesis` is registered for an unrelated HDF5/MPI serialization package.
- `anamnesis-runtime` returned 404 from the PyPI JSON API on 2026-05-23, so the
  name appears available at check time.

## Host-Neutral Boundary

Anamnesis core must remain standard-library-only and must not import Dionysus,
Graphiti, Qdrant, MemoryBasinRouter, MemEvolve, Sakshi, EventBus, Redis,
RabbitMQ, FastAPI, Elume, Autonoesis, LinOSS, or host-app modules.

The current adapter contracts are neutral:

- `GraphMutation` / `GraphMutationPort`
- `ProjectionPayload` / `ProjectionPort`
- `RoutingRequest`, `RoutingDecision`, `RoutingPort`
- `EvolutionRequest`, `EvolutionResult`, `EvolutionPort`
- `GateRequest`, `GateDecision`, `GatePort`
- `MemoryEvent`, `EventEnvelope`, `EventBridgePort`

## Dionysus Adapters Still Needed

These belong in Dionysus or an optional integration package, not in Anamnesis
core:

- `GraphitiAdapter`
- `QdrantProjectionAdapter`
- `MemoryBasinRouterAdapter`
- `MemEvolveAdapter`
- `SakshiGateAdapter`
- EventBus bridge
- Redis Streams bridge
- RabbitMQ bridge

## Runtime Activation Gates

Dionysus migration should use these gates:

1. Add feature flags for each adapter independently.
2. Wire one adapter at a time.
3. Start with fake/contract parity tests, then host integration tests.
4. Require typed adapter failures and telemetry before activation.
5. Keep rollback to the old `NemoriRiverFlow` path for each adapter family.
6. Do not cut over until parity tests prove equivalent graph, projection,
   routing, evolution, gate, and event intents.
7. Never let basin routing or vector projection replace semantic prior search.

## Remaining Nemori Parity Work

- Deeper end-to-end proof that retrieved semantic priors improve next-episode
  prediction.
- Predict-Calibrate parity against Dionysus `NemoriRiverFlow`.
- Benchmark harness plan for LoCoMo / LongMemEval-style evaluation.
- Observability for boundary rate, prior retrieval count, prediction-error
  volume, consolidation decisions, and recall composition.
- Tunables for episodic/semantic retrieval ratios and consolidation thresholds.
- Compatibility shim strategy so Dionysus callers migrate without deleting the
  old path first.

## Exact Dionysus Migration Goal Prompt

```text
/goal Work in /Volumes/Asylum/dev/dionysus3 to create the Dionysus-side Anamnesis migration plan and first adapter parity tests.

Use Anamnesis Runtime only as an external host-neutral package. Do not add Dionysus, Graphiti, Qdrant, MemoryBasinRouter, MemEvolve, Sakshi, EventBus, Redis, RabbitMQ, FastAPI, Elume, Autonoesis, LinOSS, or host-app imports to /Volumes/Asylum/dev/anamnesis-runtime.

Scope:
- Read Anamnesis specs/004-dionysus-adapter/migration-matrix.md as the adapter boundary source.
- Keep Dionysus changes on a new isolated feature branch.
- Add Dionysus-side fake/contract tests for GraphitiAdapter, QdrantProjectionAdapter, MemoryBasinRouterAdapter, MemEvolveAdapter, SakshiGateAdapter, EventBus bridge, Redis Streams bridge, and RabbitMQ bridge.
- Map each old NemoriRiverFlow/Spec 699 call path to an Anamnesis contract, a Dionysus adapter, a parity test, and a feature flag.
- Do not cut over production runtime.
- Do not delete NemoriRiverFlow.
- Do not touch /Volumes/Asylum/Sync or any /Sync/ path.

Verification:
- Run focused Dionysus adapter parity tests.
- Run existing focused NemoriRiverFlow compatibility tests.
- Run import-boundary checks proving Anamnesis remains host-neutral.

Final report must include changed files, test results, adapter matrix, feature flags, rollback gates, and the next implementation prompt for the first real adapter.
```

## Exact Next Nemori Parity Goal Prompt

```text
/goal Work in /Volumes/Asylum/dev/anamnesis-runtime to deepen Nemori parity inside Anamnesis Runtime without adding host imports.

Follow tests first. Implement only host-neutral Nemori parity improvements that do not require Dionysus, Graphiti, Qdrant, MemoryBasinRouter, MemEvolve, Sakshi, EventBus, Redis, RabbitMQ, FastAPI, Elume, Autonoesis, LinOSS, or host-app imports.

Start with RED tests for:
- end-to-end prior retrieval improving the next episode prediction path
- raw-message calibration remaining distinct from narrative episode text
- configurable episodic/semantic retrieval ratios
- telemetry records for prior retrieval count, prediction-error volume, and consolidation decisions
- compatibility fixtures that can later be compared against Dionysus NemoriRiverFlow

Do not implement benchmarks yet. Do not implement Dionysus adapters. Do not publish to PyPI.

Verification:
- uv run --extra dev pytest
- uv run --extra dev ruff check .
- uv run --extra dev mypy
- uv build
- forbidden import grep across src and tests

Final report must include changed files, commit SHA, verification results, remaining parity gaps, and the next benchmark-harness planning prompt.
```
