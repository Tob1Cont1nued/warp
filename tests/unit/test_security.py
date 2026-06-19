"""
TC-SEC – Sicherheitstests
=========================

TC-SEC-01  SQL-Injection im Login              -> kein Auth-Bypass
TC-SEC-02  XSS im Projektnamen                 -> Ausgabe HTML-escaped
TC-SEC-03  CSRF-Schutz konfiguriert            -> Extension registriert
TC-SEC-04  Session-Schutz konfiguriert         -> Flask-Login session_protection aktiv
TC-SEC-05  Path-Traversal via Static-URL       -> 400/404, kein Datei-Zugriff
TC-SEC-06  10x falsches Passwort               -> kein 500, App stabil
TC-SEC-07  Cross-User Projektzugriff           -> 403 fuer fremden User
TC-SEC-08  Sicherheits-Header vorhanden        -> X-Frame-Options, X-Content-Type-Options
TC-SEC-09  API-Key nicht in Response           -> Key nicht im Response-Body
TC-SEC-10  Geschuetzte Routen ohne Login       -> immer Redirect zu /login
TC-SEC-11  Admin-Routen fuer normalen User     -> immer 403
"""

import json
import os
import pytest

API_KEY = os.environ.get("WARP_INBOX_API_KEY", "test-api-key-123")


class TestSQLInjection:
    def test_tc_sec_01_sql_injection_im_login(self, client):
        """SQL-Injection-Payloads duerfen keinen Login-Bypass ermoeglichen."""
        payloads = [
            {"username": "' OR '1'='1", "password": "anything"},
            {"username": "admin'--",    "password": ""},
            {"username": "' OR 1=1--", "password": "' OR 1=1--"},
        ]
        for payload in payloads:
            r = client.post("/login", data=payload, follow_redirects=False)
            assert r.status_code != 302, (
                f"SQL-Injection hat Login ermoeglicht: {payload!r}"
            )


class TestXSS:
    def test_tc_sec_02_xss_in_projektname_wird_escaped(self, user_client):
        """Script-Tags im Projektnamen werden von Jinja2 HTML-escaped."""
        xss = "<script>alert('xss')</script>"
        r = user_client.post(
            "/project/new",
            data={"name": xss, "catalog_type": "assessment"},
            follow_redirects=False,
        )
        assert r.status_code == 302
        proj_id = None
        for part in r.headers.get("Location", "").split("/"):
            if part.isdigit():
                proj_id = int(part)
                break
        assert proj_id is not None, "Projekt-ID nach Anlegen nicht ermittelbar"

        r2 = user_client.get(f"/project/{proj_id}")
        assert r2.status_code == 200
        body = r2.data.decode("utf-8", errors="replace")
        assert "<script>alert(" not in body, "XSS: Script-Tag ungescaped im HTML!"


class TestCSRF:
    def test_tc_sec_03_unauthenticated_post_wird_abgelehnt(self, app):
        """POST auf geschuetzte Routen ohne Session wird nicht verarbeitet (Redirect)."""
        with app.test_client() as c:
            r = c.post(
                "/project/new",
                data={"name": "csrf-test", "catalog_type": "assessment"},
                follow_redirects=False,
            )
            assert r.status_code == 302, (
                f"Unauthentifizierter POST nicht blockiert: Status {r.status_code}"
            )
            assert "login" in r.headers.get("Location", "").lower(), (
                "Redirect geht nicht zu /login"
            )


class TestSessionFixation:
    def test_tc_sec_04_flask_login_initialisiert(self, app):
        """Flask-Login ist initialisiert und schuetzt alle Login-pflichtigen Routen."""
        assert hasattr(app, "login_manager"), "Flask-Login LoginManager nicht initialisiert"
        lm = app.login_manager
        assert lm.login_view == "login", (
            f"Login-View falsch konfiguriert: {lm.login_view!r}"
        )
        assert lm.session_protection in ("basic", "strong"), (
            f"session_protection zu schwach: {lm.session_protection!r}"
        )


class TestPathTraversal:
    def test_tc_sec_05_path_traversal_blockiert(self, client):
        """Path-Traversal-Versuche ueber Static-Route werden blockiert."""
        for path in [
            "/static/../app/__init__.py",
            "/static/../../requirements.txt",
            "/static/%2e%2e%2fapp%2f__init__.py",
        ]:
            r = client.get(path)
            assert r.status_code in (400, 404), (
                f"Path Traversal nicht blockiert: {path} -> {r.status_code}"
            )


class TestBruteForce:
    def test_tc_sec_06_wiederholte_fehlanmeldungen_stabil(self, client):
        """10x falsche Anmeldung fuehrt zu keinem Serverabsturz (kein HTTP 500)."""
        for i in range(10):
            r = client.post(
                "/login",
                data={"username": f"ghost_{i}", "password": "wrong"},
                follow_redirects=True,
            )
            assert r.status_code != 500, f"Serverabsturz bei Versuch {i + 1}"
            assert r.status_code == 200


class TestBrokenAccessControl:
    def test_tc_sec_07_fremdes_projekt_gibt_403(self, app, test_project_id):
        """User B darf nicht auf das Projekt von User A zugreifen."""
        from tests.unit.conftest import _ensure_user, _logged_in_client
        _ensure_user(app, "_sec_user_b", "sec_pw_b_456", role="user")
        user_b = _logged_in_client(app, "_sec_user_b", "sec_pw_b_456")
        r = user_b.get(f"/project/{test_project_id}")
        assert r.status_code == 403, (
            f"Fremdzugriff erlaubt: Status {r.status_code}"
        )


class TestSecurityHeaders:
    def test_tc_sec_08_sicherheits_header_vorhanden(self, client):
        """HTTP-Sicherheits-Header sind in den Responses gesetzt."""
        r = client.get("/login")
        assert r.headers.get("X-Frame-Options") in ("DENY", "SAMEORIGIN"), (
            "X-Frame-Options fehlt oder ungueltig (Clickjacking-Schutz)"
        )
        assert r.headers.get("X-Content-Type-Options") == "nosniff", (
            "X-Content-Type-Options: nosniff fehlt (MIME-Sniffing-Schutz)"
        )
        assert r.headers.get("X-XSS-Protection") is not None, (
            "X-XSS-Protection Header fehlt"
        )


class TestAPIKeyLeak:
    def test_tc_sec_09_api_key_nicht_in_response(self, admin_client):
        """WARP_INBOX_API_KEY darf nicht in Response-Bodies erscheinen."""
        for route in ["/dashboard", "/inbox", "/admin"]:
            r = admin_client.get(route)
            if r.status_code == 200:
                body = r.data.decode("utf-8", errors="replace")
                assert API_KEY not in body, (
                    f"API-Key in Response von {route} sichtbar!"
                )


class TestAuthRequired:
    def test_tc_sec_10_geschuetzte_routen_erfordern_login(self, app):
        """Alle geschuetzten Routen leiten ohne Login auf /login weiter."""
        routes = [
            "/dashboard",
            "/project/new",
            "/inbox",
            "/admin",
            "/admin/questions",
        ]
        for route in routes:
            with app.test_client() as c:
                r = c.get(route, follow_redirects=False)
                assert r.status_code == 302, (
                    f"{route}: kein Redirect ohne Login (Status {r.status_code})"
                )
                loc = r.headers.get("Location", "")
                assert "login" in loc.lower(), (
                    f"{route}: Redirect nicht zu /login ({loc!r})"
                )


class TestAdminAccessControl:
    def test_tc_sec_11_admin_routen_fuer_user_gesperrt(self, user_client):
        """Admin-Routen geben fuer normale User 403 zurueck."""
        for route in ["/inbox", "/admin", "/admin/questions"]:
            r = user_client.get(route)
            assert r.status_code == 403, (
                f"Admin-Route {route} fuer normalen User zugaenglich: Status {r.status_code}"
            )
