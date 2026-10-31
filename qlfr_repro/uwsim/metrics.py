"""Delivery ratio, delay and energy bookkeeping."""
from dataclasses import dataclass, field


@dataclass
class Metrics:
    generated: int = 0
    delivered: set = field(default_factory=set)
    delays: list = field(default_factory=list)
    transmissions: int = 0

    def on_generate(self) -> None:
        self.generated += 1

    def on_deliver(self, pkt_id: int, delay: float) -> None:
        if pkt_id not in self.delivered:
            self.delivered.add(pkt_id)
            self.delays.append(delay)

    @property
    def pdr(self) -> float:
        return len(self.delivered) / self.generated if self.generated else 0.0

    @property
    def avg_delay(self) -> float:
        return sum(self.delays) / len(self.delays) if self.delays else float("nan")
