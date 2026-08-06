"""Smoke tests: exercise the real Streamlit multipage app end-to-end.

Uses streamlit.testing.v1.AppTest, which runs pages with a proper
ScriptRunContext (unlike `python app/pages/X.py`, which triggers
"missing ScriptRunContext" and breaks session_state/st.stop()).
"""
from pathlib import Path

from streamlit.testing.v1 import AppTest

_HOME_PAGE = str(Path(__file__).resolve().parent.parent / "app" / "Home.py")


def _start():
    at = AppTest.from_file(_HOME_PAGE)
    at.run(timeout=30)
    assert not at.exception
    return at


def test_home_page_loads():
    _start()


def test_generator_page_produces_a_signal():
    at = _start()
    at.switch_page("pages/1_Generator.py")
    at.run(timeout=30)
    assert not at.exception
    assert len(at.session_state["last_signal"]) > 0


def test_generator_to_analyzer_pipeline_renders_all_plots():
    at = _start()
    at.switch_page("pages/1_Generator.py")
    at.run(timeout=30)
    at.switch_page("pages/2_Analyzer.py")
    at.run(timeout=30)
    assert not at.exception
    assert len(at.get("image")) == 3  # time domain, FFT, STFT


def test_analyzer_prompts_when_no_signal_yet():
    at = AppTest.from_file(_HOME_PAGE)
    at.run(timeout=30)
    at.switch_page("pages/2_Analyzer.py")
    at.run(timeout=30)
    assert not at.exception
    assert any("Generate a signal" in i.value for i in at.info)


def test_live_hardware_page_loads():
    at = _start()
    at.switch_page("pages/3_Live_Hardware.py")
    at.run(timeout=30)
    assert not at.exception
