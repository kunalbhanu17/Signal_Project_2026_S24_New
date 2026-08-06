# Signal Generator & Analyzer (SP24)

A DSP course project (BS-ES Signal Processing, 2026): a Streamlit web app
with (1) an audio waveform generator — square, sine, triangular, chirp,
sinc, with configurable frequency/duty-cycle/amplitude — and (2) a signal
analyzer that plots time-domain, frequency-domain (FFT), and STFT views of
a signal, plus optional live playback/recording through the sound card.

See `documentation/key_decisions.txt` for why this stack was chosen, and
`TASKS.md` for the task breakdown across the team and course deadline.

## Project layout

```
src/generator/    waveform synthesis (pure functions, no UI)     — owner A
src/analyzer/      time/frequency/STFT analysis (pure functions)  — owner B
src/hardware_io/   sound card I/O (the only module touching real
                    hardware) + app/ integration layer             — owner C
app/               Streamlit UI, wires the three modules together
tests/             pytest tests, mirrors the src/ layout
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
