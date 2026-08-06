# src/analyzer — owned by Person B

Signal analysis engine. Pure functions that take a numpy array (+ sample
rate) and return data ready to plot — no Streamlit/UI code here.

## Scope (from SP24 brief)
- Time-domain view (pass-through / windowing helpers)
- Frequency-domain view (FFT magnitude/phase spectrum)
- STFT (spectrogram) view

## Interface contract
```python
def fft_spectrum(signal: np.ndarray, sample_rate: int) -> tuple[np.ndarray, np.ndarray]:
    """Returns (freqs_hz, magnitude)."""

def stft_spectrogram(signal: np.ndarray, sample_rate: int, ...) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Returns (freqs_hz, times_s, magnitude_2d)."""
```

## Working on this module
Branch: `feature/analyzer`. Land changes in `src/analyzer/*.py` and
matching tests in `tests/test_analyzer.py`. Consume waveforms from
`src/generator` only through its public functions — don't reach into its
internals. Avoid touching `src/generator/`, `src/hardware_io/`, or `app/`
unless coordinating with the other two owners.
