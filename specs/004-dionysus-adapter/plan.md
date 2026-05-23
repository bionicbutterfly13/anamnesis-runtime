# Implementation Plan: Dionysus Adapter

**Feature**: `specs/004-dionysus-adapter/spec.md`  
**Status**: Planned adapter/migration track

## Technical Context

- Adapter code may live in a Dionysus-owned package or separate integration package.
- Anamnesis core must remain host-neutral.
- Dionysus Spec 699 is the migration map source.

## Architecture

```text
Dionysus runtime
  -> Dionysus adapter composition
      -> Anamnesis core ports
      -> GraphitiAdapter
      -> QdrantProjectionAdapter
      -> MemoryBasinRouterAdapter
      -> MemEvolveAdapter
      -> SakshiGateAdapter
      -> EventBus/Redis/RabbitMQ bridge
```

## Migration Strategy

1. Add adapter contract tests with fakes.
2. Map Dionysus Spec 699 behavior to Anamnesis ports.
3. Wire one adapter behind a feature flag.
4. Run parity tests against old call path.
5. Cut over only after parity and rollback gates pass.

## Verification

```sh
uv run --extra dev pytest tests/test_import_boundaries.py
uv run --extra dev pytest tests/test_dionysus_adapter_contracts.py
```

The actual Dionysus adapter verification belongs in Dionysus or an integration package, not Anamnesis core.

