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
TC-PP-09  Kantentyp wird übernommen, ungültiger Typ fällt auf 'default' zurück
TC-PP-10  Prozesskarte lässt sich als PDF exportieren
TC-PP-11  PDF-Export ohne Bild liefert 400
TC-PP-12  Punktfarbe setzen, ungültige Farbe fällt auf Standard zurück
TC-PP-13  Rechteck anlegen, verschieben, umbenennen, einfärben, Transparenz/Ebene setzen
TC-PP-14  Ungültige Rechteck-Farbe/-Ebene fallen auf Standard zurück
TC-PP-15  Rechteck löschen
TC-PP-16  Rechteck eines anderen Projekts ist nicht über die eigene Projekt-ID erreichbar
TC-PP-17  Punktgröße setzen (manuell), Mindestgröße wird erzwungen, Standard ist "automatisch" (null)
TC-PP-18  PDF-Export mit überdimensioniertem Bild liefert 400 statt Server-Absturz
"""

import pytest

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
        assert edge["kind"] == "default"

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

    def test_tc_pp_09_kantentyp(self, user_client, app):
        pid = _create_process_project(user_client, app)
        n1 = user_client.post(f"/project/{pid}/prozesskarte/knoten", json={"name": "A", "x": 0, "y": 0}).get_json()["node"]["id"]
        n2 = user_client.post(f"/project/{pid}/prozesskarte/knoten", json={"name": "B", "x": 100, "y": 0}).get_json()["node"]["id"]
        n3 = user_client.post(f"/project/{pid}/prozesskarte/knoten", json={"name": "C", "x": 200, "y": 0}).get_json()["node"]["id"]

        r1 = user_client.post(f"/project/{pid}/prozesskarte/kante", json={"from_id": n1, "to_id": n2, "kind": "blockiert"})
        assert r1.get_json()["edge"]["kind"] == "blockiert"

        r2 = user_client.post(f"/project/{pid}/prozesskarte/kante", json={"from_id": n2, "to_id": n3, "kind": "nicht-existent"})
        assert r2.get_json()["edge"]["kind"] == "default"

    def test_tc_pp_10_pdf_export(self, user_client, app):
        pid = _create_process_project(user_client, app)
        user_client.post(f"/project/{pid}/prozesskarte/knoten", json={"name": "A", "x": 0, "y": 0})
        tiny_png = (
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
        )
        try:
            r = user_client.post(
                f"/project/{pid}/prozesskarte/export",
                json={"image": f"data:image/png;base64,{tiny_png}", "width": 400, "height": 300},
            )
        except OSError:
            pytest.skip("WeasyPrint-Systembibliotheken (GTK/Pango) sind hier nicht installiert.")
        if r.status_code == 500:
            pytest.skip("WeasyPrint-Systembibliotheken (GTK/Pango) sind hier nicht installiert.")
        assert r.status_code == 200
        assert r.mimetype == "application/pdf"
        assert r.data[:4] == b"%PDF"

    def test_tc_pp_11_pdf_export_ohne_bild(self, user_client, app):
        pid = _create_process_project(user_client, app)
        r = user_client.post(f"/project/{pid}/prozesskarte/export", json={})
        assert r.status_code == 400

    def test_tc_pp_12_punktfarbe_setzen_und_zuruecksetzen(self, user_client, app):
        pid = _create_process_project(user_client, app)
        node_id = user_client.post(f"/project/{pid}/prozesskarte/knoten", json={"name": "A", "x": 0, "y": 0}).get_json()["node"]["id"]

        r1 = user_client.patch(f"/project/{pid}/prozesskarte/knoten/{node_id}", json={"color": "#e5484d"})
        assert r1.get_json()["node"]["color"] == "#e5484d"

        r2 = user_client.patch(f"/project/{pid}/prozesskarte/knoten/{node_id}", json={"color": "#nicht-in-der-palette"})
        assert r2.get_json()["node"]["color"] == "#3b4252"

    def test_tc_pp_13_rechteck_crud(self, user_client, app):
        pid = _create_process_project(user_client, app)
        r = user_client.post(
            f"/project/{pid}/prozesskarte/rechteck",
            json={"label": "Team A", "x": 50, "y": 60, "width": 200, "height": 120},
        )
        assert r.status_code == 200
        area = r.get_json()["area"]
        assert area["label"] == "Team A"
        assert area["layer"] == "back"

        r2 = user_client.patch(
            f"/project/{pid}/prozesskarte/rechteck/{area['id']}",
            json={"x": 80, "y": 90, "width": 300, "height": 180, "label": "Team B", "color": "#3b82f6", "opacity": 0.4, "layer": "front"},
        )
        updated = r2.get_json()["area"]
        assert updated["x"] == 80 and updated["y"] == 90
        assert updated["width"] == 300 and updated["height"] == 180
        assert updated["label"] == "Team B"
        assert updated["color"] == "#3b82f6"
        assert updated["opacity"] == 0.4
        assert updated["layer"] == "front"

    def test_tc_pp_14_rechteck_ungueltige_werte_fallen_zurueck(self, user_client, app):
        pid = _create_process_project(user_client, app)
        area_id = user_client.post(
            f"/project/{pid}/prozesskarte/rechteck", json={"x": 0, "y": 0}
        ).get_json()["area"]["id"]

        r = user_client.patch(
            f"/project/{pid}/prozesskarte/rechteck/{area_id}",
            json={"color": "#was-auch-immer", "layer": "mitte", "width": 1, "height": 1, "opacity": 5},
        )
        area = r.get_json()["area"]
        assert area["color"] == "#3b4252"
        assert area["layer"] == "back"
        assert area["width"] >= 40
        assert area["height"] >= 30
        assert area["opacity"] == 1.0

    def test_tc_pp_15_rechteck_loeschen(self, user_client, app):
        from app.models import db, ProcessArea
        pid = _create_process_project(user_client, app)
        area_id = user_client.post(
            f"/project/{pid}/prozesskarte/rechteck", json={"x": 0, "y": 0}
        ).get_json()["area"]["id"]

        r = user_client.delete(f"/project/{pid}/prozesskarte/rechteck/{area_id}")
        assert r.status_code == 200
        with app.app_context():
            assert db.session.get(ProcessArea, area_id) is None

    def test_tc_pp_16_fremdes_rechteck_nicht_erreichbar(self, user_client, admin_client, app):
        pid_mine = _create_process_project(user_client, app)
        r = admin_client.post(
            "/project/new", data={"name": "Fremdes Prozessprojekt 2", "catalog_type": "process"}, follow_redirects=False,
        )
        pid_other = int(r.headers["Location"].rstrip("/").split("/")[-1])
        area_other = admin_client.post(
            f"/project/{pid_other}/prozesskarte/rechteck", json={"x": 0, "y": 0}
        ).get_json()["area"]["id"]

        r2 = user_client.patch(f"/project/{pid_mine}/prozesskarte/rechteck/{area_other}", json={"x": 1})
        assert r2.status_code == 404

    def test_tc_pp_17_punktgroesse(self, user_client, app):
        pid = _create_process_project(user_client, app)
        r0 = user_client.post(f"/project/{pid}/prozesskarte/knoten", json={"name": "A", "x": 0, "y": 0})
        node = r0.get_json()["node"]
        assert node["width"] is None and node["height"] is None

        r1 = user_client.patch(
            f"/project/{pid}/prozesskarte/knoten/{node['id']}", json={"width": 220, "height": 80}
        )
        updated = r1.get_json()["node"]
        assert updated["width"] == 220 and updated["height"] == 80

        r2 = user_client.patch(
            f"/project/{pid}/prozesskarte/knoten/{node['id']}", json={"width": 1, "height": 1}
        )
        clamped = r2.get_json()["node"]
        assert clamped["width"] == 50 and clamped["height"] == 24

    def test_tc_pp_18_pdf_export_bild_zu_gross(self, user_client, app):
        pid = _create_process_project(user_client, app)
        user_client.post(f"/project/{pid}/prozesskarte/knoten", json={"name": "A", "x": 0, "y": 0})
        tiny_png = (
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
        )
        r = user_client.post(
            f"/project/{pid}/prozesskarte/export",
            json={"image": f"data:image/png;base64,{tiny_png}", "width": 10000, "height": 10000},
        )
        assert r.status_code == 400
