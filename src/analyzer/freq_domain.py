"""Frequency-domain analysis (FFT) helpers."""
import numpy as np


def fft_spectrum(signal: np.ndarray, sample_rate: int) -> tuple[np.ndarray, np.ndarray]:
    """Returns (freqs_hz, magnitude) for the positive-frequency half of the FFT."""
    n = len(signal)
    spectrum = np.fft.rfft(signal)
    freqs = np.fft.rfftfreq(n, d=1.0 / sample_rate)
    magnitude = np.abs(spectrum) / n
    return freqs, magnitude


def to_db(magnitude: np.ndarray, floor_db: float = -100.0) -> np.ndarray:
    """Converts a magnitude array/2D array to dB, relative to its own peak."""
    peak = np.max(magnitude)
    ref = peak if peak > 0 else 1.0
    db = 20 * np.log10(np.maximum(magnitude, 1e-12) / ref)
    return np.maximum(db, floor_db)
