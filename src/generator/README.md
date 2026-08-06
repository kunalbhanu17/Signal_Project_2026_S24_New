# src/generator — owned by Person A

Waveform synthesis engine. Pure functions that take frequency, duration,
sample rate, amplitude, duty cycle, etc. and return numpy arrays — no
Streamlit/UI code here, no audio playback here (that lives in
`src/hardware_io`).

## Scope (from SP24 brief)
- Square wave (with duty cycle)
- Sine wave
- Triangular wave
- Chirp (linear/log sweep)
- Sinc pulse

## Interface contract
Every waveform function should follow the same signature shape so
`app/pages/1_Generator.py` and `src/analyzer` can treat them uniformly:

```python
def square(freq_hz: float, duration_s: float, sample_rate: int,
           amplitude: float = 1.0, duty_cycle: float = 0.5) -> np.ndarray:
    ...
```

Returns a 1-D numpy array of samples in [-amplitude, amplitude].

## Working on this module
Branch: `feature/generator`. Land changes in `src/generator/waveforms.py`
and matching tests in `tests/test_generator.py`. Avoid touching
`src/analyzer/`, `src/hardware_io/`, or `app/` unless coordinating with the
other two owners — those are the likely merge-conflict zones.
