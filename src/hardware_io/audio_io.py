"""Audio hardware I/O — the only module that talks to sounddevice."""
import numpy as np
import sounddevice as sd


def play(signal: np.ndarray, sample_rate: int, blocking: bool = True) -> None:
    sd.play(signal, samplerate=sample_rate)
    if blocking:
        sd.wait()


def record(duration_s: float, sample_rate: int, channels: int = 1) -> np.ndarray:
    audio = sd.rec(int(duration_s * sample_rate), samplerate=sample_rate,
                    channels=channels)
    sd.wait()
    return audio.flatten()
