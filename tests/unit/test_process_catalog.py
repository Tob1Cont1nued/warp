"""
TC-PK – Fragenkatalog Deployment-Prozess
==========================================

TC-PK-01  Alle Kategorien des Prozess-Katalogs sind in der DB mit catalog_type='process'
TC-PK-02  Alle Fragen des Prozess-Katalogs sind in der DB vorhanden
TC-PK-03  Prozess-Fragen tauchen nicht im WARP-Assessment auf
TC-PK-04  Fragen-IDs sind eindeutig über alle Kataloge hinweg
"""

from app.data.questions import CATEGORIES as ASSESSMENT_CATS
from app.data.questions_process import CATEGORIES as PROC_CATS, question_count


def _all_question_ids(cats) -> list[str]:
    return [q["id"] for c in cats for q in c["questions"]]


class TestProzessKatalog:
    def test_tc_pk_01_kategorien_geladen(self, app):
        from app.models import db, Category
        with app.app_context():
            ids = set(db.session.execute(
                db.select(Category.id).where(Category.catalog_type == "process")
            ).scalars())
            assert ids == {c["id"] for c in PROC_CATS}

    def test_tc_pk_02_fragen_geladen(self, app):
        from app.models import db, Question, Category
        with app.app_context():
            count = db.session.execute(
                db.select(db.func.count(Question.id))
                .join(Category, Question.category_id == Category.id)
                .where(Category.catalog_type == "process")
            ).scalar()
            assert count == question_count()

    def test_tc_pk_03_kein_einfluss_auf_assessment(self, app):
        from app.models import db, Category
        with app.app_context():
            assessment_ids = set(db.session.execute(
                db.select(Category.id).where(Category.catalog_type == "assessment")
            ).scalars())
            assert assessment_ids == {c["id"] for c in ASSESSMENT_CATS}

    def test_tc_pk_04_ids_eindeutig(self):
        all_ids = _all_question_ids(ASSESSMENT_CATS) + _all_question_ids(PROC_CATS)
        assert len(all_ids) == len(set(all_ids))
