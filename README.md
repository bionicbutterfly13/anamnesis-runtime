# Anamnesis Runtime

Anamnesis is a host-neutral episodic-semantic memory runtime for cyclic agent
systems.

It owns the memory lifecycle:

1. Raw messages enter a buffer.
2. Messages are partitioned into raw episodes.
3. Raw episodes become narrative episodes with provenance.
4. Semantic priors are evoked before prediction.
5. Prediction error is distilled into semantic insights.
6. Semantic insights are consolidated as new, merge, or conflict decisions.
7. Recall returns episodic and semantic memory without host-specific policy.

## Package name

The exact PyPI name `anamnesis` is already registered for an unrelated package.
This project uses the publishable distribution name `anamnesis-runtime` and the
Python import package `anamnesis_runtime`.

## Boundary

This package must stay independent of Dionysus, Elume, Autonoesis, Sakshi,
LinOSS, Graphiti, Qdrant, EventBus, Redis, RabbitMQ, and host-app imports.

- Dionysus owns live runtime wiring, policy, Graphiti, Qdrant, EventBus,
  Redis/RabbitMQ bridges, and API integration.
- Elume may consume translated memory priors or assessment records.
- Autonoesis owns self-model and identity ontology.
- Sakshi owns witness, gating, and verification signals.
- LinOSS may supply optional dynamics, stability, and resonance math.

## Quickstart

```python
from anamnesis_runtime import MemoryRuntime
```

The initial skeleton provides the contracts and in-memory stores needed for
offline tests. Nemori belongs here as the first concrete memory strategy, while
production adapters should live outside this package unless they are
host-neutral.

## Core extension ports

Anamnesis core defines neutral ports for extension points that host applications
can implement without pulling host dependencies into the package:

- `MemoryEventPublisher` and `MemoryEventSubscriber` for transport-neutral
  memory events.
- `GatePort` for write/review decisions such as allow, block, quarantine, or
  manual review.
- `TelemetryPort` for runtime diagnostics that can be routed to any host
  observability system.

Concrete EventBus, Redis Streams, RabbitMQ, Graphiti, Qdrant, Sakshi, LinOSS,
MemEvolve, or Dionysus integrations belong in adapters outside the core runtime.
