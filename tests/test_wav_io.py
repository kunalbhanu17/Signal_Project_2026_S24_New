import numpy as np

from src.common.wav_io import from_wav_bytes, to_wav_bytes
from src.generator import waveforms


def test_wav_round_trip_preserves_shape_and_frequency():
    sample_rate = 8000
    signal = waveforms.sine(440, 1.0, sample_rate, amplitude=0.5)

    wav_bytes = to_wav_bytes(signal, sample_rate)
    decoded, decoded_rate = from_wav_bytes(wav_bytes)

    assert decoded_rate == sample_rate
    assert len(decoded) == len(signal)
    # 16-bit PCM quantization introduces small error — correlation should still be near 1.
    correlation = np.corrcoef(signal, decoded)[0, 1]
    assert correlation > 0.999


def test_wav_round_trip_clips_out_of_range_amplitude():
    signal = np.array([-2.0, 0.0, 2.0])
    decoded, _ = from_wav_bytes(to_wav_bytes(signal, 8000))
    assert np.max(decoded) <= 1.0
    assert np.min(decoded) >= -1.0
