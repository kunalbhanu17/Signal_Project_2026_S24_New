import numpy as np

from src.hardware_io import audio_io


def test_play_calls_sounddevice(monkeypatch):
    calls = {}
    monkeypatch.setattr(audio_io.sd, "play", lambda sig, samplerate: calls.update(
        signal=sig, samplerate=samplerate))
    monkeypatch.setattr(audio_io.sd, "wait", lambda: calls.update(waited=True))

    signal = np.zeros(10)
    audio_io.play(signal, 8000)

    assert calls["samplerate"] == 8000
    assert calls["waited"] is True


def test_record_returns_flat_array(monkeypatch):
    monkeypatch.setattr(audio_io.sd, "rec", lambda n, samplerate, channels: np.ones((n, channels)))
    monkeypatch.setattr(audio_io.sd, "wait", lambda: None)

    recorded = audio_io.record(1.0, 8000)
    assert recorded.shape == (8000,)
