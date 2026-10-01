"""
TC-ACC – Konto & Passwort (Registrierung/Reset/Account-Einstellungen)
======================================================================

TC-ACC-01  GET  /forgot-password                     → HTTP 200
TC-ACC-02  POST /forgot-password bekannte E-Mail      → sent=True, Reset-Token in DB gesetzt
TC-ACC-03  POST /forgot-password unbekannte E-Mail    → ebenfalls sent=True (kein User-Enumeration-Leak)
TC-ACC-04  GET  /reset-password/<gültiges Token>      → HTTP 200, Formular sichtbar
TC-ACC-05  GET  /reset-password/<ungültiges Token>    → Fehlermeldung statt Formular
TC-ACC-06  POST /reset-password/<token> neues PW      → Passwort geändert, Login mit neuem PW klappt
TC-ACC-07  POST /reset-password/<abgelaufenes Token>  → Fehlermeldung statt Formular
TC-ACC-08  POST /reset-password/<token> PW < 6 Zeichen → Fehlermeldung
TC-ACC-09  GET  /account ohne Login                   → Redirect auf /login
TC-ACC-10  POST /account change_password falsches PW  → Fehlermeldung, kein Change
TC-ACC-11  POST /account change_password korrekt      → Passwort geändert
TC-ACC-12  POST /account change_email bereits vergeben → Fehlermeldung
TC-ACC-13  POST /account change_email erfolgreich     → E-Mail geändert
"""

import datetime as dt

import pytest

from tests.unit.conftest import _ensure_user, _logged_in_client


def _text(r) -> str:
    return r.data.decode("utf-8", errors="replace").lower()


def _set_email(app, username: str, email: str) -> None:
    from app.models import db, User
    with app.app_context():
        u = db.session.execute(db.select(User).where(User.username == username)).scalar_one()
        u.email = email
        db.session.commit()


def _get_reset_token(app, username: str) -> str | None:
    from app.models import db, User
    with app.app_context():
        u = db.session.execute(db.select(User).where(User.username == username)).scalar_one()
        return u.reset_token


def _expire_reset_token(app, username: str) -> None:
    from app.models import db, User
    with app.app_context():
        u = db.session.execute(db.select(User).where(User.username == username)).scalar_one()
        u.reset_token_expires = dt.datetime.utcnow() - dt.timedelta(hours=1)
        db.session.commit()


class TestForgotPassword:
    def test_tc_acc_01_forgot_password_seite_erreichbar(self, client):
        r = client.get("/forgot-password")
        assert r.status_code == 200

    def test_tc_acc_02_bekannte_email_setzt_reset_token(self, app, client):
        _ensure_user(app, "_unit_acc_fp1", "fp_pw_123")
        _set_email(app, "_unit_acc_fp1", "_unit_acc_fp1@example.com")
        r = client.post("/forgot-password", data={"email": "_unit_acc_fp1@example.com"},
                         follow_redirects=True)
        assert r.status_code == 200
        assert _get_reset_token(app, "_unit_acc_fp1") is not None

    def test_tc_acc_03_unbekannte_email_kein_enumeration_leak(self, client):
        """Dieselbe Erfolgsmeldung für unbekannte wie bekannte E-Mail - ein Client darf
        aus der Antwort nicht ableiten können, ob die Adresse existiert."""
        r = client.post("/forgot-password", data={"email": "nie_vorhanden@example.com"},
                         follow_redirects=True)
        assert r.status_code == 200
        # Die Seite darf keine Fehlermeldung ("ungültig"/"nicht gefunden") zeigen
        assert "nicht gefunden" not in _text(r)


class TestResetPassword:
    def test_tc_acc_04_gueltiges_token_zeigt_formular(self, app, client):
        _ensure_user(app, "_unit_acc_rp1", "rp_pw_123")
        _set_email(app, "_unit_acc_rp1", "_unit_acc_rp1@example.com")
        client.post("/forgot-password", data={"email": "_unit_acc_rp1@example.com"})
        token = _get_reset_token(app, "_unit_acc_rp1")
        assert token, "Kein Reset-Token gesetzt - Vorbedingung für diesen Test nicht erfüllt"
        r = client.get(f"/reset-password/{token}")
        assert r.status_code == 200
        assert "password" in _text(r) or "passwort" in _text(r)

    def test_tc_acc_05_ungueltiges_token_zeigt_fehler(self, client):
        r = client.get("/reset-password/kein-gueltiges-token-xyz")
        assert r.status_code == 200
        text = _text(r)
        assert any(kw in text for kw in ("ungültig", "abgelaufen", "invalid"))

    def test_tc_acc_06_neues_passwort_wird_gesetzt_und_login_klappt(self, app, client):
        _ensure_user(app, "_unit_acc_rp2", "alt_pw_123")
        _set_email(app, "_unit_acc_rp2", "_unit_acc_rp2@example.com")
        client.post("/forgot-password", data={"email": "_unit_acc_rp2@example.com"})
        token = _get_reset_token(app, "_unit_acc_rp2")

        r = client.post(f"/reset-password/{token}",
                         data={"password": "neu_pw_456", "password2": "neu_pw_456"},
                         follow_redirects=False)
        assert r.status_code == 302
        assert "login" in r.headers.get("Location", "").lower()

        # Mit dem neuen Passwort muss ein Login jetzt klappen
        c2 = _logged_in_client(app, "_unit_acc_rp2", "neu_pw_456")
        assert c2 is not None  # _logged_in_client asserted bereits 302 intern

    def test_tc_acc_07_abgelaufenes_token_zeigt_fehler(self, app, client):
        _ensure_user(app, "_unit_acc_rp3", "rp3_pw_123")
        _set_email(app, "_unit_acc_rp3", "_unit_acc_rp3@example.com")
        client.post("/forgot-password", data={"email": "_unit_acc_rp3@example.com"})
        token = _get_reset_token(app, "_unit_acc_rp3")
        _expire_reset_token(app, "_unit_acc_rp3")

        r = client.get(f"/reset-password/{token}")
        assert r.status_code == 200
        text = _text(r)
        assert any(kw in text for kw in ("ungültig", "abgelaufen", "invalid"))

    def test_tc_acc_08_zu_kurzes_passwort_gibt_fehler(self, app, client):
        _ensure_user(app, "_unit_acc_rp4", "rp4_pw_123")
        _set_email(app, "_unit_acc_rp4", "_unit_acc_rp4@example.com")
        client.post("/forgot-password", data={"email": "_unit_acc_rp4@example.com"})
        token = _get_reset_token(app, "_unit_acc_rp4")

        r = client.post(f"/reset-password/{token}",
                         data={"password": "abc", "password2": "abc"},
                         follow_redirects=True)
        assert r.status_code == 200
        text = _text(r)
        assert any(kw in text for kw in ("zeichen", "kurz", "mindest"))


class TestAccountSeite:
    def test_tc_acc_09_account_ohne_login_redirected(self, client):
        r = client.get("/account", follow_redirects=False)
        assert r.status_code == 302
        assert "login" in r.headers.get("Location", "").lower()

    def test_tc_acc_10_falsches_aktuelles_passwort_gibt_fehler(self, app):
        _ensure_user(app, "_unit_acc_pw1", "original_pw_123")
        c = _logged_in_client(app, "_unit_acc_pw1", "original_pw_123")
        r = c.post("/account", data={
            "action": "change_password",
            "current_password": "voellig_falsch",
            "new_password": "neues_pw_456",
            "new_password2": "neues_pw_456",
        }, follow_redirects=True)
        assert r.status_code == 200
        assert "falsch" in _text(r)
        # Altes Passwort muss weiterhin gelten
        _logged_in_client(app, "_unit_acc_pw1", "original_pw_123")

    def test_tc_acc_11_passwort_aendern_erfolgreich(self, app):
        _ensure_user(app, "_unit_acc_pw2", "original_pw_789")
        c = _logged_in_client(app, "_unit_acc_pw2", "original_pw_789")
        r = c.post("/account", data={
            "action": "change_password",
            "current_password": "original_pw_789",
            "new_password": "frisches_pw_999",
            "new_password2": "frisches_pw_999",
        }, follow_redirects=True)
        assert r.status_code == 200
        assert "erfolgreich" in _text(r)
        _logged_in_client(app, "_unit_acc_pw2", "frisches_pw_999")

    def test_tc_acc_12_email_bereits_vergeben_gibt_fehler(self, app):
        _ensure_user(app, "_unit_acc_em1", "em1_pw_123")
        _ensure_user(app, "_unit_acc_em2", "em2_pw_123")
        _set_email(app, "_unit_acc_em1", "_unit_acc_em1@example.com")
        c = _logged_in_client(app, "_unit_acc_em2", "em2_pw_123")
        r = c.post("/account", data={
            "action": "change_email",
            "current_password": "em2_pw_123",
            "new_email": "_unit_acc_em1@example.com",
        }, follow_redirects=True)
        assert r.status_code == 200
        assert "bereits verwendet" in _text(r)

    def test_tc_acc_13_email_aendern_erfolgreich(self, app):
        _ensure_user(app, "_unit_acc_em3", "em3_pw_123")
        c = _logged_in_client(app, "_unit_acc_em3", "em3_pw_123")
        r = c.post("/account", data={
            "action": "change_email",
            "current_password": "em3_pw_123",
            "new_email": "_unit_acc_em3_neu@example.com",
        }, follow_redirects=True)
        assert r.status_code == 200
        assert "erfolgreich" in _text(r)
