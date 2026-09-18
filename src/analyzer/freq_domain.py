"""Frequency-domain analysis (FFT) helpers."""
import numpy as np
from scipy.signal import get_window

WINDOWS = {"rectangular": "boxcar", "hann": "hann", "hamming": "hamming"}


def fft_spectrum(signal: np.ndarray, sample_rate: int, window: str = "rectangular"
                  ) -> tuple[np.ndarray, np.ndarray]:
    """Returns (freqs_hz, magnitude) for the positive-frequency half of the FFT.

    `window` is one of WINDOWS' keys. Magnitude is normalized by the window's
    coherent gain (sum of its samples), so "rectangular" matches the
    unwindowed result exactly.
    """
    n = len(signal)
    win = get_window(WINDOWS[window], n)
    spectrum = np.fft.rfft(signal * win)
    freqs = np.fft.rfftfreq(n, d=1.0 / sample_rate)
    magnitude = np.abs(spectrum) / np.sum(win)
    return freqs, magnitude


def to_db(magnitude: np.ndarray, floor_db: float = -100.0) -> np.ndarray:
    """Converts a magnitude array/2D array to dB, relative to its own peak."""
    peak = np.max(magnitude)
    ref = peak if peak > 0 else 1.0
    db = 20 * np.log10(np.maximum(magnitude, 1e-12) / ref)
    return np.maximum(db, floor_db)
