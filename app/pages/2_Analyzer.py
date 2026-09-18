import _pathfix  # noqa: F401  (must be first — puts repo root on sys.path)
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import streamlit as st

from src.analyzer import freq_domain, stft, time_domain
from src.common.wav_io import from_wav_bytes

st.title("Analyzer")

uploaded = st.file_uploader("Analyze your own WAV file (optional)", type=["wav"])
if uploaded is not None:
    signal, sample_rate = from_wav_bytes(uploaded.read())
    st.session_state["last_signal"] = signal
    st.session_state["last_sample_rate"] = sample_rate
    st.session_state["last_label"] = uploaded.name

signal = st.session_state.get("last_signal")
sample_rate = st.session_state.get("last_sample_rate")

if signal is None:
    st.info("Generate a signal on the Generator page, or upload a WAV file above.")
    st.stop()

st.caption(
    f"Analyzing: **{st.session_state.get('last_label', 'signal')}** — "
    f"{len(signal)} samples @ {sample_rate} Hz ({len(signal) / sample_rate:.3f} s)"
)

col1, col2 = st.columns(2)
col1.metric("RMS", f"{time_domain.rms(signal):.4f}")
col2.metric("Peak-to-peak", f"{time_domain.peak_to_peak(signal):.4f}")

st.subheader("Time domain")
duration_ms = len(signal) / sample_rate * 1000
default_view_ms = float(min(50.0, duration_ms))
view_ms = st.slider("View window (ms)", 5.0, float(duration_ms), default_view_ms)
n_view = max(2, int(sample_rate * view_ms / 1000))
t_ms = np.arange(n_view) / sample_rate * 1000
sig_view = signal[:n_view]
show_samples = st.checkbox("Show discrete samples (stem plot)")

fig1 = go.Figure()
if show_samples:
    stem_x, stem_y = [], []
    for xi, yi in zip(t_ms, sig_view):
        stem_x += [xi, xi, None]
        stem_y += [0, yi, None]
    fig1.add_trace(go.Scatter(x=stem_x, y=stem_y, mode="lines", line=dict(color="steelblue"), showlegend=False))
    fig1.add_trace(go.Scatter(x=t_ms, y=sig_view, mode="markers", marker=dict(color="steelblue", size=6), showlegend=False))
else:
    fig1.add_trace(go.Scatter(x=t_ms, y=sig_view, mode="lines", line=dict(color="steelblue"), showlegend=False))
fig1.update_layout(xaxis_title="Time (ms)", yaxis_title="Amplitude")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Frequency domain (FFT)")
window = st.selectbox("FFT window", list(freq_domain.WINDOWS.keys()))
freqs, magnitude = freq_domain.fft_spectrum(signal, sample_rate, window)
db = freq_domain.to_db(magnitude)
fig2, ax2 = plt.subplots()
ax2.plot(freqs, db)
ax2.set_xlabel("Frequency (Hz)")
ax2.set_ylabel("Magnitude (dB, relative to peak)")
ax2.grid(True, alpha=0.3)
st.pyplot(fig2)
plt.close(fig2)

st.subheader("STFT (spectrogram)")
f_stft, t_stft, mag_2d = stft.stft_spectrogram(signal, sample_rate)
db_2d = freq_domain.to_db(mag_2d)
fig3, ax3 = plt.subplots()
im = ax3.pcolormesh(t_stft, f_stft, db_2d, shading="gouraud", cmap="magma")
ax3.set_xlabel("Time (s)")
ax3.set_ylabel("Frequency (Hz)")
fig3.colorbar(im, ax=ax3, label="Magnitude (dB)")
st.pyplot(fig3)
plt.close(fig3)
