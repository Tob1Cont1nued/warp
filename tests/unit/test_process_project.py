"""
TC-PP – Deployment-Prozess-Projekte in der UI
==============================================

TC-PP-01  Projekt mit Typ 'process' anlegen → in DB als process gespeichert
TC-PP-02  Projektseite zeigt Prozess-Kategorien, aber keine Reifegrad-Auswahl und keinen Auswertungs-Tab
TC-PP-03  Notiz ohne Antwort-Wert wird gespeichert und nach dem Laden wieder angezeigt
TC-PP-04  Prozesskarte ist erreichbar und legt beim ersten Aufruf ein ProcessModel an
TC-PP-05  Prozesskarte ist für Assessment-Projekte nicht erreichbar (404)
TC-PP-06  Punkt anlegen, verschieben, umbenennen, löschen
TC-PP-07  Zwei Punkte werden gerichtet verbunden, Kante wird wieder gelöscht
TC-PP-08  Punkt/Kante eines anderen Projekts ist nicht über die eigene Projekt-ID erreichbar
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

    def test_tc_pp_04_prozesskarte_legt_processmodel_an(self, app, user_client):
        from app.models import ProcessModel
        pid = _create_process_project(user_client, app)
        r = user_client.get(f"/project/{pid}/prozesskarte")
        assert r.status_code == 200
        with app.app_context():
            assert db.session.execute(
                db.select(ProcessModel).where(ProcessModel.project_id == pid)
            ).scalar_one_or_none() is not None

    def test_tc_pp_05_prozesskarte_nicht_fuer_assessment(self, user_client):
        r = user_client.post(
            "/project/new",
            data={"name": "TC-PP-05 Assessmentprojekt", "catalog_type": "assessment"},
            follow_redirects=False,
        )
        pid = int(r.headers["Location"].rstrip("/").split("/")[-1])
        r2 = user_client.get(f"/project/{pid}/prozesskarte")
        assert r2.status_code == 404

    def test_tc_pp_06_punkt_crud(self, app, user_client):
        pid = _create_process_project(user_client, app)
        r = user_client.post(
            f"/project/{pid}/prozesskarte/knoten",
            json={"name": "Anforderung erstellen", "x": 100, "y": 50},
        )
        assert r.status_code == 200
        node_id = r.get_json()["node"]["id"]

        r2 = user_client.patch(
            f"/project/{pid}/prozesskarte/knoten/{node_id}",
            json={"x": 150, "y": 75, "name": "Anforderung final", "description": "Akzeptanzkriterium prüfen"},
        )
        assert r2.status_code == 200
        updated = r2.get_json()["node"]
        assert updated["x"] == 150 and updated["y"] == 75
        assert updated["name"] == "Anforderung final"
        assert updated["description"] == "Akzeptanzkriterium prüfen"

        r3 = user_client.delete(f"/project/{pid}/prozesskarte/knoten/{node_id}")
        assert r3.status_code == 200
        from app.models import ProcessStep
        with app.app_context():
            assert db.session.get(ProcessStep, node_id) is None

    def test_tc_pp_07_kante_mit_richtung_anlegen_und_loeschen(self, user_client, app):
        pid = _create_process_project(user_client, app)
        n1 = user_client.post(f"/project/{pid}/prozesskarte/knoten", json={"name": "A", "x": 0, "y": 0}).get_json()["node"]["id"]
        n2 = user_client.post(f"/project/{pid}/prozesskarte/knoten", json={"name": "B", "x": 100, "y": 0}).get_json()["node"]["id"]

        r = user_client.post(f"/project/{pid}/prozesskarte/kante", json={"from_id": n1, "to_id": n2})
        assert r.status_code == 200
        edge = r.get_json()["edge"]
        assert edge["from_id"] == n1 and edge["to_id"] == n2

        r2 = user_client.delete(f"/project/{pid}/prozesskarte/kante/{edge['id']}")
        assert r2.status_code == 200

    def test_tc_pp_08_fremdes_projekt_nicht_erreichbar(self, user_client, admin_client, app):
        pid_mine = _create_process_project(user_client, app)
        r = admin_client.post(
            "/project/new", data={"name": "Fremdes Prozessprojekt", "catalog_type": "process"}, follow_redirects=False,
        )
        pid_other = int(r.headers["Location"].rstrip("/").split("/")[-1])
        node_other = admin_client.post(
            f"/project/{pid_other}/prozesskarte/knoten", json={"name": "Fremder Punkt", "x": 0, "y": 0},
        ).get_json()["node"]["id"]

        r2 = user_client.patch(
            f"/project/{pid_mine}/prozesskarte/knoten/{node_other}", json={"x": 1, "y": 1},
        )
        assert r2.status_code == 404
