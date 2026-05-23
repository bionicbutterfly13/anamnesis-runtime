# Dionysus Adapter Migration Matrix

## Source Context

This matrix is read-only planning context for a Dionysus-side migration. It does
not authorize real Dionysus adapter code inside Anamnesis core.

- Dionysus Spec 699 defines a `NemoriParityFacade` with injected ports for
  message buffering, partitioning, episode generation, semantic prior evoke,
  prediction-error distillation, consolidation, basin integration, and approved
  persistence ports (`/Volumes/Asylum/dev/dionysus3/specs/699-nemori-parity/plan.md:27`).
- Existing `NemoriRiverFlow` remains the compatibility path until migrated
  (`/Volumes/Asylum/dev/dionysus3/specs/699-nemori-parity/plan.md:40`).
- Caller changes are deferred to feature-gated Dionysus work after tests
  (`/Volumes/Asylum/dev/dionysus3/specs/699-nemori-parity/plan.md:60`).
- Basins provide routing, activation, context-prior metadata, and final
  placement after Nemori decides new/merge/conflict; semantic prior search
  remains required (`/Volumes/Asylum/dev/dionysus3/specs/699-nemori-parity/plan.md:69`).
- The ranked Nemori audit maps Tier 1-4 work to Spec 699 phases, led by
  Predict-Calibrate with retrieved priors (`/Volumes/Asylum/dev/dionysus3/docs/audits/2026-05-22-nemori-feature-ranking.md:73`).

## Adapter Location Decision

Initial real adapters should live in Dionysus or a Dionysus-owned integration
package, not in `anamnesis_runtime` core. Anamnesis exposes only neutral
contracts:

- `GraphMutationPort`
- `ProjectionPort`
- `RoutingPort`
- `EvolutionPort`
- existing `GatePort`
- `EventBridgePort`

A future `anamnesis-dionysus` package is acceptable only if it remains optional,
declares host dependencies as extras, and keeps Anamnesis core install-light.

## Runtime Wiring And Activation Gates

Each adapter must be independently activated by Dionysus runtime policy:

| Target | Anamnesis contract | Dionysus-owned adapter | Parity test | Cutover gate |
|---|---|---|---|---|
| Graph persistence | `GraphMutationPort.apply_mutation(GraphMutation)` | `GraphitiAdapter` | Old `GraphitiService.persist_fact()` path and new mutation path produce equivalent node/edge intent. | Feature flag routes one memory write family at a time; rollback returns to old call path. |
| Vector projection | `ProjectionPort.project(ProjectionPayload)` | `QdrantProjectionAdapter` | Eligible records produce the same text, vector, record id, and metadata envelope. | Projection failure is typed and observable; graph authority remains unchanged. |
| Basin routing | `RoutingPort.route(RoutingRequest)` | `MemoryBasinRouterAdapter` | Routing context/activation metadata matches `MemoryBasinRouter.route_memory()` behavior. | Basin metadata may boost or place memory, but cannot replace semantic prior search. |
| Process evolution | `EvolutionPort.evolve(EvolutionRequest)` | `MemEvolveAdapter` | High-error episodes produce equivalent evolution/review signals and no recursive ingestion loop. | Cascade guards remain active before enabling writes. |
| Witness gate | existing `GatePort.review(GateRequest)` | `SakshiGateAdapter` | Allow/block/quarantine/review decisions map to existing write-guard behavior. | Gate decision must happen before graph mutation, projection, routing, or event emission. |
| Event bridge | `EventBridgePort` plus `MemoryEvent`/`EventEnvelope` | EventBus, Redis Streams, or RabbitMQ bridge | Publish/subscribe semantics match transport-specific expectations using neutral events. | Enable one transport bridge at a time; no transport dependency enters core. |

## Spec 699 Behavior Mapping

| Old Dionysus behavior | Evidence | New Anamnesis port/contract | Migration test | Gate |
|---|---|---|---|---|
| `NemoriRiverFlow.predict_and_calibrate()` runs after episode boundary, distills facts, routes facts, and persists them. | `/Volumes/Asylum/dev/dionysus3/docs/memory-pipeline.md:155` | `NemoriStrategy` plus `GraphMutationPort`, `RoutingPort`, and `ProjectionPort` at adapter boundary. | Old flow and new adapter-composed flow produce equivalent episode, semantic insight, routing, and persistence intents. | Do not delete `NemoriRiverFlow`; ship compatibility wrapper first. |
| SEM boundary probability can trigger episode segmentation. | `/Volumes/Asylum/dev/dionysus3/docs/memory-pipeline.md:181` | Host-side boundary signal becomes input metadata to Anamnesis ingest/segmentation; core does not import SEM. | Boundary-triggered fixture produces the same raw episode boundary under old and new flow. | Keep SEM as host-owned signal; Anamnesis stays neutral. |
| Trajectory ingestion uses `MemoryPersistenceAdapter` and Graphiti pipeline steps. | `/Volumes/Asylum/dev/dionysus3/docs/memory-pipeline.md:194` | `EvolutionRequest`/`EvolutionResult` and `GraphMutation` describe the integration intent. | Fake MemEvolve and fake Graphiti contract tests pass before real adapters are wired. | No direct Neo4j or Graphiti client access from Anamnesis. |
| MemoryBasinRouter owns routing and placement behavior. | `/Volumes/Asylum/dev/dionysus3/docs/memory-pipeline.md:227` | `RoutingRequest`/`RoutingDecision` carry active-lane, recall boost, placement, and activation metadata. | Basin contract proves routing cannot skip semantic prior retrieval. | Basins stay context/placement layer, not memory formation. |
| Predict-Calibrate retrieved priors are the highest-value Nemori feature. | `/Volumes/Asylum/dev/dionysus3/docs/audits/2026-05-22-nemori-feature-ranking.md:73` | `PriorMemory`, `EpisodePredictor`, and semantic-store ports remain inside Anamnesis core; host adapters only persist/project results. | End-to-end memory loop test checks prior retrieval improves next prediction before Dionysus cutover. | Do not substitute graph projection or basin routing for semantic prior search. |
| Observability and tunables are needed before claiming parity. | `/Volumes/Asylum/dev/dionysus3/docs/audits/2026-05-22-nemori-feature-ranking.md:100` | `TelemetryPort`, typed adapter errors, and host-owned metrics adapters. | Adapter failure tests assert loud typed failures and observable telemetry. | Runtime activation waits on telemetry coverage. |

## Not Implemented Here

- Real `GraphitiAdapter`
- Real `QdrantProjectionAdapter`
- Real `MemoryBasinRouterAdapter`
- Real `MemEvolveAdapter`
- Real `SakshiGateAdapter`
- EventBus, Redis, or RabbitMQ clients
- Dionysus feature flags, API routes, or runtime wiring
