"""Simulation parameters. Values are documented assumptions, not taken from the QLFR paper (full text unavailable)."""
from dataclasses import dataclass


@dataclass
class Config:
    area_xyz: tuple = (1000.0, 1000.0, 1000.0)   # m
    n_sinks: int = 9
    comm_range: float = 250.0                    # m
    f_khz: float = 25.0
    source_level_db: float = 95.0                # chosen so success prob falls from ~0.98 at 200 m to ~0.7 at 250 m
    noise_level_db: float = 50.0
    packet_bits: int = 800
    bit_rate: float = 16000.0                    # bit/s
    tx_power_w: float = 2.0
    rx_power_w: float = 0.1
    initial_energy_j: float = 100.0
    max_hold_s: float = 0.5                      # upper bound of holding time window
    retx_limit: int = 2
    # Q-learning
    alpha: float = 0.5                           # learning rate
    gamma: float = 0.9                           # discount
    w_depth: float = 1.0                         # depth-progress reward weight
    w_energy: float = 1.0                        # residual-energy reward weight
    hop_cost: float = 1.0
    fail_penalty: float = 2.0
    void_penalty: float = 3.0                    # DQ-EVDR only
    sink_value: float = 5.0                      # value of reaching a sink
    n_candidates: int = 3                        # forwarding-candidate set size (anypath)
    # DBR / VBF
    dbr_depth_threshold: float = 0.0
    vbf_pipe_radius: float = 150.0

    @property
    def packet_time(self) -> float:
        return self.packet_bits / self.bit_rate
