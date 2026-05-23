# Contract: Memory Events and Transports

## MemoryEvent

Fields:

- `event_id`: stable event identifier
- `event_type`: namespaced event type
- `schema_version`: event payload contract version
- `occurred_at`: timezone-aware timestamp
- `source`: emitting component
- `correlation_id`: optional workflow trace identifier
- `causation_id`: optional parent event identifier
- `payload`: structured event data
- `metadata`: optional diagnostics/context

## Suggested Event Types

- `memory.message_ingested`
- `memory.raw_episode_created`
- `memory.episode_created`
- `memory.priors_retrieved`
- `memory.prediction_created`
- `memory.semantic_insight_distilled`
- `memory.consolidation_decided`
- `memory.consolidation_routed`
- `memory.recall_requested`
- `memory.recall_returned`
- `memory.write_blocked`
- `memory.write_quarantined`

## Publisher Port

Accepts a `MemoryEvent`, validates required fields, and delegates delivery.

## Subscriber Port

Registers handlers by event type or pattern and invokes handlers with decoded `MemoryEvent` objects.

