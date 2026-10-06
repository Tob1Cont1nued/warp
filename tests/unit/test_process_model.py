"""
TC-PZ – Prozesszwilling: Datenmodell
=====================================

TC-PZ-01  Prozessmodell mit Phasen, Schritten, Rollen und Schnittstellen anlegen
TC-PZ-02  Rolle verweist auf Vertretung
TC-PZ-03  Abhängigkeit auf externes System ohne Schritt-Referenz
TC-PZ-04  Projekt löschen entfernt Prozessmodell samt Inhalt
TC-PZ-05  Pro Projekt nur ein Prozessmodell erlaubt
TC-PZ-06  Umgebung mit Versionsständen, neuester Stand zuerst
"""

import datetime as dt

import pytest
from sqlalchemy.exc import IntegrityError

from tests.unit.conftest import _ensure_user


def _new_project(app, username: str) -> int:
    from app.models import db, User, Project
    _ensure_user(app, username, "pz_pw_123456")
    with app.app_context():
        user = db.session.execute(db.select(User).where(User.username == username)).scalar_one()
        project = Project(user_id=user.id, name="Prozess-Testprojekt")
        db.session.add(project)
        db.session.commit()
        return project.id


class TestProzessmodell:
    def test_tc_pz_01_prozessmodell_mit_inhalt_anlegen(self, app):
        from app.models import (
            db, ProcessModel, ProcessPhase, ProcessRole, ProcessStep, ProcessInterface,
        )
        project_id = _new_project(app, "_unit_pz_01")
        with app.app_context():
            model = ProcessModel(project_id=project_id)
            db.session.add(model)
            db.session.flush()

            testmanager = ProcessRole(model_id=model.id, name="Testmanager")
            team_a = ProcessRole(model_id=model.id, name="Team A")
            db.session.add_all([testmanager, team_a])
            db.session.flush()

            test_phase = ProcessPhase(model_id=model.id, name="Test", sort_order=2)
            dev_phase = ProcessPhase(model_id=model.id, name="Entwicklung", sort_order=1)
            db.session.add_all([test_phase, dev_phase])
            db.session.flush()

            db.session.add(ProcessStep(
                phase_id=test_phase.id, name="Regressionstest",
                responsible_role_id=testmanager.id, is_test_step=True, sort_order=1,
            ))
            db.session.add(ProcessStep(
                phase_id=dev_phase.id, name="Code-Review",
                responsible_role_id=team_a.id, sort_order=1,
            ))
            db.session.add(ProcessInterface(
                model_id=model.id, name="ERP-Export", source_system="ERP",
                target_system="Datawarehouse", owner_role_id=team_a.id,
            ))
            db.session.commit()

            loaded = db.session.get(ProcessModel, model.id)
            assert [p.name for p in loaded.phases] == ["Entwicklung", "Test"]
            assert [r.name for r in loaded.roles] == ["Team A", "Testmanager"]
            assert loaded.phases[1].steps[0].is_test_step is True
            assert loaded.phases[1].steps[0].responsible_role.name == "Testmanager"
            assert loaded.interfaces[0].owner_role.name == "Team A"

    def test_tc_pz_02_rolle_mit_vertretung(self, app):
        from app.models import db, ProcessModel, ProcessRole
        project_id = _new_project(app, "_unit_pz_02")
        with app.app_context():
            model = ProcessModel(project_id=project_id)
            db.session.add(model)
            db.session.flush()
            deputy = ProcessRole(model_id=model.id, name="stellv. Testmanager")
            db.session.add(deputy)
            db.session.flush()
            manager = ProcessRole(model_id=model.id, name="Testmanager", deputy_role_id=deputy.id)
            db.session.add(manager)
            db.session.commit()

            loaded = db.session.get(ProcessRole, manager.id)
            assert loaded.deputy_role.name == "stellv. Testmanager"

    def test_tc_pz_03_abhaengigkeit_auf_externes_system(self, app):
        from app.models import (
            db, ProcessModel, ProcessPhase, ProcessStep, ProcessDependency,
        )
        project_id = _new_project(app, "_unit_pz_03")
        with app.app_context():
            model = ProcessModel(project_id=project_id)
            db.session.add(model)
            db.session.flush()
            phase = ProcessPhase(model_id=model.id, name="Deployment")
            db.session.add(phase)
            db.session.flush()
            step = ProcessStep(phase_id=phase.id, name="Datenladung")
            db.session.add(step)
            db.session.flush()
            db.session.add(ProcessDependency(
                model_id=model.id, step_id=step.id, depends_on_label="Datawarehouse",
            ))
            db.session.commit()

            dep = db.session.execute(db.select(ProcessDependency)).scalars().one()
            assert dep.depends_on_step_id is None
            assert dep.depends_on_label == "Datawarehouse"

    def test_tc_pz_04_projekt_loeschen_entfernt_prozessmodell(self, app):
        from app.models import db, Project, ProcessModel, ProcessRole
        project_id = _new_project(app, "_unit_pz_04")
        with app.app_context():
            model = ProcessModel(project_id=project_id)
            db.session.add(model)
            db.session.flush()
            model_id = model.id
            db.session.add(ProcessRole(model_id=model_id, name="Betrieb"))
            db.session.commit()

            db.session.delete(db.session.get(Project, project_id))
            db.session.commit()

            assert db.session.get(ProcessModel, model_id) is None
            assert db.session.execute(
                db.select(ProcessRole).where(ProcessRole.model_id == model_id)
            ).first() is None

    def test_tc_pz_06_umgebung_mit_versionsstaenden(self, app):
        from app.models import (
            db, ProcessModel, ProcessEnvironment, ProcessEnvironmentVersion,
        )
        project_id = _new_project(app, "_unit_pz_06")
        with app.app_context():
            model = ProcessModel(project_id=project_id)
            db.session.add(model)
            db.session.flush()
            env = ProcessEnvironment(model_id=model.id, name="Testumgebung A", stage="test")
            db.session.add(env)
            db.session.flush()
            db.session.add(ProcessEnvironmentVersion(
                environment_id=env.id, version="1.2.0", deployed_at=dt.datetime(2026, 9, 1),
            ))
            db.session.add(ProcessEnvironmentVersion(
                environment_id=env.id, version="1.3.0", deployed_at=dt.datetime(2026, 9, 20),
            ))
            db.session.commit()

            loaded = db.session.get(ProcessEnvironment, env.id)
            assert [v.version for v in loaded.versions] == ["1.3.0", "1.2.0"]

    def test_tc_pz_05_ein_prozessmodell_pro_projekt(self, app):
        from app.models import db, ProcessModel
        project_id = _new_project(app, "_unit_pz_05")
        with app.app_context():
            db.session.add(ProcessModel(project_id=project_id))
            db.session.commit()
            db.session.add(ProcessModel(project_id=project_id))
            with pytest.raises(IntegrityError):
                db.session.commit()
            db.session.rollback()
