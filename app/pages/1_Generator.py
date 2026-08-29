import _pathfix  # noqa: F401  (must be first — puts repo root on sys.path)
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from src.common.wav_io import to_wav_bytes
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
    label = f"square_{freq_hz}Hz_dc{duty_cycle:.2f}"
elif waveform_type == "chirp":
    f1_hz = st.slider("End frequency (Hz)", 20, 4000, 1000)
    signal = waveforms.chirp(freq_hz, f1_hz, duration_s, sample_rate, amplitude)
    label = f"chirp_{freq_hz}-{f1_hz}Hz"
else:
    signal = getattr(waveforms, waveform_type)(freq_hz, duration_s, sample_rate, amplitude)
    label = f"{waveform_type}_{freq_hz}Hz"

st.subheader("Waveform")
duration_ms = duration_s * 1000
default_view_ms = float(min(50.0, duration_ms))
view_ms = st.slider("View window (ms)", 5.0, float(duration_ms), default_view_ms)
n_view = max(2, int(sample_rate * view_ms / 1000))
t_ms = np.arange(n_view) / sample_rate * 1000
show_samples = st.checkbox("Show discrete samples (stem plot)")

fig, ax = plt.subplots()
if show_samples:
    ax.stem(t_ms, signal[:n_view], basefmt=" ")
else:
    ax.plot(t_ms, signal[:n_view])
ax.set_xlabel("Time (ms)")
ax.set_ylabel("Amplitude")
ax.set_title(f"{waveform_type} @ {freq_hz} Hz")
ax.grid(True, alpha=0.3)
st.pyplot(fig)
plt.close(fig)

wav_bytes = to_wav_bytes(signal, sample_rate)
st.audio(wav_bytes, format="audio/wav")
st.download_button("Download as WAV", data=wav_bytes, file_name=f"{label}.wav", mime="audio/wav")

st.session_state["last_signal"] = signal
st.session_state["last_sample_rate"] = sample_rate
st.session_state["last_label"] = label
st.caption("Signal stored in session — open the Analyzer page to inspect it.")
