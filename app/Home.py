import streamlit as st

st.set_page_config(page_title="Signal Generator & Analyzer", layout="wide")

st.title("Signal Generator & Analyzer — SP24")
st.markdown(
    """
    Use the pages in the sidebar:
    - **Generator** — synthesize square/sine/triangular/chirp/sinc waveforms
    - **Analyzer** — view time-domain, frequency-domain (FFT), and STFT plots
    - **Live Hardware** — play/record through your sound card
    """
)
