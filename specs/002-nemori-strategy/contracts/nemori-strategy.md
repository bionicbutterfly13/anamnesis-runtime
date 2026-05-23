# Contract: Nemori Strategy

## Strategy Surface

```python
class NemoriStrategy:
    async def ingest(messages: Sequence[NemoriMessage]) -> None: ...
    async def flush() -> tuple[NemoriEpisode, ...]: ...
    async def recall(query: RecallQuery) -> NemoriRecallResult: ...
```

## Required Pipeline

1. Buffer input messages/events.
2. Segment buffered data into raw episodes.
3. Generate narrative episodes.
4. Retrieve semantic priors.
5. Predict from episode cue + priors.
6. Calibrate against raw source episode.
7. Distill semantic insights.
8. Consolidate semantic insights.
9. Return recall over episodic and semantic memory.

## Host Boundary

The strategy may define ports for LLMs, embeddings, stores, and telemetry. It must not import a concrete host.

