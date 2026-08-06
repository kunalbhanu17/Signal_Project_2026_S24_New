import streamlit as st

st.set_page_config(page_title="Signal Generator & Analyzer", layout="wide")

st.title("Signal Generator & Analyzer — SP24")
st.markdown(
    """
    Use the pages in the sidebar:
    - **Generator** — synthesize square/sine/triangular/chirp/sinc waveforms,
      play them in-browser, and download as WAV
    - **Analyzer** — view time-domain, frequency-domain (FFT), and STFT
      plots of the last generated signal, or upload your own WAV file
    - **Live Hardware** — play/record through your machine's sound card
      (local use only, not on a hosted server)
    """
)
