import _pathfix  # noqa: F401  (must be first — puts repo root on sys.path)
import streamlit as st

from src.common.wav_io import from_wav_bytes
from src.hardware_io import audio_io

st.title("Live Hardware")

signal = st.session_state.get("last_signal")
sample_rate = st.session_state.get("last_sample_rate")

st.subheader("Browser microphone")
st.caption(
    "Records through your **browser's** mic via the Web Audio API — works on "
    "any device, including mobile, even when this app is hosted remotely."
)
audio_value = st.audio_input("Record")
if audio_value is not None:
    signal, sample_rate = from_wav_bytes(audio_value.read())
    st.session_state["last_signal"] = signal
    st.session_state["last_sample_rate"] = sample_rate
    st.session_state["last_label"] = "browser_microphone_recording"
    st.line_chart({"amplitude": signal[: min(2000, len(signal))]})
    st.success("Recorded — open the Analyzer page to inspect it.")

st.subheader("Local sound card")
st.caption(
    "Plays/records through **this machine's** sound card via `sounddevice`. "
    "Only works when the app is running locally (not on a hosted server)."
)

if st.button("Play last generated signal") and signal is not None:
    audio_io.play(signal, sample_rate)
    st.success("Played.")
elif signal is None:
    st.info("Generate a signal on the Generator page first to enable playback.")

duration_s = st.slider("Record duration (s)", 0.5, 5.0, 2.0)
if st.button("Record from microphone"):
    recorded = audio_io.record(duration_s, sample_rate or 44100)
    st.session_state["last_signal"] = recorded
    st.session_state["last_sample_rate"] = sample_rate or 44100
    st.session_state["last_label"] = "microphone_recording"
    st.line_chart({"amplitude": recorded[: min(2000, len(recorded))]})
    st.success("Recorded — open the Analyzer page to inspect it.")
