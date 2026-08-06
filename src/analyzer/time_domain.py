"""Time-domain analysis helpers."""
import numpy as np


def time_vector(signal: np.ndarray, sample_rate: int) -> np.ndarray:
    return np.arange(len(signal)) / sample_rate


def rms(signal: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(signal))))


def peak_to_peak(signal: np.ndarray) -> float:
    return float(np.max(signal) - np.min(signal))
