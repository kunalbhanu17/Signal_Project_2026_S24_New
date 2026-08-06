import _pathfix  # noqa: F401  (must be first — puts repo root on sys.path)
import streamlit as st

from src.analyzer import freq_domain, stft, time_domain

st.title("Analyzer")

signal = st.session_state.get("last_signal")
sample_rate = st.session_state.get("last_sample_rate")

if signal is None:
    st.info("Generate a signal on the Generator page first.")
    st.stop()

st.subheader("Time domain")
st.line_chart({"amplitude": signal[: min(2000, len(signal))]})
st.metric("RMS", f"{time_domain.rms(signal):.4f}")
st.metric("Peak-to-peak", f"{time_domain.peak_to_peak(signal):.4f}")

st.subheader("Frequency domain (FFT)")
freqs, magnitude = freq_domain.fft_spectrum(signal, sample_rate)
st.line_chart({"frequency_hz": freqs, "magnitude": magnitude}, x="frequency_hz")

st.subheader("STFT (spectrogram)")
f_stft, t_stft, mag_2d = stft.stft_spectrogram(signal, sample_rate)
st.write(f"Spectrogram shape: {mag_2d.shape} (freq bins x time frames)")
st.image(mag_2d / mag_2d.max(), clamp=True, caption="STFT magnitude (normalized)")
