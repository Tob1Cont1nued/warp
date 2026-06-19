"""
TC-AUTH – Authentifizierung & Autorisierung
==========================================

TC-AUTH-01  GET /login         → HTTP 200
TC-AUTH-02  GET /register      → HTTP 200
TC-AUTH-03  POST /login gültig → Redirect (302)
TC-AUTH-04  POST /login ungültig → 200 + Fehlermeldung
TC-AUTH-05  GET /logout        → Redirect auf /login
TC-AUTH-06  GET /dashboard ohne Login → Redirect auf /login
TC-AUTH-07  GET /admin ohne Login → Redirect auf /login
TC-AUTH-08  GET /admin als normaler Benutzer → 403
TC-AUTH-09  POST /register doppelter Username → Fehler
TC-AUTH-10  POST /register Passwörter stimmen nicht überein → Fehler
TC-AUTH-11  POST /register Passwort zu kurz → Fehler
"""

import pytest


class TestLoginSeite:
    def test_tc_auth_01_login_seite_erreichbar(self, client):
        r = client.get("/login")
        assert r.status_code == 200
        assert b"WARP" in r.data or b"login" in r.data.lower()

    def test_tc_auth_03_gueltiger_login_redirected(self, client):
        r = client.post(
            "/login",
            data={"username": "admin", "password": "warp2024"},
            follow_redirects=False,
        )
        assert r.status_code == 302

    def test_tc_auth_04_ungueltiges_passwort_bleibt_auf_login(self, client):
        r = client.post(
            "/login",
            data={"username": "admin", "password": "falsch_xyz"},
            follow_redirects=True,
        )
        assert r.status_code == 200
        assert b"login" in r.data.lower() or b"fehler" in r.data.lower() or b"incorrect" in r.data.lower() or b"falsch" in r.data.lower() or b"Ungültig" in r.data or b"ungültig" in r.data.lower()

    def test_tc_auth_05_logout_redirected(self, user_client):
        r = user_client.get("/logout", follow_redirects=False)
        assert r.status_code == 302


class TestRegisterSeite:
    def test_tc_auth_02_register_seite_erreichbar(self, client):
        r = client.get("/register")
        assert r.status_code == 200

    def test_tc_auth_09_doppelter_username_gibt_fehler(self, client):
        r = client.post(
            "/register",
            data={
                "username": "admin",
                "display_name": "Duplikat",
                "password": "sicher123",
                "password2": "sicher123",
            },
            follow_redirects=True,
        )
        assert r.status_code == 200
        assert b"vergeben" in r.data or b"exist" in r.data.lower()

    def test_tc_auth_10_passwort_mismatch_gibt_fehler(self, client):
        r = client.post(
            "/register",
            data={
                "username": "_unit_pw_mismatch",
                "display_name": "Test",
                "password": "passwort1",
                "password2": "passwort2",
            },
            follow_redirects=True,
        )
        assert r.status_code == 200
        assert b"überein" in r.data or b"match" in r.data.lower() or b"stimm" in r.data.lower()

    def test_tc_auth_11_passwort_zu_kurz_gibt_fehler(self, client):
        r = client.post(
            "/register",
            data={
                "username": "_unit_short_pw",
                "display_name": "Test",
                "password": "abc",
                "password2": "abc",
            },
            follow_redirects=True,
        )
        assert r.status_code == 200
        assert b"Zeichen" in r.data or b"kurz" in r.data.lower() or b"short" in r.data.lower()


class TestZugriffskontrolle:
    def test_tc_auth_06_dashboard_ohne_login_redirected(self, client):
        c = client.application.test_client()
        r = c.get("/dashboard", follow_redirects=False)
        assert r.status_code == 302
        assert "login" in r.headers.get("Location", "").lower()

    def test_tc_auth_07_admin_ohne_login_redirected(self, client):
        c = client.application.test_client()
        r = c.get("/admin", follow_redirects=False)
        assert r.status_code == 302
        assert "login" in r.headers.get("Location", "").lower()

    def test_tc_auth_08_admin_als_user_gibt_403(self, user_client):
        r = user_client.get("/admin")
        assert r.status_code == 403
