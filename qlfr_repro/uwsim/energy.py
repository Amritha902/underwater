"""Per-node battery accounting."""
from dataclasses import dataclass


@dataclass
class Battery:
    initial_j: float
    tx_power_w: float
    rx_power_w: float
    idle_power_w: float = 0.0
    residual_j: float = None

    def __post_init__(self):
        if self.residual_j is None:
            self.residual_j = self.initial_j

    @property
    def alive(self) -> bool:
        return self.residual_j > 0

    def _draw(self, joules: float) -> None:
        self.residual_j = max(0.0, self.residual_j - joules)

    def transmit(self, duration_s: float) -> None:
        self._draw(self.tx_power_w * duration_s)

    def receive(self, duration_s: float) -> None:
        self._draw(self.rx_power_w * duration_s)

    def idle(self, duration_s: float) -> None:
        self._draw(self.idle_power_w * duration_s)
