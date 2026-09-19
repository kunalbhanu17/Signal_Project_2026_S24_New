# Signal Generator & Analyzer (SP24)

A DSP course project (BS-ES Signal Processing, 2026): a Streamlit web app
with (1) an audio waveform generator — square, sine, triangular, chirp,
sinc, with configurable frequency/duty-cycle/amplitude — and (2) a signal
analyzer that plots time-domain, frequency-domain (FFT), and STFT
(Short-Time Fourier Transform) views of a signal.

**Features:**
- Generate any of the 5 waveform types, listen to it in-browser, and
  download it as a WAV file.
- Analyze the last generated signal, *or* upload your own WAV file to
  analyze (time domain, FFT magnitude in dB with a selectable window —
  rectangular/Hann/Hamming, STFT spectrogram with colorbar).
- Optional local-only page to play/record through your machine's sound
  card via `sounddevice` (works when run locally; browser audio on the
  Generator page works everywhere, including a hosted deployment).

## High-level design

A single Python codebase, all execution server-side (or on your own
machine when run locally), presented through a Streamlit multipage web
UI. There's no separate frontend/backend split and no database — each
page reruns its Python top-to-bottom on every interaction (Streamlit's
execution model), holding the "current signal" in `st.session_state` so
it can pass between pages.

```
                     Streamlit UI (app/)
   Home.py  |  1_Generator.py | 2_Analyzer.py | 3_Live_Hardware.py
       |                |                |
       v                v                v
 src/generator/   src/analyzer/     src/hardware_io/
 waveforms.py     time_domain.py    audio_io.py
                  freq_domain.py
                  stft.py
       \                |                /
        \               v               /
              src/common/wav_io.py
              (WAV encode/decode)
```

**Typical session**: user sets parameters on the Generator page →
`src/generator/waveforms.py` returns a numpy float array → stored in
`st.session_state` and encoded to WAV bytes for in-browser playback /
download → user switches to the Analyzer page (or uploads a WAV directly,
bypassing the Generator) → `src/analyzer/{time_domain,freq_domain,stft}.py`
compute the three views (RMS/peak-to-peak, FFT magnitude in dB, STFT
spectrogram).

`src/hardware_io/audio_io.py` is the only module that talks to real
hardware (via `sounddevice`/PortAudio) — isolated there so the rest of
the DSP core stays pure numpy, hardware-free, and unit-testable anywhere.
It only works when the app runs on a machine with a real sound device —
see "Deploying to your own Streamlit Cloud" below for why that page
won't do anything useful once hosted.

## Code structure

```
src/generator/    waveform synthesis (pure functions, no UI)
src/analyzer/     time/frequency/STFT analysis (pure functions)
src/hardware_io/  sound card I/O — the only module touching real hardware
src/common/       wav_io.py — WAV encode/decode shared by Generator/Analyzer
app/              Streamlit UI: Home.py + pages/1_Generator.py,
                  2_Analyzer.py, 3_Live_Hardware.py — wires the src/
                  modules together, all input controls in the sidebar
tests/            pytest unit tests (mirrors src/ layout) +
                  test_app_smoke.py (drives the real multipage app via
                  streamlit.testing.v1.AppTest) +
                  tests/e2e/ (Playwright browser test, also used to
                  record the demo video — see tests/e2e/README.md)
requirements.txt  Python dependencies
packages.txt      apt-level dependency (libportaudio2, needed for
                  sounddevice's PortAudio backend on a Linux host)
```

Each `src/*` module has its own `README.md` describing its scope and
interface contract.

On GitHub, this repo also has `doc_operations/` (design rationale, viva
prep Q&A, course reference docs) and `report/` (final report + video
demo) — development-process material not included in the distributed
source archive.

## Installation

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/Home.py
```

On Linux, `sounddevice` needs the PortAudio system library — install it
first if `pip install` or the app's import fails:

```bash
sudo apt-get install libportaudio2   # Debian/Ubuntu — see packages.txt
```

## Deploying to your own Streamlit Cloud

1. Push this repository to your own GitHub account (public or private —
   either works for deployment).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in,
   then **New app**.
3. Pick your repo, branch (`main`), and set the main file path to
   `app/Home.py`.
4. Deploy. `requirements.txt` and `packages.txt` are already set up, so
   no extra configuration is needed — `packages.txt` installs
   `libportaudio2` at the OS level, which `sounddevice` needs even just
   to import successfully on a fresh container.
5. The **Live Hardware** page will load but can't actually play/record —
   `sounddevice` talks to whatever sound device the *server process* is
   running on, and a cloud container has no speaker/microphone attached.
   Everything else (waveform generation, in-browser playback via
   `st.audio`, WAV upload/download, FFT/STFT analysis) works identically
   to running locally.
6. Under your app's **Settings → Sharing**, app visibility is controlled
   independently of the GitHub repo's visibility — you can keep the repo
   private while making the deployed app public (viewable via link, no
   login required), or vice versa.

## Tests

```bash
pytest                 # unit tests + AppTest smoke test
pytest tests/e2e        # browser E2E test (needs `pip install -r requirements-test.txt`
                         # and `playwright install chromium` first — see tests/e2e/README.md)
```

## Working as a team

See `CONTRIBUTING.md` for the branch-per-module workflow that lets
multiple people work simultaneously without stepping on each other's
files.
