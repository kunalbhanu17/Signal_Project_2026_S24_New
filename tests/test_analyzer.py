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


def test_to_db_peak_is_zero_and_floor_is_respected():
    magnitude = np.array([0.001, 1.0, 0.5])
    db = freq_domain.to_db(magnitude, floor_db=-40.0)
    assert np.isclose(db[1], 0.0)
    assert np.all(db >= -40.0)


def test_hann_window_reduces_spectral_leakage_vs_rectangular():
    # A non-integer number of cycles fit in the window, so a rectangular
    # window leaks energy into neighboring bins; Hann leaks less there.
    sample_rate = 8000
    signal = waveforms.sine(437.5, 1.0, sample_rate)
    freqs, mag_rect = freq_domain.fft_spectrum(signal, sample_rate, "rectangular")
    _, mag_hann = freq_domain.fft_spectrum(signal, sample_rate, "hann")
    bin_far_from_peak = np.argmin(np.abs(freqs - 800))
    assert mag_hann[bin_far_from_peak] < mag_rect[bin_far_from_peak]


def test_fft_windows_all_match_rectangular_shape():
    sample_rate = 8000
    signal = waveforms.sine(440, 1.0, sample_rate)
    for window in freq_domain.WINDOWS:
        freqs, magnitude = freq_domain.fft_spectrum(signal, sample_rate, window)
        assert freqs.shape == magnitude.shape


def test_leakage_db_ranks_windows_rectangular_worst_hann_best():
    # Off-bin tone (see tests/e2e/fixtures/README.md for the same setup).
    sample_rate = 44100
    signal = waveforms.sine(440.5, 1.0, sample_rate)
    leakage = {}
    for window in freq_domain.WINDOWS:
        freqs, magnitude = freq_domain.fft_spectrum(signal, sample_rate, window)
        leakage[window] = freq_domain.leakage_db(freqs, magnitude)
    assert leakage["hann"] < leakage["hamming"] < leakage["rectangular"]


def test_window_curve_shapes():
    n = 100
    assert np.allclose(freq_domain.window_curve(n, "rectangular"), 1.0)
    for window in ["hann", "hamming"]:
        curve = freq_domain.window_curve(n, window)
        assert len(curve) == n
        assert curve[0] < curve[n // 2]  # tapered at the edges, peak in the middle
