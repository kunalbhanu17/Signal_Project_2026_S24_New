"""Waveform synthesis engine — see README.md for the interface contract."""
import numpy as np


def _time_vector(duration_s: float, sample_rate: int) -> np.ndarray:
    n_samples = int(duration_s * sample_rate)
    return np.arange(n_samples) / sample_rate


def sine(freq_hz: float, duration_s: float, sample_rate: int,
         amplitude: float = 1.0) -> np.ndarray:
    t = _time_vector(duration_s, sample_rate)
    return amplitude * np.sin(2 * np.pi * freq_hz * t)


def square(freq_hz: float, duration_s: float, sample_rate: int,
           amplitude: float = 1.0, duty_cycle: float = 0.5) -> np.ndarray:
    t = _time_vector(duration_s, sample_rate)
    phase = (freq_hz * t) % 1.0
    return amplitude * np.where(phase < duty_cycle, 1.0, -1.0)


def triangular(freq_hz: float, duration_s: float, sample_rate: int,
               amplitude: float = 1.0) -> np.ndarray:
    t = _time_vector(duration_s, sample_rate)
    phase = (freq_hz * t) % 1.0
    return amplitude * (2 * np.abs(2 * (phase - np.floor(phase + 0.5))) - 1)


def chirp(f0_hz: float, f1_hz: float, duration_s: float, sample_rate: int,
          amplitude: float = 1.0) -> np.ndarray:
    t = _time_vector(duration_s, sample_rate)
    k = (f1_hz - f0_hz) / duration_s
    phase = 2 * np.pi * (f0_hz * t + 0.5 * k * t ** 2)
    return amplitude * np.sin(phase)


def sinc_pulse(freq_hz: float, duration_s: float, sample_rate: int,
               amplitude: float = 1.0) -> np.ndarray:
    t = _time_vector(duration_s, sample_rate) - duration_s / 2
    return amplitude * np.sinc(2 * freq_hz * t)
