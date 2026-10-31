"""Underwater acoustic channel: Thorp absorption, spreading loss, propagation delay."""
import math

SOUND_SPEED = 1500.0  # m/s, nominal


def thorp_absorption_db_per_km(f_khz: float) -> float:
    """Thorp's empirical absorption coefficient a(f) in dB/km, f in kHz."""
    f2 = f_khz * f_khz
    return 0.11 * f2 / (1 + f2) + 44 * f2 / (4100 + f2) + 2.75e-4 * f2 + 0.003


def path_loss_db(distance_m: float, f_khz: float, k: float = 1.5) -> float:
    """Attenuation A(l, f) in dB: 10*k*log10(l) + l*a(f), with l in metres for spreading, km for absorption."""
    if distance_m <= 0:
        return 0.0
    return 10 * k * math.log10(distance_m) + (distance_m / 1000.0) * thorp_absorption_db_per_km(f_khz)


def propagation_delay(distance_m: float, speed: float = SOUND_SPEED) -> float:
    return distance_m / speed
