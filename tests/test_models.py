from datetime import UTC, datetime

import pytest

from anamnesis_runtime import (
    ConsolidationDecision,
    ConsolidationOperation,
    MemoryType,
    NemoriMessage,
    NemoriSemanticInsight,
    Role,
)


def test_message_requires_timezone_aware_timestamp() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        NemoriMessage(
            message_id="m1",
            user_id="u1",
            agent_id="a1",
            role=Role.USER,
            content="hello",
            timestamp=datetime(2026, 5, 22),
        )


def test_semantic_insight_confidence_is_bounded() -> None:
    with pytest.raises(ValueError, match="confidence"):
        NemoriSemanticInsight(
            insight_id="i1",
            user_id="u1",
            agent_id="a1",
            content="The user prefers host-neutral libraries.",
            source_episode_id="e1",
            prediction="No known preference.",
            prediction_error_summary="Preference was newly observed.",
            confidence=1.5,
        )


def test_consolidation_decision_keeps_nemori_ownership() -> None:
    insight = NemoriSemanticInsight(
        insight_id="i1",
        user_id="u1",
        agent_id="a1",
        content="The user prefers host-neutral libraries.",
        source_episode_id="e1",
        prediction="No known preference.",
        prediction_error_summary="Preference was newly observed.",
        confidence=0.92,
        memory_type=MemoryType.SEMANTIC,
    )

    decision = ConsolidationDecision(
        operation=ConsolidationOperation.NEW,
        insight=insight,
        reason="new semantic preference",
    )

    assert decision.operation is ConsolidationOperation.NEW
    assert decision.insight.content.startswith("The user prefers")


def test_message_accepts_utc_timestamp() -> None:
    message = NemoriMessage(
        message_id="m1",
        user_id="u1",
        agent_id="a1",
        role=Role.USER,
        content="hello",
        timestamp=datetime(2026, 5, 22, tzinfo=UTC),
    )

    assert message.role is Role.USER

