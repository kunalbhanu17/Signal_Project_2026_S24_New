# Test fixtures

## windowing_demo_440.5Hz.wav

A 1-second, 44100 Hz, 0.8-amplitude sine tone at **440.5 Hz** — deliberately
off an FFT bin (bin spacing is `sample_rate / duration` = 1 Hz at these
settings, so any integer frequency lands exactly on a bin and shows almost
no leakage regardless of window). At 440.5 Hz, rectangular windowing leaks
visibly into neighboring bins, which is what makes the Hann/Hamming
comparison worth watching in the demo video.

Generated with:

```python
from src.generator.waveforms import sine
from src.common.wav_io import to_wav_bytes

signal = sine(440.5, 1.0, 44100, amplitude=0.8)
open("windowing_demo_440.5Hz.wav", "wb").write(to_wav_bytes(signal, 44100))
```

Measured with `freq_domain.fft_spectrum` (dB level 20 Hz off the 440.5 Hz
peak — lower means less leakage):

| Window      | dB @ 20 Hz off-peak |
|-------------|---------------------|
| rectangular | -32.0 dB            |
| hann        | -85.9 dB            |
| hamming     | -50.9 dB            |

Used by `tests/e2e/test_demo.py` to demonstrate the FFT windowing effect on
the Analyzer page (uploaded via the file uploader, then compared across all
three window options) — both for the automated assertions and the video
demo captions.
