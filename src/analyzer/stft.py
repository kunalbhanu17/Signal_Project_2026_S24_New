"""Short-Time Fourier Transform (spectrogram) helpers."""
import numpy as np
from scipy.signal import stft


def stft_spectrogram(signal: np.ndarray, sample_rate: int, nperseg: int = 256
                      ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Returns (freqs_hz, times_s, magnitude_2d)."""
    freqs, times, z = stft(signal, fs=sample_rate, nperseg=nperseg)
    return freqs, times, np.abs(z)
