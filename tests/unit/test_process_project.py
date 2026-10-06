"""
TC-PP – Deployment-Prozess-Projekte in der UI
==============================================

TC-PP-01  Projekt mit Typ 'process' anlegen → in DB als process gespeichert
TC-PP-02  Projektseite zeigt Prozess-Kategorien, aber keine Reifegrad-Auswahl und keinen Auswertungs-Tab
TC-PP-03  Notiz ohne Antwort-Wert wird gespeichert und nach dem Laden wieder angezeigt
"""

from app.models import db, Project


def _create_process_project(user_client, app) -> int:
    r = user_client.post(
        "/project/new",
        data={"name": "TC-PP Prozessprojekt", "catalog_type": "process"},
        follow_redirects=False,
    )
    assert r.status_code == 302
    return int(r.headers["Location"].rstrip("/").split("/")[-1])


class TestDeploymentProzessProjekt:
    def test_tc_pp_01_projekt_typ_process_gespeichert(self, app, user_client):
        pid = _create_process_project(user_client, app)
        with app.app_context():
            project = db.session.get(Project, pid)
            assert project.catalog_type == "process"

    def test_tc_pp_02_seite_zeigt_prozess_fragen_ohne_reifegrad(self, app, user_client):
        pid = _create_process_project(user_client, app)
        r = user_client.get(f"/project/{pid}")
        assert r.status_code == 200
        assert "Anforderungserhebung".encode() in r.data
        assert b'data-tab="auswertung"' not in r.data
        assert b'class="js-answer"' not in r.data
        assert "Antwort im Notizfeld".encode() in r.data

    def test_tc_pp_03_notiz_ohne_antwort_wird_gespeichert(self, app, user_client):
        pid = _create_process_project(user_client, app)
        r = user_client.post(
            f"/project/{pid}/answer",
            json={"question_id": "proc-anf-1", "answer_id": None, "note": "Product Owner entscheidet"},
        )
        assert r.status_code == 200
        with app.app_context():
            project = db.session.get(Project, pid)
            assert project.notes_dict()["proc-anf-1"] == "Product Owner entscheidet"
