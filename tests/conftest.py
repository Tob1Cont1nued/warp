"""
Shared fixtures für alle WARP Playwright-Tests (Page Object Model).
"""

import re
import subprocess
import sys
import time
from pathlib import Path

import pytest
import requests
from playwright.sync_api import Page

# tests/ in sys.path aufnehmen damit 'from pages.xxx import ...' in Testdateien klappt
sys.path.insert(0, str(Path(__file__).parent))

from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.questionnaire_page import QuestionnairePage
from pages.admin_page import AdminPage

ROOT     = Path(__file__).parent.parent
BASE_URL = "http://127.0.0.1:5000"

ADMIN      = {"username": "admin",          "password": "warp2024"}
TEST_USER  = {"username": "_pytest_user",   "password": "pytest_pw1",
              "display_name": "Pytest Testbenutzer"}
TEST_USER2 = {"username": "_pytest_user2",  "password": "pytest_pw2",
              "display_name": "Pytest Testbenutzer 2"}


# ── Server ───────────────────────────────────────────────────────────────────

def _server_healthy() -> bool:
    """Prüft per HTTP-Request ob der Server tatsächlich antwortet (nicht nur TCP)."""
    try:
        r = requests.get(f"{BASE_URL}/login", timeout=2, allow_redirects=False)
        return r.status_code in (200, 301, 302)
    except requests.RequestException:
        return False


@pytest.fixture(scope="session")
def live_server():
    """Startet Flask falls noch nicht aktiv oder abgestürzt; gibt BASE_URL zurück."""
    proc = None
    if not _server_healthy():
        proc = subprocess.Popen(
            [sys.executable, "run.py"],
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        for _ in range(60):
            if _server_healthy():
                break
            time.sleep(0.25)
        else:
            proc.kill()
            pytest.fail(
                "Flask-Server konnte nicht gestartet werden. "
                "Stelle sicher dass die venv aktiv ist und "
                "'pip install -r requirements.txt' ausgeführt wurde."
            )
    yield BASE_URL
    if proc:
        proc.terminate()


@pytest.fixture(scope="session")
def base_url(live_server: str) -> str:
    return live_server


# ── Test-Benutzer Setup ──────────────────────────────────────────────────────

def _register_user(base_url: str, username: str, password: str, display_name: str = "") -> None:
    """Registriert einen Benutzer mit CSRF-Token (idempotent)."""
    session = requests.Session()
    resp = session.get(f"{base_url}/register", timeout=5)
    # CSRF-Token aus dem HTML-Formular lesen
    m = re.search(r'name="csrf_token"\s+value="([^"]+)"', resp.text)
    csrf_token = m.group(1) if m else ""
    session.post(f"{base_url}/register", data={
        "csrf_token":   csrf_token,
        "username":     username,
        "display_name": display_name,
        "password":     password,
        "password2":    password,
    })


@pytest.fixture(scope="session", autouse=True)
def setup_test_users(live_server: str):
    """Legt Testbenutzer einmalig an (idempotent – schlägt still fehl wenn schon vorhanden)."""
    for user in (TEST_USER, TEST_USER2):
        _register_user(live_server, user["username"], user["password"],
                       user.get("display_name", ""))


# ── Page Object Fixtures ─────────────────────────────────────────────────────

@pytest.fixture
def login_page(page: Page, base_url: str) -> LoginPage:
    """LoginPage-Objekt (nicht eingeloggt)."""
    return LoginPage(page, base_url)


@pytest.fixture
def register_page(page: Page, base_url: str) -> RegisterPage:
    """RegisterPage-Objekt (nicht eingeloggt)."""
    return RegisterPage(page, base_url)


@pytest.fixture
def admin_page(page: Page, base_url: str) -> AdminPage:
    """AdminPage-Objekt – bereits als Admin eingeloggt, Seite /admin."""
    LoginPage(page, base_url).login(ADMIN["username"], ADMIN["password"])
    return AdminPage(page, base_url)


@pytest.fixture
def user_page(page: Page, base_url: str) -> QuestionnairePage:
    """QuestionnairePage-Objekt – als Testbenutzer eingeloggt."""
    LoginPage(page, base_url).login(TEST_USER["username"], TEST_USER["password"])
    qp = QuestionnairePage(page, base_url)
    if "project/new" in page.url:
        qp.create_first_project("Pytest Testprojekt")
    return qp
