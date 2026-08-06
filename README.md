# Signal Generator & Analyzer (SP24)

A DSP course project (BS-ES Signal Processing, 2026): a Streamlit web app
with (1) an audio waveform generator — square, sine, triangular, chirp,
sinc, with configurable frequency/duty-cycle/amplitude — and (2) a signal
analyzer that plots time-domain, frequency-domain (FFT), and STFT views of
a signal.

**Features:**
- Generate any of the 5 waveform types, listen to it in-browser, and
  download it as a WAV file.
- Analyze the last generated signal, *or* upload your own WAV file to
  analyze (time domain, FFT magnitude in dB, STFT spectrogram with
  colorbar).
- Optional local-only page to play/record through your machine's sound
  card via `sounddevice` (works when run locally; browser audio on the
  Generator page works everywhere, including a hosted deployment).

See `documentation/key_decisions.txt` for why this stack was chosen, and
`TASKS.md` for the task breakdown across the team and course deadline.

## Project layout

```
src/generator/    waveform synthesis (pure functions, no UI)     — owner A
src/analyzer/      time/frequency/STFT analysis (pure functions)  — owner B
src/hardware_io/   sound card I/O (the only module touching real
                    hardware) + app/ integration layer             — owner C
src/common/        wav_io.py — WAV encode/decode shared by Generator/Analyzer
app/               Streamlit UI, wires the three modules together
tests/             pytest tests, mirrors the src/ layout, plus
                    test_app_smoke.py (exercises the real multipage app
                    via streamlit.testing.v1.AppTest)
documentation/     decisions log, proposal, course FAQ reference
report/            final report + video demo (per course submission format)
```

Each `src/*` module has its own `README.md` describing its scope and
interface contract — read that before touching a module you don't own.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/Home.py
```

## Tests

```bash
pytest
```

## Working as a team of 3

See `CONTRIBUTING.md` for the branch-per-module workflow that lets three
people (each running their own Claude Code agent) work simultaneously
without stepping on each other's files.
