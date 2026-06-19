"""
Fixtures für Flask-Unit-Tests (Test-Client, kein Browser).
Verwendet SQLite in-memory – keine laufende DB nötig.
"""

import os
import pytest

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "unit-test-secret")
os.environ.setdefault("ANTHROPIC_API_KEY", "dummy-key-for-tests")

from app import create_app
from app.models import db, User, Project


@pytest.fixture(scope="session")
def app():
    application = create_app()
    application.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        WTF_CSRF_ENABLED=False,
    )
    yield application


@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


# ---------------------------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------------------------

def _ensure_user(app, username: str, password: str, role: str = "user") -> int:
    with app.app_context():
        u = db.session.execute(
            db.select(User).where(User.username == username)
        ).scalar_one_or_none()
        if not u:
            u = User(username=username, display_name=username, role=role)
            u.set_password(password)
            db.session.add(u)
            db.session.commit()
        return u.id


# ---------------------------------------------------------------------------
# Angemeldete Clients
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def user_client(app, client):
    """Flask-Test-Client als normaler Benutzer eingeloggt."""
    _ensure_user(app, "_unit_user", "unit_pw_123", role="user")
    client.post("/login", data={"username": "_unit_user", "password": "unit_pw_123"})
    yield client
    client.get("/logout")


@pytest.fixture(scope="session")
def admin_client(app, client):
    """Flask-Test-Client als Admin eingeloggt (nutzt seeded admin)."""
    _ensure_user(app, "_unit_admin", "unit_admin_pw", role="admin")
    c = app.test_client()
    c.post("/login", data={"username": "_unit_admin", "password": "unit_admin_pw"})
    yield c
    c.get("/logout")


@pytest.fixture(scope="session")
def superuser_client(app, client):
    """Flask-Test-Client als Superuser (nutzt seeded admin)."""
    c = app.test_client()
    c.post("/login", data={"username": "admin", "password": "warp2024"})
    yield c
    c.get("/logout")


# ---------------------------------------------------------------------------
# Testprojekt
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def test_project_id(app, user_client):
    """Legt einmalig ein Projekt für _unit_user an und gibt die ID zurück."""
    resp = user_client.post(
        "/project/new",
        data={"name": "Unit-Test-Projekt", "catalog_type": "assessment"},
        follow_redirects=False,
    )
    location = resp.headers.get("Location", "")
    # Location z.B. /project/5
    for part in location.split("/"):
        if part.isdigit():
            return int(part)
    pytest.fail(f"Konnte Projekt-ID nicht aus Location ermitteln: {location}")
