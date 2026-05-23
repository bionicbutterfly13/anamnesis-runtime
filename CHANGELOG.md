# Changelog

All notable changes to Anamnesis Runtime will be documented here.

This project has not been published to PyPI yet.

## 0.1.0 - Unreleased

### Added

- Core host-neutral memory records, ports, runtime wrapper, and in-memory stores.
- Nemori as the first built-in host-neutral memory strategy.
- Neutral memory event contracts, serialization helpers, wildcard matching, and
  in-process event transport for tests and local experiments.
- Dionysus adapter boundary contracts for graph mutation, vector projection,
  basin routing, memory-process evolution, gate compatibility, and event bridges.
- Spec Kit planning artifacts for core runtime, Nemori strategy, event
  transports, and Dionysus adapter migration.

### Not Included

- Real Dionysus, Graphiti, Qdrant, MemoryBasinRouter, MemEvolve, Sakshi,
  EventBus, Redis, RabbitMQ, FastAPI, Elume, Autonoesis, or LinOSS adapters.
- PyPI publication.
- Runtime activation inside Dionysus.
