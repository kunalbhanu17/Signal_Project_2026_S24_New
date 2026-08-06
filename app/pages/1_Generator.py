import _pathfix  # noqa: F401  (must be first — puts repo root on sys.path)
import numpy as np
import streamlit as st

from src.generator import waveforms

st.title("Generator")

waveform_type = st.selectbox(
    "Waveform", ["sine", "square", "triangular", "chirp", "sinc_pulse"]
)
freq_hz = st.slider("Frequency (Hz)", 20, 2000, 440)
duration_s = st.slider("Duration (s)", 0.1, 5.0, 1.0)
sample_rate = st.selectbox("Sample rate (Hz)", [8000, 16000, 44100], index=2)
amplitude = st.slider("Amplitude", 0.0, 1.0, 0.8)

if waveform_type == "square":
    duty_cycle = st.slider("Duty cycle", 0.05, 0.95, 0.5)
    signal = waveforms.square(freq_hz, duration_s, sample_rate, amplitude, duty_cycle)
elif waveform_type == "chirp":
    f1_hz = st.slider("End frequency (Hz)", 20, 4000, 1000)
    signal = waveforms.chirp(freq_hz, f1_hz, duration_s, sample_rate, amplitude)
else:
    signal = getattr(waveforms, waveform_type)(freq_hz, duration_s, sample_rate, amplitude)

t = np.arange(len(signal)) / sample_rate
st.line_chart({"amplitude": signal[: min(2000, len(signal))]})

st.session_state["last_signal"] = signal
st.session_state["last_sample_rate"] = sample_rate
st.caption("Signal stored in session — open the Analyzer page to inspect it.")
