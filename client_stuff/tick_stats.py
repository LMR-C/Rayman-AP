import logging
import time

logger = logging.getLogger("RaymanClient")
# logger.setLevel(logging.DEBUG)  # uncomment when debug logs are needed


class TickStats:
    """Timing of the BizHawk calls, logged as a summary to keep the log file readable."""

    SUMMARY_PERIOD_S = 30.0
    SLOW_TICK_S = 0.25

    def __init__(self) -> None:
        self.durations: dict[str, list[float]] = {}
        self.last_summary = time.perf_counter()

    def end_tick(self, tick: dict[str, float]) -> None:
        """Record the durations of one tick. Warns if it was slow, and logs the summary when it is due.

        Args:
            tick: Duration in seconds of each BizHawk call of the tick, by name.
        """
        for name, duration in tick.items():
            self.durations.setdefault(name, []).append(duration)

        total = sum(tick.values())
        if total > self.SLOW_TICK_S:
            detail = ", ".join(f"{name}={value * 1000:.0f}ms" for name, value in tick.items())
            logger.warning(f"Slow tick: {total * 1000:.0f}ms ({detail})")

        now = time.perf_counter()
        if now - self.last_summary >= self.SUMMARY_PERIOD_S:
            parts = [f"{name}: avg={sum(values) / len(values) * 1000:.1f}ms "
                     f"max={max(values) * 1000:.1f}ms n={len(values)}"
                     for name, values in self.durations.items()]
            logger.info("Timings | " + " | ".join(parts))
            self.durations.clear()
            self.last_summary = now
