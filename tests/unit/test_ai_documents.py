"""
TC-DOC – KI-Dokumentgenerierung & Fortschritt
================================================
Nutzt ein gefaktes `anthropic`-Modul (sys.modules-Injektion) statt echter
API-Aufrufe – schnell, deterministisch, kein API-Guthaben nötig.

TC-DOC-01  POST /project/<id>/generate/teststrategie        → 200, .docx-Datei
TC-DOC-02  GET  /project/<id>/document/teststrategie        → erneuter Download aus DB klappt
TC-DOC-03  POST /project/<id>/generate/<unbekannter_typ>    → 404
TC-DOC-04  POST .../generate/<typ>/start + Polling          → Fortschritt läuft bis "done"
TC-DOC-05  GET  .../generate/<typ>/progress ohne Start      → status "idle"
TC-DOC-06  Fehlender ANTHROPIC_API_KEY                       → 500 mit verständlicher Fehlermeldung
"""

import sys
import time
import types

import pytest


class _FakeMessage:
    def __init__(self, text: str):
        self.content = [types.SimpleNamespace(text=text)]


class _FakeMessages:
    def create(self, **kwargs):
        # Immer eine gültige Antwort im vom Code erwarteten JSON-Format -
        # _parse_chapter_response() muss sie parsen können.
        return _FakeMessage(
            '{"intro": "Mock-Einleitung fuer diesen Testlauf.", '
            '"bullets": ["Mock-Massnahme eins.", "Mock-Massnahme zwei."]}'
        )


class _FakeAnthropicClient:
    def __init__(self, api_key=None):
        self.messages = _FakeMessages()


@pytest.fixture
def mock_anthropic():
    """Ersetzt das anthropic-Modul für die Dauer eines Tests durch ein Fake,
    das ohne Netzwerk/API-Key eine gültige Kapitel-Antwort zurückgibt."""
    fake_module = types.ModuleType("anthropic")
    fake_module.Anthropic = _FakeAnthropicClient
    original = sys.modules.get("anthropic")
    sys.modules["anthropic"] = fake_module
    yield fake_module
    if original is not None:
        sys.modules["anthropic"] = original
    else:
        del sys.modules["anthropic"]


class TestSyncGeneration:
    def test_tc_doc_01_dokument_wird_generiert(self, user_client, test_project_id, mock_anthropic):
        r = user_client.post(f"/project/{test_project_id}/generate/teststrategie")
        assert r.status_code == 200
        assert "wordprocessingml.document" in r.headers.get("Content-Type", "")
        assert "attachment" in r.headers.get("Content-Disposition", "")
        # .docx ist ein ZIP-Container, beginnt immer mit der PK-Signatur
        assert r.data[:2] == b"PK"
        assert len(r.data) > 1000

    def test_tc_doc_02_dokument_erneut_abrufbar(self, user_client, test_project_id, mock_anthropic):
        # Setzt TC-DOC-01 voraus (legt das Dokument in der DB ab)
        user_client.post(f"/project/{test_project_id}/generate/teststrategie")
        r = user_client.get(f"/project/{test_project_id}/document/teststrategie")
        assert r.status_code == 200
        assert r.data[:2] == b"PK"

    def test_tc_doc_03_unbekannter_dokumenttyp_gibt_404(self, user_client, test_project_id):
        r = user_client.post(f"/project/{test_project_id}/generate/nicht_vorhanden")
        assert r.status_code == 404


class TestAsyncGenerationUndFortschritt:
    def test_tc_doc_04_start_und_progress_laufen_bis_done(self, user_client, test_project_id, mock_anthropic):
        r = user_client.post(f"/project/{test_project_id}/generate/stufentestkonzept/start")
        assert r.status_code == 200
        assert r.get_json()["ok"] is True

        # Läuft in einem Hintergrund-Thread - auf Abschluss pollen statt eines festen sleep().
        deadline = time.time() + 20
        state = {}
        while time.time() < deadline:
            resp = user_client.get(f"/project/{test_project_id}/generate/stufentestkonzept/progress")
            state = resp.get_json()
            if state.get("status") in ("done", "error"):
                break
            time.sleep(0.2)
        assert state.get("status") == "done", f"Generierung nicht fertig geworden: {state}"
        assert state.get("total", 0) > 0
        assert state.get("done") == state.get("total")

    def test_tc_doc_05_progress_ohne_start_ist_idle(self, user_client, test_project_id):
        r = user_client.get(f"/project/{test_project_id}/generate/mastertestkonzept/progress")
        assert r.status_code == 200
        data = r.get_json()
        assert data["status"] == "idle"


class TestFehlerbehandlung:
    def test_tc_doc_06_fehlender_api_key_gibt_verstaendlichen_fehler(
        self, user_client, test_project_id, monkeypatch, mock_anthropic
    ):
        # mock_anthropic sorgt dafür, dass "import anthropic" klappt (das echte Paket
        # ist in dieser venv nicht installiert) - getestet wird gezielt der
        # api_key-Check in _build_ai_document, nicht ein ModuleNotFoundError.
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
        r = user_client.post(f"/project/{test_project_id}/generate/teststrategie")
        assert r.status_code == 500
        text = r.data.decode("utf-8", errors="replace")
        assert "ANTHROPIC_API_KEY" in text
