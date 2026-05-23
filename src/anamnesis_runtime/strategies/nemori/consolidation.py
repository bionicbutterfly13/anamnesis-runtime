"""Nemori semantic consolidation components."""

from __future__ import annotations

from collections.abc import Sequence

from anamnesis_runtime.models import (
    ConsolidationDecision,
    ConsolidationOperation,
    NemoriSemanticInsight,
)


class NemoriSemanticConsolidator:
    """Default host-neutral consolidator.

    It records each distilled insight as a new semantic memory. Merge/conflict
    policy stays injectable so hosts can add richer behavior later without
    changing the strategy contract.
    """

    async def consolidate(
        self, insights: Sequence[NemoriSemanticInsight]
    ) -> tuple[ConsolidationDecision, ...]:
        return tuple(
            ConsolidationDecision(
                operation=ConsolidationOperation.NEW,
                insight=insight,
                reason="nemori-default-new",
            )
            for insight in insights
        )

