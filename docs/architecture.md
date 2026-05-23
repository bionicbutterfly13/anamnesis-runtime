# Architecture

Anamnesis is a memory runtime kernel. It exposes records and ports that a host
application can wire to its own persistence, LLM, vector, graph, and event
systems.

## Ownership

| Layer | Owned here | Owned by host |
| --- | --- | --- |
| Message buffer | Interface and in-memory implementation | Durable queues or event logs |
| Episode formation | Raw and narrative episode records, partition/generation ports | Host source adapters |
| Predict-calibrate | Prior retrieval contract, prediction, distillation, consolidation | LLM provider selection and policy |
| Recall | Unified recall result shape | API routes, dashboards, auth |
| Persistence | Store protocols and test stores | Graphiti, Qdrant, Postgres, Neo4j, EventBus |
| Events/gates/telemetry | Neutral records and ports | EventBus, Redis, RabbitMQ, Sakshi, observability backends |

## Runtime Flow

```text
messages
  -> buffer
  -> partition raw episodes
  -> generate narrative episodes
  -> retrieve semantic priors
  -> predict episode
  -> distill prediction error into semantic insights
  -> consolidate new / merge / conflict
  -> recall episodic + semantic memory
```

## Strategy Boundary

`NemoriStrategy` is the first built-in strategy. It composes the core runtime
with host-neutral components for message-count segmentation, narrative episode
generation, prior-aware prediction, raw-episode prediction-error distillation,
and semantic consolidation.

The strategy does not own host persistence, graph memory, vector projection,
transport, gates, or application policy. Those remain adapter concerns.

## Transport Boundary

Core event support is limited to `MemoryEvent`, serialization helpers,
publisher/subscriber protocols, namespace wildcard matching, and
`InMemoryEventTransport` for local tests. EventBus, Redis Streams, and RabbitMQ
bridges should live as optional extras or separate adapter packages so the core
runtime stays standard-library-only.

## Dionysus Adapter Boundary

Anamnesis exposes neutral adapter contracts for host-owned integration code:

- `GraphMutationPort` accepts `GraphMutation` records for durable graph intent.
- `ProjectionPort` accepts `ProjectionPayload` records for vector projection.
- `RoutingPort` accepts `RoutingRequest` and returns `RoutingDecision`.
- `EvolutionPort` accepts `EvolutionRequest` and returns `EvolutionResult`.
- `GatePort` remains the canonical witness/write-guard contract.
- `EventBridgePort` composes neutral memory event publishing and subscription.

Real Dionysus adapters should live in Dionysus or an optional integration
package. They must translate these contracts to Graphiti, Qdrant,
MemoryBasinRouter, MemEvolve, Sakshi, EventBus, Redis Streams, or RabbitMQ
without adding those imports to Anamnesis core.

## Non-goals

- No direct Dionysus imports.
- No direct Graphiti, Qdrant, Neo4j, or EventBus imports.
- No Elume, Autonoesis, or Sakshi ownership of memory formation.
- No LinOSS ownership of memory formation.
- No concrete Redis or RabbitMQ transport in core.
- No production activation policy.
