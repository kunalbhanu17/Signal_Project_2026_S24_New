import _pathfix  # noqa: F401  (must be first — puts repo root on sys.path)
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import streamlit as st

from src.analyzer import freq_domain, stft, time_domain
from src.common.wav_io import from_wav_bytes

st.title("Analyzer")

with st.sidebar:
    st.subheader("Controls")
    uploaded = st.file_uploader("Analyze your own WAV file (optional)", type=["wav"])
    if uploaded is not None:
        signal, sample_rate = from_wav_bytes(uploaded.read())
        st.session_state["last_signal"] = signal
        st.session_state["last_sample_rate"] = sample_rate
        st.session_state["last_label"] = uploaded.name

    signal = st.session_state.get("last_signal")
    sample_rate = st.session_state.get("last_sample_rate")

    if signal is not None:
        duration_ms = len(signal) / sample_rate * 1000
        default_view_ms = float(min(50.0, duration_ms))
        view_ms = st.slider("View window (ms)", 5.0, float(duration_ms), default_view_ms)
        show_samples = st.checkbox("Show discrete samples (stem plot)", value=True)
        window = st.selectbox("FFT window", list(freq_domain.WINDOWS.keys()))
        compact_view = st.checkbox(
            "Compact 2x2 view (no scrolling)", value=True,
            help="Shows waveform, window shape, FFT, and STFT together in one "
                 "screen. Uncheck to go back to the larger scrolling layout.",
        )

if signal is None:
    st.info("Generate a signal on the Generator page, or upload a WAV file above.")
    st.stop()

st.caption(
    f"Analyzing: **{st.session_state.get('last_label', 'signal')}** — "
    f"{len(signal)} samples @ {sample_rate} Hz ({len(signal) / sample_rate:.3f} s) — "
    f"RMS **{time_domain.rms(signal):.4f}** — "
    f"Peak-to-peak **{time_domain.peak_to_peak(signal):.4f}**"
)

n_view = max(2, int(sample_rate * view_ms / 1000))
t_ms = np.arange(n_view) / sample_rate * 1000
sig_view = signal[:n_view]

freqs, magnitude = freq_domain.fft_spectrum(signal, sample_rate, window)
db = freq_domain.to_db(magnitude)
f_stft, t_stft, mag_2d = stft.stft_spectrogram(signal, sample_rate)
db_2d = freq_domain.to_db(mag_2d)
leakage = freq_domain.leakage_db(freqs, magnitude)

if compact_view:
    quad_figsize = (5.0, 2.7)

    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        st.caption("Waveform")
        fig_wave, ax_wave = plt.subplots(figsize=quad_figsize)
        if show_samples:
            ax_wave.plot(t_ms, sig_view, marker="o", markersize=2, linewidth=0.8)
        else:
            ax_wave.plot(t_ms, sig_view)
        ax_wave.set_xlabel("Time (ms)")
        ax_wave.set_ylabel("Amplitude")
        ax_wave.grid(True, alpha=0.3)
        fig_wave.tight_layout()
        st.pyplot(fig_wave)
        plt.close(fig_wave)

    with row1_col2:
        st.caption(f"Window shape ({window})")
        win_curve = freq_domain.window_curve(len(signal), window)
        fig_win, ax_win = plt.subplots(figsize=quad_figsize)
        ax_win.plot(win_curve)
        ax_win.set_xlabel("Sample index")
        ax_win.set_ylabel("Amplitude")
        ax_win.set_ylim(-0.05, 1.05)
        ax_win.grid(True, alpha=0.3)
        fig_win.tight_layout()
        st.pyplot(fig_win)
        plt.close(fig_win)

    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        st.caption(f"FFT — leakage {leakage:.1f} dB")
        fig_fft, ax_fft = plt.subplots(figsize=quad_figsize)
        ax_fft.plot(freqs, db)
        ax_fft.set_xlabel("Frequency (Hz)")
        ax_fft.set_ylabel("Magnitude (dB)")
        ax_fft.grid(True, alpha=0.3)
        fig_fft.tight_layout()
        st.pyplot(fig_fft)
        plt.close(fig_fft)

    with row2_col2:
        st.caption("STFT (spectrogram)")
        fig_stft, ax_stft = plt.subplots(figsize=quad_figsize)
        ax_stft.pcolormesh(t_stft, f_stft, db_2d, shading="gouraud", cmap="magma")
        ax_stft.set_xlabel("Time (s)")
        ax_stft.set_ylabel("Frequency (Hz)")
        fig_stft.tight_layout()
        st.pyplot(fig_stft)
        plt.close(fig_stft)

else:
    st.subheader("Time domain")
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
    fig1.update_layout(
        xaxis_title="Time (ms)", yaxis_title="Amplitude", uirevision="analyzer-time-domain-plot",
        height=260, margin=dict(l=10, r=10, t=10, b=10),
    )
    st.plotly_chart(fig1, use_container_width=True)

    col_fft, col_stft = st.columns(2)

    with col_fft:
        st.subheader("Frequency domain (FFT)")
        fig2, ax2 = plt.subplots(figsize=(5.2, 3.6))
        ax2.plot(freqs, db)
        ax2.set_xlabel("Frequency (Hz)")
        ax2.set_ylabel("Magnitude (dB, relative to peak)")
        ax2.grid(True, alpha=0.3)
        fig2.tight_layout()
        st.pyplot(fig2)
        plt.close(fig2)
        st.metric(
            f"Spectral leakage ({window}, 20 Hz off-peak)",
            f"{leakage:.1f} dB",
            help="Magnitude 20 Hz from the peak, relative to the peak. Lower (more "
                 "negative) means less leakage. Compare this number across FFT "
                 "window choices for the same signal.",
        )

    with col_stft:
        st.subheader("STFT (spectrogram)")
        fig3, ax3 = plt.subplots(figsize=(5.2, 3.6))
        im = ax3.pcolormesh(t_stft, f_stft, db_2d, shading="gouraud", cmap="magma")
        ax3.set_xlabel("Time (s)")
        ax3.set_ylabel("Frequency (Hz)")
        fig3.colorbar(im, ax=ax3, label="Magnitude (dB)")
        fig3.tight_layout()
        st.pyplot(fig3)
        plt.close(fig3)
