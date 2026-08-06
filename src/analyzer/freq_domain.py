"""Frequency-domain analysis (FFT) helpers."""
import numpy as np


def fft_spectrum(signal: np.ndarray, sample_rate: int) -> tuple[np.ndarray, np.ndarray]:
    """Returns (freqs_hz, magnitude) for the positive-frequency half of the FFT."""
    n = len(signal)
    spectrum = np.fft.rfft(signal)
    freqs = np.fft.rfftfreq(n, d=1.0 / sample_rate)
    magnitude = np.abs(spectrum) / n
    return freqs, magnitude
