"""Starts a local Streamlit server for the Playwright E2E/demo-video tests.

Parametrized over theme (light/dark) so the same walkthrough gets recorded
against both — each theme gets its own Streamlit process (theme is a
server-side launch flag, not something togglable at runtime here).
"""
import socket
import subprocess
import time
from contextlib import closing
from pathlib import Path

import pytest
import requests

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def _free_port() -> int:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


@pytest.fixture(scope="session", params=["light", "dark"])
def theme(request):
    return request.param


@pytest.fixture(scope="session")
def streamlit_server(theme):
    port = _free_port()
    base_url = f"http://localhost:{port}"
    proc = subprocess.Popen(
        ["streamlit", "run", "app/Home.py", "--server.headless", "true",
         "--server.port", str(port), "--theme.base", theme],
        cwd=str(REPO_ROOT),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        for _ in range(60):
            try:
                if requests.get(base_url, timeout=1).status_code == 200:
                    break
            except requests.RequestException:
                pass
            time.sleep(0.5)
        else:
            proc.terminate()
            pytest.fail("Streamlit server did not start in time")
        yield base_url
    finally:
        proc.terminate()
        proc.wait(timeout=10)


@pytest.fixture(scope="session")
def base_url(streamlit_server):
    return streamlit_server


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "viewport": {"width": 1280, "height": 900}}
