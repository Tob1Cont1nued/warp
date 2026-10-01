"""
Konfigurations-Overrides für Remote-Tests gegen die Produktions-URL.
Diese conftest überschreibt die lokalen Server-Fixtures aus tests/conftest.py.
"""
import pytest
from dotenv import load_dotenv

# Lädt .env im Projektroot (WARP_E2E_USERNAME/WARP_E2E_PASSWORD), bevor
# test_assessment.py seine Modul-Konstanten mit os.environ.get(...) auswertet.
# conftest.py wird von pytest vor dem Testmodul im selben Verzeichnis geladen.
load_dotenv()

PROD_URL = "https://warp-5ld0.onrender.com"


@pytest.fixture(scope="session")
def live_server() -> str:
    """Zeigt auf den Produktions-Server – kein lokaler Start nötig."""
    return PROD_URL


@pytest.fixture(scope="session", autouse=True)
def setup_test_users(live_server: str):  # noqa: F811
    """No-op: Benutzer existieren bereits auf dem Produktions-Server."""
    yield
