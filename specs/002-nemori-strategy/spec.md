# Feature Specification: Nemori Strategy

**Feature Directory**: `specs/002-nemori-strategy`  
**Status**: Planning artifact only  
**Created**: 2026-05-23

## Summary

Nemori is Anamnesis Runtime's first concrete memory strategy. It implements the episodic-semantic pipeline described by the Nemori paper while staying host-neutral:

```text
buffer -> segment -> episode -> semantic priors -> predict-calibrate
-> semantic consolidation -> recall
```

Anamnesis remains broader than Nemori. Nemori is a strategy inside the package, not the package identity.

## User Scenarios & Testing

### User Story 1 - Run Nemori in any cyclic host

As a cyclic agent runtime, I want to send observations, actions, reflections, and outcomes into Anamnesis so Nemori can form useful memory without knowing my host framework.

### User Story 2 - Build episodes from buffered activity

As a memory strategy, Nemori needs to buffer raw events, segment them into coherent spans, and generate durable episodes with provenance and boundaries.

### User Story 3 - Retrieve semantic priors before prediction

As an agent loop, I want Nemori to retrieve relevant semantic priors before prediction so memory updates are driven by prediction error instead of direct importance scoring.

### User Story 4 - Predict and calibrate outcomes

As a long-running agent, I want Nemori to compare predictions against raw source episodes and produce reusable semantic deltas.

### User Story 5 - Consolidate and recall context

As a host, I want to query Nemori for relevant episodes, semantic insights, predictions, and calibration history through stable runtime contracts.

## Requirements

- FR-001: Nemori MUST accept buffered input through Anamnesis core contracts.
- FR-002: Nemori MUST segment buffered events into coherent candidate episodes through an injected or deterministic segmentation policy.
- FR-003: Nemori MUST generate episodes with stable IDs, timestamps, source references, boundary reasons, cue/title, narrative, and provenance.
- FR-004: Nemori MUST retrieve semantic priors through an abstract retrieval port before prediction.
- FR-005: Nemori MUST record predictions with basis priors and confidence metadata.
- FR-006: Nemori MUST distill semantic insights by comparing prediction against raw episode source data.
- FR-007: Nemori MUST consolidate repeated or high-value episode patterns into semantic records with traceability.
- FR-008: Nemori MUST support recall across episodic and semantic memory.
- FR-009: Nemori MUST run without Dionysus, Graphiti, Qdrant, EventBus, Redis, RabbitMQ, Elume, Autonoesis, Sakshi, or LinOSS.
- FR-010: Host adapters MUST remain outside Anamnesis core and depend inward on strategy contracts.

## Success Criteria

- SC-001: Nemori strategy tests prove priors are retrieved before prediction.
- SC-002: Nemori strategy tests prove calibration compares predictions against raw source episodes.
- SC-003: Import-boundary tests prove no forbidden host dependency in strategy modules.
- SC-004: Strategy docs map the implementation to the Dionysus Spec 699 extraction plan without importing Dionysus code.

## Out of Scope

- Dionysus adapter implementation.
- Graphiti/Qdrant persistence.
- Redis/RabbitMQ/EventBus transports.
- LoCoMo benchmark harness.
- Production activation.

