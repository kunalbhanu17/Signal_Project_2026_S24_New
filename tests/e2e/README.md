# Browser E2E test / video demo

`test_demo.py` drives the real Streamlit app in a headless browser with
[Playwright](https://playwright.dev/python/): it cycles every waveform on
the Generator page, exercises the Analyzer's time/FFT/STFT views and the
FFT window selector, and checks the Live Hardware page loads. It runs
against a local Streamlit server started automatically by `conftest.py`,
parametrized over the light and dark themes.

The unit/AppTest suite (`pytest` from the repo root) does not run this —
it's excluded by default because it needs a browser install. Run it
explicitly:

## Setup (once)

```bash
pip install -r requirements-test.txt
playwright install chromium        # downloads the browser; --with-deps needs sudo
```

## Run the tests

```bash
pytest tests/e2e
```

## Record the demo video

```bash
pytest tests/e2e --video=on --output=test-results
```

This produces one `.webm` per theme under `test-results/`. Convert to MP4
for the report (test-results/ is gitignored — regenerate on demand):

```bash
ffmpeg -i "test-results/tests-e2e-test-demo-py-test-full-app-walkthrough-light-chromium/video.webm" \
  -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -movflags +faststart \
  report/video_demo/app_walkthrough_light.mp4

ffmpeg -i "test-results/tests-e2e-test-demo-py-test-full-app-walkthrough-dark-chromium/video.webm" \
  -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -movflags +faststart \
  report/video_demo/app_walkthrough_dark.mp4
```

A banner overlay names each step under test for ~3 seconds so the
recording is self-explanatory without narration.
