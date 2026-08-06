# Task list — SP24 Signal Generator & Analyzer

Deadline: **20 September 2026** (final submission = report + video demo +
code, per course FAQ). Work backward from that; leave real buffer before
the deadline for the report/video/viva prep, which are 95% of the grade.

Legend: `[A]` Person A (generator), `[B]` Person B (analyzer),
`[C]` Person C (app + hardware I/O), `[ALL]` everyone.

## 0. Kickoff (do first, together)
- [ ] `[ALL]` Assign who is A / B / C and write names into this file and
      `CONTRIBUTING.md`.
- [ ] `[ALL]` If this project is being submitted under the pre-approved
      SP24 topic, confirm with the instructor whether a proposal email is
      still required (course FAQ: proposal is required for **custom**
      topics; pre-approved topics start immediately after the selection
      form). If a proposal is wanted anyway, draft
      `documentation/proposal.md` (Problem / Objectives / Methodology) and
      send to vishal@study.iitm.ac.in, cc venkatesan@study.iitm.ac.in,
      ankita_p@study.iitm.ac.in.
- [ ] `[ALL]` Each person clones the repo and sets up their branch per
      `CONTRIBUTING.md`.
- [ ] `[ALL]` Each person runs `pip install -r requirements.txt` and
      confirms `streamlit run app/Home.py` launches locally.

## 1. Core implementation

### `[A]` Generator (`src/generator/`)
- [ ] Sanity-check/extend `waveforms.py` (sine, square, triangular, chirp,
      sinc already scaffolded) — verify against known reference plots.
- [ ] Add duty-cycle edge case handling and amplitude clipping guards.
- [ ] Write/expand `tests/test_generator.py` (frequency accuracy, RMS,
      duty cycle, chirp sweep bounds).
- [ ] Add docstring examples for each waveform's expected use (frequency
      range, when to use it) — feeds report Section 5 (Methodology).

### `[B]` Analyzer (`src/analyzer/`)
- [ ] Sanity-check/extend FFT (`freq_domain.py`) and STFT
      (`stft.py`) — verify peak frequency detection against known inputs.
- [ ] Add windowing options (Hann/Hamming/rectangular) for FFT and compare
      spectral leakage — useful evidence for the report.
- [ ] Write/expand `tests/test_analyzer.py`.
- [ ] Decide and document STFT parameters (window size, overlap) and why.

### `[C]` App + Hardware (`src/hardware_io/`, `app/`)
- [ ] Verify `sounddevice` play/record works on your machine; document
      any platform-specific setup (e.g. PortAudio install) in README.
- [ ] Polish the three Streamlit pages (Generator/Analyzer/Live Hardware)
      — file upload for analyzing external audio, download button for
      generated waveforms (WAV export).
- [ ] Write/expand `tests/test_hardware_io.py` (mocked, no real device
      needed in CI).
- [ ] Decide on deployment target (Streamlit Community Cloud vs. local +
      video demo only) and document the choice in `key_decisions.txt`.

## 2. Integration (`[C]` leads, `[A]`/`[B]` review)
- [ ] Merge `feature/generator` and `feature/analyzer` into `main`.
- [ ] Merge `feature/app-hardware` last; confirm generator → analyzer →
      hardware round-trip works end-to-end in the running app.
- [ ] Cross-test: each person tries the other two modules' features and
      files issues for anything confusing or broken.

## 3. Report & submission (per course FAQ format)
- [ ] `[ALL]` Draft report sections individually, then combine:
      1) Abstract 2) Introduction 3) Problem statement
      4) Goals and Objectives 5) Methodology 6) Implementation details
      7) Problems faced & solutions 8) Results and discussions
      9) Conclusions 10) Individual contributions 11) Annexure (Drive link
      to video + code zip — **must be "anyone with the link"**).
- [ ] `[C]` Record video demo: generator producing each waveform type,
      analyzer showing time/freq/STFT views, live hardware playback.
- [ ] `[ALL]` Zip the code (or link the GitHub repo) and upload to Google
      Drive with public link access; add link to report Annexure.
- [ ] `[ALL]` Submit report + video + code via the Seek portal.

## 4. Viva prep (50% of the grade — don't shortchange this)
- [ ] `[ALL]` Each person can independently explain: the DSP theory behind
      their module (FFT/STFT math, waveform synthesis formulas), design
      decisions in `documentation/key_decisions.txt`, and the full
      pipeline end-to-end — not just their own piece.
- [ ] `[ALL]` Do a practice run-through of the demo + likely viva
      questions together before the real viva.

## Milestone checkpoints (adjust dates once the actual timeline is known)
- **Week 1–2**: Kickoff + core module implementation (`[A]`, `[B]`, `[C]`
  in parallel).
- **Week 3**: Integration + cross-testing.
- **Week 4**: Report drafting + video demo recording.
- **Buffer before 20 Sept**: Final submission + viva prep.
