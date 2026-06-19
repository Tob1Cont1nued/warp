"""
Fixtures für Flask-Unit-Tests (Test-Client, kein Browser).
Verwendet SQLite als temporäre Datei – alle Connections sehen dieselbe DB.
"""

import os
import tempfile
import pytest

# Env-Variablen VOR dem Import von app setzen
os.environ["SECRET_KEY"]         = "unit-test-secret"
os.environ["ANTHROPIC_API_KEY"]  = "dummy-key-for-tests"
os.environ["WARP_INBOX_API_KEY"] = "test-api-key-123"

from app import create_app
from app.models import db, User


# ---------------------------------------------------------------------------
# App-Fixture mit temporärer SQLite-Datei
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def app():
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    db_url = f"sqlite:///{db_path}"
    os.environ["DATABASE_URL"] = db_url

    application = create_app()
    application.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=db_url,
        WTF_CSRF_ENABLED=False,
    )
    yield application

    os.close(db_fd)
    try:
        os.unlink(db_path)
    except OSError:
        pass


# ---------------------------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------------------------

def _ensure_user(app, username: str, password: str, role: str = "user") -> None:
    with app.app_context():
        u = db.session.execute(
            db.select(User).where(User.username == username)
        ).scalar_one_or_none()
        if not u:
            u = User(username=username, display_name=username, role=role)
            u.set_password(password)
            db.session.add(u)
            db.session.commit()


def _logged_in_client(app, username: str, password: str):
    c = app.test_client()
    r = c.post("/login", data={"username": username, "password": password},
               follow_redirects=False)
    assert r.status_code == 302, (
        f"Login fehlgeschlagen für {username!r}: Status {r.status_code}"
    )
    return c


# ---------------------------------------------------------------------------
# Clients – jeder hat EIGENE Instanz, keine geteilte Session
# ---------------------------------------------------------------------------

@pytest.fixture
def client(app):
    """Frischer, nicht eingeloggter Client – function-scoped."""
    return app.test_client()


@pytest.fixture(scope="session")
def user_client(app):
    _ensure_user(app, "_unit_user", "unit_pw_123", role="user")
    return _logged_in_client(app, "_unit_user", "unit_pw_123")


@pytest.fixture(scope="session")
def admin_client(app):
    _ensure_user(app, "_unit_admin", "unit_admin_pw", role="admin")
    return _logged_in_client(app, "_unit_admin", "unit_admin_pw")


@pytest.fixture(scope="session")
def superuser_client(app):
    # Der seeded Admin (warp2024) wird in create_app() angelegt
    return _logged_in_client(app, "admin", "warp2024")


# ---------------------------------------------------------------------------
# Testprojekt
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def test_project_id(app, user_client):
    resp = user_client.post(
        "/project/new",
        data={"name": "Unit-Test-Projekt", "catalog_type": "assessment"},
        follow_redirects=False,
    )
    location = resp.headers.get("Location", "")
    for part in location.split("/"):
        if part.isdigit():
            return int(part)
    pytest.fail(
        f"Projekt-ID nicht ermittelbar – Location: {location!r} "
        f"(Status: {resp.status_code})"
    )
