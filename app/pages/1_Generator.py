import _pathfix  # noqa: F401  (must be first — puts repo root on sys.path)
import numpy as np
import plotly.graph_objects as go
import streamlit as st

from src.common.wav_io import to_wav_bytes
from src.generator import waveforms

st.title("Generator")

with st.sidebar:
    st.subheader("Controls")
    waveform_type = st.selectbox(
        "Waveform", ["sine", "square", "triangular", "chirp", "sinc_pulse"]
    )
    freq_hz = st.slider("Frequency (Hz)", 20, 2000, 440)
    duration_s = st.slider("Duration (s)", 0.1, 5.0, 1.0)
    sample_rate_choice = st.selectbox("Sample rate (Hz)", ["8000", "16000", "44100", "Custom"], index=2)
    if sample_rate_choice == "Custom":
        sample_rate = st.number_input(
            "Custom sample rate (Hz)", min_value=100, max_value=384000, value=44100, step=100
        )
    else:
        sample_rate = int(sample_rate_choice)
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

    duration_ms = duration_s * 1000
    default_view_ms = float(min(50.0, duration_ms))
    view_ms = st.slider("View window (ms)", 5.0, float(duration_ms), default_view_ms)
    show_samples = st.checkbox("Show discrete samples (stem plot)", value=True)

st.subheader("Waveform")
n_view = max(2, int(sample_rate * view_ms / 1000))
t_ms = np.arange(n_view) / sample_rate * 1000
sig_view = signal[:n_view]

fig = go.Figure()
if show_samples:
    stem_x, stem_y = [], []
    for xi, yi in zip(t_ms, sig_view):
        stem_x += [xi, xi, None]
        stem_y += [0, yi, None]
    fig.add_trace(go.Scatter(x=stem_x, y=stem_y, mode="lines", line=dict(color="steelblue"), showlegend=False))
    fig.add_trace(go.Scatter(x=t_ms, y=sig_view, mode="markers", marker=dict(color="steelblue", size=6), showlegend=False))
else:
    fig.add_trace(go.Scatter(x=t_ms, y=sig_view, mode="lines", line=dict(color="steelblue"), showlegend=False))
fig.update_layout(
    title=f"{waveform_type} @ {freq_hz} Hz",
    xaxis_title="Time (ms)",
    yaxis_title="Amplitude",
    uirevision="generator-waveform-plot",
)
st.plotly_chart(fig, use_container_width=True)

wav_bytes = to_wav_bytes(signal, sample_rate)
st.audio(wav_bytes, format="audio/wav")
st.download_button("Download as WAV", data=wav_bytes, file_name=f"{label}.wav", mime="audio/wav")

st.session_state["last_signal"] = signal
st.session_state["last_sample_rate"] = sample_rate
st.session_state["last_label"] = label
st.caption("Signal stored in session — open the Analyzer page to inspect it.")
