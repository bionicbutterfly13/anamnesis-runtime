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

## Non-goals

- No direct Dionysus imports.
- No direct Graphiti, Qdrant, Neo4j, or EventBus imports.
- No Elume, Autonoesis, or Sakshi ownership of memory formation.
- No LinOSS ownership of memory formation.
- No production activation policy.
