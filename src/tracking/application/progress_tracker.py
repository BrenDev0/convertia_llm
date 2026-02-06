from src.tracking.domain.entites import ProgressStage


class ProgressTracker:
    def __init__(
        self,
        stage: ProgressStage,
        total_steps: int,
        publish_every: int = 1
    ):
        if total_steps <= 0:
            raise ValueError("total_steps must be > 0")

        if stage.start >= stage.end:
            raise ValueError("stage.start must be < stage.end")

        self._stage = stage
        self._total = total_steps
        self._completed = 0
        self._publish_every = publish_every

    def step(self) -> int:
        if self._completed >= self._total:
            return self._stage.end

        self._completed += 1

        span = self._stage.end - self._stage.start
        progress = self._stage.start + (self._completed / self._total) * span

        return int(progress)

    def should_publish(self) -> bool:
        return (
            self._completed == 1 or
            self._completed % self._publish_every == 0 or
            self._completed == self._total
        )

    def is_done(self) -> bool:
        return self._completed >= self._total
