"""
TC-API – API-Endpunkte & Admin-Postkorb
=======================================

TC-API-01  POST /api/inbox gültiger API-Key   → 201, Nachricht angelegt
TC-API-02  POST /api/inbox falscher API-Key   → 401
TC-API-03  POST /api/inbox fehlendes Pflichtfeld → 400
TC-API-04  GET  /api/inbox/count (Admin)       → 200 JSON {count: N}
TC-API-05  GET  /api/inbox/count (Anon)        → 302 oder 401
TC-API-06  GET  /inbox (Admin)                 → 200
TC-API-07  GET  /inbox (normaler User)         → 403
TC-API-08  GET  /admin/questions (Superuser)   → 200
TC-API-09  GET  /coverage-matrix (Admin)       → 200
"""

import json
import os
import pytest


API_KEY = os.environ.get("WARP_INBOX_API_KEY", "test-api-key-123")

SAMPLE_PAYLOAD = {
    "userName": "API Test GmbH",
    "userEmail": "api@test.de",
    "recommendation": "WARP Assessment empfohlen",
    "scores": {"Teststrategie": 7, "Automatisierung": 4},
    "rationale": "Mittlerer Reifegrad festgestellt.",
    "top_factors": ["Fehlende Automatisierung", "Kein CI/CD"],
    "maturity": "ausbaufaehig",
}


class TestWebhook:
    def test_tc_api_01_gueltiger_api_key_erstellt_nachricht(self, client):
        r = client.post(
            "/api/inbox",
            data=json.dumps(SAMPLE_PAYLOAD),
            content_type="application/json",
            headers={"X-API-Key": API_KEY},
        )
        assert r.status_code in (200, 201), r.data

    def test_tc_api_02_falscher_api_key_gibt_401(self, client):
        r = client.post(
            "/api/inbox",
            data=json.dumps(SAMPLE_PAYLOAD),
            content_type="application/json",
            headers={"X-API-Key": "WRONG_KEY"},
        )
        assert r.status_code == 401

    def test_tc_api_03_fehlendes_pflichtfeld_gibt_400(self, client):
        payload = {"email": "nur@email.de"}
        r = client.post(
            "/api/inbox",
            data=json.dumps(payload),
            content_type="application/json",
            headers={"X-API-Key": API_KEY},
        )
        assert r.status_code in (400, 422)


class TestInboxCount:
    def test_tc_api_04_count_fuer_admin(self, admin_client):
        r = admin_client.get("/api/inbox/count")
        assert r.status_code == 200
        data = r.get_json()
        assert "count" in data
        assert isinstance(data["count"], int)

    def test_tc_api_05_count_ohne_login_redirected(self, client):
        c = client.application.test_client()
        r = c.get("/api/inbox/count", follow_redirects=False)
        assert r.status_code in (302, 401)


class TestPostkorb:
    def test_tc_api_06_inbox_fuer_admin_erreichbar(self, admin_client):
        r = admin_client.get("/inbox")
        assert r.status_code == 200

    def test_tc_api_07_inbox_fuer_user_gibt_403(self, user_client):
        r = user_client.get("/inbox")
        assert r.status_code == 403


class TestAdminRouten:
    def test_tc_api_08_questions_fuer_superuser(self, superuser_client):
        r = superuser_client.get("/admin/questions")
        assert r.status_code == 200

    def test_tc_api_09_coverage_matrix_fuer_admin(self, admin_client):
        r = admin_client.get("/coverage-matrix")
        assert r.status_code == 200
        assert b"Abdeckung" in r.data or b"coverage" in r.data.lower() or b"Testfall" in r.data
