# Contract: Core Memory Runtime

## Public Runtime

```python
class MemoryRuntime:
    async def add_messages(self, user_id: str, messages: Sequence[NemoriMessage]) -> None: ...
    async def flush(self, user_id: str) -> tuple[NemoriEpisode, ...]: ...
    async def search(self, user_id: str, query: str, *, top_k: int = 10) -> NemoriRecallResult: ...
    async def health(self) -> dict[str, str]: ...
    async def stats(self) -> dict[str, int]: ...
```

## Required Lifecycle Order

1. Buffer messages.
2. Partition buffered messages into raw episodes.
3. Generate narrative episodes.
4. Store narrative episodes.
5. Retrieve semantic priors.
6. Predict from episode + priors.
7. Distill prediction error from raw episode + prediction.
8. Consolidate semantic insights.
9. Apply consolidation decisions.
10. Route/annotate through optional host-neutral ports.

## Import Boundary

Core modules MUST NOT import:

- Dionysus or `api.*`
- Graphiti
- Qdrant
- Redis
- RabbitMQ / pika / aio-pika
- EventBus host modules
- FastAPI
- Elume
- Autonoesis
- Sakshi
- LinOSS

Adapters may depend on these packages outside core.

