"""Browser E2E test that doubles as the video-demo recording.

Run with `--video=on` (see tests/e2e/README.md) so Playwright records a
.webm of the whole walkthrough into test-results/. Parametrized over
light/dark theme (see conftest.py), so this produces one video per theme.

Notes on Streamlit + Playwright quirks this file works around:
- Multipage navigation must go through the sidebar nav links (client-side
  routing); a direct page.goto() to another page's URL starts a brand new
  Streamlit session and loses st.session_state.
- Streamlit's script-rerun timing isn't reflected by Playwright's
  network-idle signal (it's all websocket traffic), so nav-link clicks are
  retried until the URL actually changes rather than trusting one click.
- The range-slider's accessible name gets doubled up via aria-labelledby,
  which breaks get_by_role name matching — sliders are matched on their
  aria-label attribute directly instead.
- Streamlit fades new content in via a CSS transition; if nothing repaints
  after it settles, Playwright's video recorder freezes on a faded
  mid-transition frame. verify_visible() scrolls the element into view
  (forcing a repaint) before confirming it's actually visible.
"""
import re

WAVEFORMS = ["sine", "square", "triangular", "chirp", "sinc_pulse"]

BANNER_ID = "e2e-test-banner"
BANNER_JS_SHOW = """(text) => {
    let el = document.getElementById(%r);
    if (!el) {
        el = document.createElement('div');
        el.id = %r;
        el.style.cssText = 'position:fixed;top:0;left:0;right:0;z-index:999999;' +
            'padding:14px 20px;font:600 20px system-ui,sans-serif;text-align:center;' +
            'background:#1f6feb;color:#fff;box-shadow:0 2px 10px rgba(0,0,0,.35);';
        document.body.appendChild(el);
    }
    el.textContent = text;
    el.style.display = 'block';
}""" % (BANNER_ID, BANNER_ID)
BANNER_JS_HIDE = """() => {
    const el = document.getElementById(%r);
    if (el) el.style.display = 'none';
}""" % (BANNER_ID,)


def show_banner(page, text, duration_ms=3000):
    """Overlay a caption naming the step under test, held for `duration_ms`."""
    page.evaluate(BANNER_JS_SHOW, text)
    page.wait_for_timeout(duration_ms)
    page.evaluate(BANNER_JS_HIDE)


def assert_no_exception(page):
    assert page.locator('[data-testid="stException"]').count() == 0


def verify_visible(page, locator, timeout=20_000):
    """Scroll into view and confirm visible — forces a repaint so Streamlit's
    fade-in transition settles instead of freezing mid-fade in the video."""
    locator.wait_for(state="attached", timeout=timeout)
    locator.scroll_into_view_if_needed(timeout=timeout)
    locator.wait_for(state="visible", timeout=timeout)


def select_option(page, label, option, exact=True):
    combo = page.get_by_role("combobox", name=label)
    combo.scroll_into_view_if_needed()
    combo.click()
    page.get_by_role("option", name=option, exact=exact).first.wait_for(
        state="visible", timeout=10_000
    )
    page.get_by_role("option", name=option, exact=exact).click()


def nudge_slider(page, label, times=5, key="ArrowRight"):
    slider = page.locator(f'input[type="range"][aria-label="{label}"]')
    slider.scroll_into_view_if_needed()
    slider.focus()
    for _ in range(times):
        page.keyboard.press(key)


def goto_page(page, name, path, retries=8):
    link = page.get_by_test_id("stSidebarNavLink").filter(has_text=name)
    for _ in range(retries):
        link.click()
        try:
            page.wait_for_url(f"**{path}", timeout=1500)
            page.wait_for_timeout(500)
            return
        except Exception:
            continue
    raise AssertionError(f"never navigated to {name} ({path})")


def test_full_app_walkthrough(page, theme):
    page.goto("/", wait_until="networkidle")
    page.wait_for_timeout(1500)
    assert_no_exception(page)
    show_banner(page, f"Signal Generator & Analyzer — {theme} theme demo")

    # --- Generator: cycle every waveform type ---
    goto_page(page, "Generator", "/Generator")
    show_banner(page, "Generator: controls in the sidebar, live plot on the right")
    for waveform in WAVEFORMS:
        select_option(page, "Waveform", waveform, exact=True)
        page.wait_for_timeout(700)

        if waveform == "square":
            nudge_slider(page, "Duty cycle", times=5)
        elif waveform == "chirp":
            nudge_slider(page, "End frequency (Hz)", times=5)

        nudge_slider(page, "Frequency (Hz)", times=5)
        page.wait_for_timeout(500)

        verify_visible(page, page.locator(".js-plotly-plot").first)
        assert page.locator("audio").count() == 1
        assert page.get_by_role("button", name=re.compile("Download as WAV")).count() == 1
        assert_no_exception(page)

    # --- Analyzer: time/FFT/STFT views + FFT windowing ---
    goto_page(page, "Analyzer", "/Analyzer")
    show_banner(page, "Analyzer: time domain, FFT (dB), and STFT spectrogram")
    page.wait_for_timeout(500)
    assert_no_exception(page)

    verify_visible(page, page.locator(".js-plotly-plot").first)
    assert page.locator(".js-plotly-plot").count() == 1  # time domain
    images = page.locator('[data-testid="stImage"] img')
    page.wait_for_function(
        "document.querySelectorAll('[data-testid=\"stImage\"] img').length >= 2",
        timeout=20_000,
    )
    verify_visible(page, images.last)
    assert images.count() == 2  # FFT (dB) + STFT spectrogram

    show_banner(page, "FFT windowing: rectangular vs. Hann vs. Hamming")
    for window in ["rectangular", "hann", "hamming"]:
        select_option(page, "FFT window", window, exact=True)
        page.wait_for_timeout(900)
        verify_visible(page, page.locator('[data-testid="stImage"] img').first)
        assert_no_exception(page)

    # --- Live Hardware: page loads with local-only controls present ---
    goto_page(page, "Live Hardware", "/Live_Hardware")
    show_banner(page, "Live Hardware: local sound-card play/record controls")
    play_button = page.get_by_role("button", name="Play last generated signal")
    verify_visible(page, play_button)
    assert_no_exception(page)

    assert play_button.count() == 1
    assert page.get_by_role("button", name="Record from microphone").count() == 1
    assert page.get_by_text("this machine's").count() == 1
    show_banner(page, "Walkthrough complete", duration_ms=2000)
