import numpy as np

from src.analyzer import freq_domain, stft, time_domain
from src.generator import waveforms


def test_fft_finds_peak_at_signal_frequency():
    sample_rate = 8000
    signal = waveforms.sine(440, 1.0, sample_rate)
    freqs, magnitude = freq_domain.fft_spectrum(signal, sample_rate)
    peak_freq = freqs[np.argmax(magnitude)]
    assert abs(peak_freq - 440) < 2


def test_rms_of_unit_sine_is_about_0_707():
    signal = waveforms.sine(440, 1.0, 8000, amplitude=1.0)
    assert abs(time_domain.rms(signal) - 0.7071) < 0.01


def test_stft_shape():
    signal = waveforms.sine(440, 1.0, 8000)
    freqs, times, mag = stft.stft_spectrogram(signal, 8000, nperseg=256)
    assert mag.shape == (len(freqs), len(times))
