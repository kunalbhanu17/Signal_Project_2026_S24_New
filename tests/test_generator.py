import numpy as np

from src.generator import waveforms


def test_sine_amplitude_bounds():
    signal = waveforms.sine(440, 1.0, 8000, amplitude=0.5)
    assert np.max(signal) <= 0.5 + 1e-9
    assert np.min(signal) >= -0.5 - 1e-9


def test_square_duty_cycle():
    signal = waveforms.square(1, 1.0, 8000, duty_cycle=0.5)
    assert np.isclose(np.mean(signal > 0), 0.5, atol=0.05)


def test_chirp_length():
    signal = waveforms.chirp(100, 1000, 2.0, 8000)
    assert len(signal) == 16000
