"""Nemori predict-calibrate components."""

from __future__ import annotations

from collections.abc import Sequence

from anamnesis_runtime.models import (
    MemoryType,
    NemoriEpisode,
    NemoriRawEpisode,
    NemoriSemanticInsight,
    Prediction,
    PriorMemory,
)


def _message_texts(raw_episode: NemoriRawEpisode) -> tuple[str, ...]:
    texts: list[str] = []
    for message in raw_episode.messages:
        if isinstance(message.content, str):
            texts.append(message.content)
        else:
            texts.append(" ".join(part.text or "" for part in message.content).strip())
    return tuple(text for text in texts if text)


class PriorAwarePredictor:
    """Predict from episode cue plus retrieved semantic priors."""

    async def predict(self, episode: NemoriEpisode, priors: Sequence[PriorMemory]) -> Prediction:
        prior_summary = "; ".join(prior.content for prior in priors) or "no semantic priors"
        return Prediction(
            content=(
                f"Given {episode.cue!r} and {prior_summary}, "
                "predict the expected memory delta."
            ),
            priors=tuple(priors),
            metadata={"prior_ids": tuple(prior.prior_id for prior in priors)},
        )


class RawEpisodePredictionErrorDistiller:
    """Distill semantic insight by comparing prediction against raw source messages."""

    async def distill(
        self, raw_episode: NemoriRawEpisode, episode: NemoriEpisode, prediction: Prediction
    ) -> tuple[NemoriSemanticInsight, ...]:
        raw_text = " ".join(_message_texts(raw_episode)).strip()
        if not raw_text:
            return ()

        return (
            NemoriSemanticInsight(
                insight_id=f"insight:{episode.episode_id}",
                user_id=episode.user_id,
                agent_id=episode.agent_id,
                content=f"{episode.cue}: {raw_text}",
                source_episode_id=episode.episode_id,
                prediction=prediction.content,
                prediction_error_summary=self._prediction_error_summary(raw_episode),
                confidence=0.75 if prediction.priors else 0.6,
                memory_type=MemoryType.SEMANTIC,
            ),
        )

    def _prediction_error_summary(self, raw_episode: NemoriRawEpisode) -> str:
        return (
            "Compared prediction against "
            f"{len(raw_episode.messages)} raw source message(s)."
        )
