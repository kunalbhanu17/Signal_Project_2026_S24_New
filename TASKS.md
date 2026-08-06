# Task list — SP24 Signal Generator & Analyzer

Deadline: **20 September 2026** (final submission = report + video demo +
code, per course FAQ). Work backward from that; leave real buffer before
the deadline for the report/video/viva prep, which are 95% of the grade.

Legend: `[A]` Person A (generator), `[B]` Person B (analyzer),
`[C]` Person C (app + hardware I/O), `[ALL]` everyone.

> **Status: a complete, working reference implementation is on `main`.**
> All 5 waveforms, time/FFT/STFT analysis, WAV export/import, and the
> Streamlit app are implemented and verified (16/16 tests pass, including
> end-to-end app smoke tests via `streamlit.testing.v1.AppTest`). Items
> below are checked off where genuinely done in that reference build.
>
> **This does not replace understanding it yourselves.** The viva is 50%
> of the grade and tests *your* understanding of the DSP concepts and
> implementation — and the report requires an individual contribution
> section, with plagiarism checks. Each person should read, run, tweak,
> and be able to explain their module in depth, not just accept it as-is.
> Treat the reference build as a strong starting point to extend and
> genuinely own, not a finished submission.

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
- [x] `[ALL]` `pip install -r requirements.txt` + `streamlit run
      app/Home.py` confirmed working (reference build, this machine) —
      each person should still confirm it on their own machine.

## 1. Core implementation

### `[A]` Generator (`src/generator/`)
- [x] `waveforms.py` implemented (sine, square, triangular, chirp,
      sinc) and unit-tested against expected frequency/amplitude/duty
      cycle behaviour.
- [ ] Review the formulas yourself and decide if any need tuning (e.g.
      different chirp sweep shape, extra waveform types) — make it yours.
- [x] `tests/test_generator.py` covers amplitude bounds, duty cycle, and
      chirp length.
- [ ] Add docstring examples for each waveform's expected use (frequency
      range, when to use it) — feeds report Section 5 (Methodology).

### `[B]` Analyzer (`src/analyzer/`)
- [x] FFT (`freq_domain.py`) and STFT (`stft.py`) implemented; FFT peak
      frequency detection is unit-tested.
- [ ] Add windowing options (Hann/Hamming/rectangular) for FFT and compare
      spectral leakage — useful evidence for the report (currently
      rectangular/no window on the FFT view; STFT uses scipy's default
      Hann window).
- [x] `tests/test_analyzer.py` covers FFT peak detection, RMS, STFT shape,
      and dB conversion.
- [ ] Document why these STFT parameters (window size, overlap) were
      chosen, or change them and document that instead.

### `[C]` App + Hardware (`src/hardware_io/`, `app/`)
- [ ] Verify `sounddevice` play/record works on your machine; document
      any platform-specific setup (e.g. PortAudio install) in README.
      (Not verifiable in the sandbox this was built in — no audio
      hardware there. Logic is unit-tested with mocked `sounddevice`
      calls, but real-hardware playback/recording needs a human to check.)
- [x] Three Streamlit pages implemented: Generator (waveform plot,
      in-browser playback, WAV download), Analyzer (time/FFT-dB/STFT
      plots, WAV upload to analyze any file), Live Hardware
      (local play/record).
- [x] `tests/test_hardware_io.py` (mocked `sounddevice`) and
      `tests/test_app_smoke.py` (full multipage app, via
      `streamlit.testing.v1.AppTest`) both pass.
- [ ] Decide on deployment target (Streamlit Community Cloud vs. local +
      video demo only) and document the choice in `key_decisions.txt`.

## 2. Integration (`[C]` leads, `[A]`/`[B]` review)
- [x] `feature/generator`, `feature/analyzer`, `feature/app-hardware`
      branches exist; reference implementation is merged to `main` and
      end-to-end verified (generator → analyzer round-trip, WAV
      export/import round-trip, all pages load with no exceptions).
- [ ] Each person pulls `main`, works from their branch, and opens PRs
      back in — don't just keep building on top of `main` solo.
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
