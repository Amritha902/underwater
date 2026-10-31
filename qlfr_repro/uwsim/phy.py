"""Link-level reception model: SNR from Thorp path loss and ambient noise, BPSK bit errors."""
import math
from .channel import path_loss_db


def snr_db(distance_m: float, source_level_db: float, noise_level_db: float, f_khz: float, k: float = 1.5) -> float:
    return source_level_db - path_loss_db(distance_m, f_khz, k) - noise_level_db


def packet_success_prob(distance_m: float, bits: int, source_level_db: float, noise_level_db: float, f_khz: float) -> float:
    """P(packet received) = (1 - BER)^bits with BPSK BER = 0.5 * erfc(sqrt(SNR))."""
    snr = 10 ** (snr_db(distance_m, source_level_db, noise_level_db, f_khz) / 10)
    ber = 0.5 * math.erfc(math.sqrt(max(snr, 0.0)))
    return (1 - ber) ** bits
