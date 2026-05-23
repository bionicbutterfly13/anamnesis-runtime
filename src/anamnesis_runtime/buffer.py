"""Message buffer implementations."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Sequence

from anamnesis_runtime.models import NemoriMessage


class InMemoryMessageBuffer:
    """Simple offline buffer for tests and local experiments."""

    def __init__(self) -> None:
        self._messages: dict[str, list[NemoriMessage]] = defaultdict(list)

    async def add(self, user_id: str, messages: Sequence[NemoriMessage]) -> None:
        self._messages[user_id].extend(messages)

    async def pop(self, user_id: str) -> tuple[NemoriMessage, ...]:
        messages = tuple(self._messages.pop(user_id, []))
        return messages

