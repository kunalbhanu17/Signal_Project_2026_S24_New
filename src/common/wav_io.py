"""WAV encode/decode helpers — shared by the Generator (export) and Analyzer (import) pages."""
import io

import numpy as np
from scipy.io import wavfile


def to_wav_bytes(signal: np.ndarray, sample_rate: int) -> bytes:
    """Encodes a float signal in [-1, 1] as 16-bit PCM WAV bytes."""
    pcm16 = (np.clip(signal, -1.0, 1.0) * 32767).astype(np.int16)
    buf = io.BytesIO()
    wavfile.write(buf, sample_rate, pcm16)
    return buf.getvalue()


def from_wav_bytes(data: bytes) -> tuple[np.ndarray, int]:
    """Decodes WAV bytes to a mono float signal in [-1, 1] and its sample rate."""
    sample_rate, samples = wavfile.read(io.BytesIO(data))
    if samples.ndim > 1:
        samples = samples.mean(axis=1)
    if np.issubdtype(samples.dtype, np.integer):
        samples = samples.astype(np.float64) / np.iinfo(samples.dtype).max
    return samples.astype(np.float64), sample_rate
