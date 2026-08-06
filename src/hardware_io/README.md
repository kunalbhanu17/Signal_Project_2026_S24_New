# src/hardware_io — owned by Person C

Audio I/O boundary — the one place the app touches real hardware (sound
card playback/recording via `sounddevice`). Keeping this isolated means
`src/generator` and `src/analyzer` stay pure/testable without a sound
device attached, and it gives a single seam to extend to other hardware
(e.g. serial/ADC input) later without touching the DSP code.

## Scope
- Play a numpy waveform through the speakers
- Record a numpy array from the microphone
- (Future) abstract input source so a non-audio hardware signal (e.g. a
  serial-connected ADC) can feed the same analyzer pipeline

## Working on this module
Branch: `feature/app-hardware`. This person also owns `app/` (the
Streamlit integration layer that wires `src/generator` + `src/analyzer` +
`src/hardware_io` together), since app integration and hardware I/O tend
to land together. Land changes in `src/hardware_io/*.py`, `app/*.py`, and
matching tests in `tests/test_hardware_io.py`.
