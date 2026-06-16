"""
WARP Tool - Flask Application

Routes:
  GET  /                               - Redirect zum letzten Projekt oder Neuanlage
  POST /project/new                    - Neues Projekt anlegen
  GET  /project/<id>                   - Fragenkatalog für ein Projekt
  POST /project/<id>/answer            - AJAX: Antwort/Notiz speichern
  POST /project/<id>/info              - AJAX: Projektinfos speichern
  POST /project/<id>/delete            - Projekt löschen
  POST /project/<id>/report/html       - HTML-Vorschau
  POST /project/<id>/report            - PDF-Download
  GET  /login                          - Login
  POST /login                          - Login verarbeiten
  GET  /register                       - Registrierung
  POST /register                       - Registrierung verarbeiten
  GET  /logout                         - Logout
  GET  /admin                          - Admin-Übersicht
  GET  /admin/questions                - Fragenkatalog verwalten
  POST /admin/question/new             - Neue Frage anlegen
  POST /admin/question/<qid>/edit      - Frage bearbeiten
  POST /admin/question/<qid>/delete    - Frage löschen
  POST /admin/category/new             - Neue Kategorie anlegen
  POST /admin/category/<cid>/edit      - Kategorie bearbeiten
  POST /admin/category/<cid>/delete    - Kategorie löschen
  POST /api/inbox                      - Webhook: IMPULSE-Nachricht empfangen (API-Key)
  GET  /api/inbox/count                - AJAX: Anzahl neuer Nachrichten
  GET  /inbox                          - Admin-Postkorb
  POST /inbox/<mid>/claim              - Nachricht übernehmen
  POST /inbox/<mid>/done               - Nachricht als erledigt markieren
  POST /inbox/<mid>/release            - Nachricht freigeben
  POST /inbox/<mid>/delete             - Nachricht löschen
"""

from __future__ import annotations

import io
import json as _json
import os
import uuid
import datetime as dt
from pathlib import Path
from collections import OrderedDict
from typing import Any, Dict, List

from flask import (
    Flask, render_template, request, send_file, abort,
    redirect, url_for, jsonify, flash,
)
from flask_login import (
    LoginManager, login_required, login_user, logout_user, current_user,
)

from .models import db, User, Project, Answer, Category, Question, InboxMessage
from .data.questions import ANSWER_OPTIONS, WARP_LEVEL_ORDER

ROOT = Path(__file__).parent.parent


# ---------------------------------------------------------------------------
# DB-Seed: Fragen aus Python-Code beim ersten Start laden
# ---------------------------------------------------------------------------

def _seed_questions_if_needed() -> None:
    from .data.questions import CATEGORIES as PY_CATS
    count = db.session.execute(
        db.select(db.func.count()).select_from(Category)
    ).scalar()
    if count and count > 0:
        return
    for sort_idx, cat_data in enumerate(PY_CATS):
        cat = Category(
            id=cat_data["id"],
            title=cat_data["title"],
            parent=cat_data["parent"],
            description=cat_data.get("description", ""),
            sort_order=sort_idx,
        )
        db.session.add(cat)
        for q_idx, q_data in enumerate(cat_data["questions"]):
            q = Question(
                id=q_data["id"],
                category_id=cat_data["id"],
                text=q_data["text"],
                hint=q_data.get("hint"),
                is_new=q_data.get("new", False),
                sort_order=q_idx,
            )
            db.session.add(q)
    db.session.commit()
    q_total = sum(len(c["questions"]) for c in PY_CATS)
    print(f"[WARP] Fragenkatalog ({q_total} Fragen, {len(PY_CATS)} Kategorien) in DB geladen.")


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "warp-dev-secret-key-change-in-production")

    db_url = os.environ.get("DATABASE_URL", f"sqlite:///{ROOT / 'warp.db'}")
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    if db_url.startswith("postgresql://") and "sslmode" not in db_url:
        db_url += "?sslmode=require"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"
    login_manager.login_message = "Bitte melden Sie sich an."

    @login_manager.user_loader
    def load_user(user_id: str):
        return db.session.get(User, int(user_id))

    with app.app_context():
        db.create_all()

        try:
            admin_user = db.session.execute(
                db.select(User).where(User.username == "admin")
            ).scalar_one_or_none()
            if not admin_user:
                default = User(username="admin", display_name="Administrator", role='superuser')
                default.set_password("warp2024")
                db.session.add(default)
                db.session.commit()
                print("[WARP] Standard-Admin erstellt: admin / warp2024")
            elif not admin_user.is_superuser:
                admin_user.role = 'superuser'
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"[WARP] Admin-Init übersprungen: {e}")

        try:
            _seed_questions_if_needed()
        except Exception as e:
            db.session.rollback()
            print(f"[WARP] Fragen-Seed übersprungen: {e}")

    score_lookup = {opt["id"]: opt["score"] for opt in ANSWER_OPTIONS}
    label_lookup = {opt["id"]: opt["label"] for opt in ANSWER_OPTIONS}

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _get_project_or_403(pid: int) -> Project:
        project = db.session.get(Project, pid)
        if not project:
            abort(403)
        if not current_user.is_superuser and project.user_id != current_user.id:
            abort(403)
        return project

    def _db_question_count() -> int:
        return db.session.execute(
            db.select(db.func.count()).select_from(Question)
        ).scalar() or 0

    def _load_categories_from_db() -> List[Dict]:
        cats = db.session.execute(
            db.select(Category).order_by(Category.sort_order)
        ).scalars().all()
        return [
            {
                "id": c.id,
                "title": c.title,
                "parent": c.parent,
                "description": c.description,
                "questions": [
                    {"id": q.id, "text": q.text, "hint": q.hint, "new": q.is_new}
                    for q in c.questions
                ],
            }
            for c in cats
        ]

    def _upsert_answer(project_id: int, question_id: str,
                       answer_id: str | None, note: str | None) -> None:
        row = db.session.execute(
            db.select(Answer).where(
                Answer.project_id == project_id,
                Answer.question_id == question_id,
            )
        ).scalar_one_or_none()
        if row:
            if answer_id is not None:
                row.answer_id = answer_id or None
            if note is not None:
                row.note = note.strip() or None
        else:
            row = Answer(
                project_id=project_id,
                question_id=question_id,
                answer_id=answer_id or None,
                note=(note.strip() if note else None),
            )
            db.session.add(row)
        db.session.commit()

    def _collect_answers(form) -> Dict[str, str]:
        out: Dict[str, str] = {}
        for key, value in form.items():
            if key.startswith("answer-") and value:
                qid = key[len("answer-"):]
                if value in score_lookup:
                    out[qid] = value
        return out

    def _collect_notes(form) -> Dict[str, str]:
        out: Dict[str, str] = {}
        for key, value in form.items():
            if key.startswith("note-"):
                qid = key[len("note-"):]
                if value.strip():
                    out[qid] = value.strip()
        return out

    def _build_report_context(form) -> Dict[str, Any]:
        LEVEL_THRESHOLD = 70

        LEVEL_NUMBERS = {
            "Stufe 2 - Managed": 2,
            "Stufe 3 - Defined": 3,
            "Stufe 4 - Measured": 4,
            "Stufe 5 - Optimization": 5,
        }

        answers = _collect_answers(form)
        notes = _collect_notes(form)
        project_name = form.get("project_name", "").strip() or "Unbenannte Analyse"
        project_owner = form.get("project_owner", "").strip()
        project_date = form.get("project_date", "").strip() or dt.date.today().strftime("%d.%m.%Y")

        db_categories = _load_categories_from_db()

        level_total_map: Dict[str, int] = {
            lv: sum(len(cat["questions"]) for cat in db_categories if cat["parent"] == lv)
            for lv in WARP_LEVEL_ORDER
        }
        total_questions = _db_question_count()

        categories: List[Dict[str, Any]] = []
        all_scores_sum: float = 0.0
        level_scores_sum: Dict[str, float] = {lv: 0.0 for lv in WARP_LEVEL_ORDER}

        for cat in db_categories:
            cat_scores_sum: float = 0.0
            cat_questions: List[Dict[str, Any]] = []
            answered = 0
            distribution: "OrderedDict[str, int]" = OrderedDict(
                (opt["id"], 0) for opt in ANSWER_OPTIONS
            )

            for q in cat["questions"]:
                aid = answers.get(q["id"])
                if aid:
                    answered += 1
                    distribution[aid] += 1
                    score = score_lookup[aid]
                    cat_scores_sum += score
                    all_scores_sum += score
                    level_scores_sum[cat["parent"]] += score

                cat_questions.append({
                    "id": q["id"],
                    "text": q["text"],
                    "hint": q.get("hint"),
                    "answer_id": aid,
                    "answer_label": label_lookup.get(aid),
                    "score": score_lookup.get(aid),
                    "note": notes.get(q["id"], ""),
                })

            cat_total = len(cat["questions"])
            cat_avg = cat_scores_sum / cat_total if cat_total > 0 else 0.0
            categories.append({
                "id": cat["id"],
                "title": cat["title"],
                "description": cat["description"],
                "parent": cat["parent"],
                "questions": cat_questions,
                "answered": answered,
                "total": cat_total,
                "score": round(cat_avg, 1),
                "distribution": [
                    {"id": opt["id"], "label": opt["label"], "count": distribution[opt["id"]]}
                    for opt in ANSWER_OPTIONS
                ],
            })

        overall = round(all_scores_sum / total_questions, 1) if total_questions > 0 else 0.0
        answered_count = sum(c["answered"] for c in categories)

        warp_levels: List[Dict[str, Any]] = [{
            "number": 1, "name": "Initial", "full_name": "Stufe 1 – Initial",
            "score": None, "categories": [], "achieved": True,
        }]
        all_lower_achieved = True
        for level_name in WARP_LEVEL_ORDER:
            lv_total = level_total_map.get(level_name, 0)
            lv_score = round(level_scores_sum[level_name] / lv_total, 1) if lv_total > 0 else 0.0
            lv_cats = [c for c in categories if c["parent"] == level_name]
            num = LEVEL_NUMBERS[level_name]
            short_name = level_name.split(" - ")[1]
            achieved = all_lower_achieved and (lv_score >= LEVEL_THRESHOLD)
            if not achieved:
                all_lower_achieved = False
            warp_levels.append({
                "number": num, "name": short_name,
                "full_name": level_name.replace(" - ", " – "),
                "score": lv_score, "categories": lv_cats, "achieved": achieved,
            })

        warp_level_reached = max(ld["number"] for ld in warp_levels if ld["achieved"])
        warp_level_label = next(ld["full_name"] for ld in warp_levels if ld["number"] == warp_level_reached)

        return {
            "project_name": project_name,
            "project_owner": project_owner,
            "project_date": project_date,
            "generated_at": dt.datetime.now().strftime("%d.%m.%Y, %H:%M"),
            "categories": categories,
            "overall_score": overall,
            "answered_count": answered_count,
            "total_count": total_questions,
            "maturity_label": warp_level_label,
            "maturity_index": warp_level_reached,
            "warp_levels": warp_levels,
            "warp_level_reached": warp_level_reached,
            "level_threshold": LEVEL_THRESHOLD,
            "answer_options": ANSWER_OPTIONS,
        }

    # ------------------------------------------------------------------
    # Auth Routes
    # ------------------------------------------------------------------

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        error = None
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            display_name = request.form.get("display_name", "").strip()
            password = request.form.get("password", "")
            password2 = request.form.get("password2", "")
            if not username:
                error = "Benutzername darf nicht leer sein."
            elif len(password) < 6:
                error = "Passwort muss mindestens 6 Zeichen haben."
            elif password != password2:
                error = "Passwörter stimmen nicht überein."
            else:
                existing = db.session.execute(
                    db.select(User).where(User.username == username)
                ).scalar_one_or_none()
                if existing:
                    error = f"Benutzername '{username}' ist bereits vergeben."
                else:
                    u = User(username=username, display_name=display_name or None)
                    u.set_password(password)
                    db.session.add(u)
                    db.session.commit()
                    login_user(u)
                    return redirect(url_for("index"))
        return render_template("register.html", error=error)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        error = None
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            user = db.session.execute(
                db.select(User).where(User.username == username)
            ).scalar_one_or_none()
            if user and user.check_password(password):
                if user.is_locked:
                    error = "Ihr Konto wurde gesperrt. Bitte wenden Sie sich an den Administrator."
                else:
                    login_user(user)
                    next_page = request.args.get("next", "")
                    if not next_page.startswith("/"):
                        next_page = url_for("index")
                    return redirect(next_page)
            elif not error:
                error = "Ungültiger Benutzername oder Passwort."
        return render_template("login.html", error=error)

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("login"))

    # ------------------------------------------------------------------
    # Project Routes
    # ------------------------------------------------------------------

    @app.route("/")
    @login_required
    def index():
        if current_user.is_superuser:
            return redirect(url_for("admin_overview"))
        if current_user.is_admin:
            return redirect(url_for("inbox"))
        projects = current_user.projects
        if projects:
            return redirect(url_for("questionnaire", pid=projects[0].id))
        return redirect(url_for("new_project"))

    @app.route("/admin")
    @login_required
    def admin_overview():
        if not current_user.is_superuser:
            abort(403)
        users = db.session.execute(
            db.select(User).where(User.id != current_user.id).order_by(User.id)
        ).scalars().all()
        return render_template("admin.html", users=users, total_questions=_db_question_count())

    @app.route("/admin/user/new", methods=["POST"])
    @login_required
    def admin_user_new():
        if not current_user.is_superuser:
            abort(403)
        username = request.form.get("username", "").strip()
        display_name = request.form.get("display_name", "").strip()
        password = request.form.get("password", "").strip()
        role = request.form.get("role", "user")
        if role not in ('user', 'admin', 'superuser'):
            role = 'user'
        error = None
        if not username or not password:
            error = "Benutzername und Passwort sind erforderlich."
        elif len(password) < 6:
            error = "Passwort muss mindestens 6 Zeichen haben."
        else:
            existing = db.session.execute(
                db.select(User).where(User.username == username)
            ).scalar_one_or_none()
            if existing:
                error = f"Benutzername '{username}' ist bereits vergeben."
        if error:
            users = db.session.execute(
                db.select(User).where(User.id != current_user.id).order_by(User.id)
            ).scalars().all()
            return render_template("admin.html", users=users,
                                   total_questions=_db_question_count(), error=error)
        u = User(username=username, display_name=display_name or None, role=role)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        return redirect(url_for("admin_overview"))

    @app.route("/admin/user/<int:uid>/set-role", methods=["POST"])
    @login_required
    def admin_user_set_role(uid: int):
        if not current_user.is_superuser:
            abort(403)
        if uid == current_user.id:
            abort(400)
        user = db.session.get(User, uid)
        if not user:
            abort(404)
        new_role = request.form.get("role", "user")
        if new_role not in ('user', 'admin', 'superuser'):
            abort(400)
        user.role = new_role
        db.session.commit()
        return redirect(url_for("admin_overview"))

    @app.route("/admin/user/<int:uid>/delete", methods=["POST"])
    @login_required
    def admin_user_delete(uid: int):
        if not current_user.is_superuser:
            abort(403)
        if uid == current_user.id:
            abort(400)
        user = db.session.get(User, uid)
        if not user:
            abort(404)
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("admin_overview"))

    @app.route("/admin/user/<int:uid>/toggle-lock", methods=["POST"])
    @login_required
    def admin_user_toggle_lock(uid: int):
        if not current_user.is_superuser:
            abort(403)
        if uid == current_user.id:
            abort(400)
        user = db.session.get(User, uid)
        if not user:
            abort(404)
        user.is_locked = not user.is_locked
        db.session.commit()
        return redirect(url_for("admin_overview"))

    # ------------------------------------------------------------------
    # Admin – Fragenkatalog
    # ------------------------------------------------------------------

    @app.route("/admin/questions")
    @login_required
    def admin_questions():
        if not current_user.is_superuser:
            abort(403)
        cats = db.session.execute(
            db.select(Category).order_by(Category.sort_order)
        ).scalars().all()
        return render_template(
            "admin_questions.html",
            categories=cats,
            levels=WARP_LEVEL_ORDER,
            total_questions=_db_question_count(),
        )

    @app.route("/admin/question/new", methods=["POST"])
    @login_required
    def admin_question_new():
        if not current_user.is_superuser:
            abort(403)
        category_id = request.form.get("category_id", "").strip()
        text = request.form.get("text", "").strip()
        hint = request.form.get("hint", "").strip() or None
        if not category_id or not text:
            flash("Fragetext darf nicht leer sein.", "error")
            return redirect(url_for("admin_questions"))
        cat = db.session.get(Category, category_id)
        if not cat:
            abort(404)
        max_sort = db.session.execute(
            db.select(db.func.max(Question.sort_order)).where(
                Question.category_id == category_id
            )
        ).scalar()
        new_sort = (max_sort or 0) + 1
        new_id = f"{category_id}-{uuid.uuid4().hex[:6]}"
        q = Question(
            id=new_id,
            category_id=category_id,
            text=text,
            hint=hint,
            sort_order=new_sort,
        )
        db.session.add(q)
        db.session.commit()
        flash("Frage erfolgreich hinzugefügt.", "success")
        return redirect(url_for("admin_questions") + f"#{category_id}")

    @app.route("/admin/question/<qid>/edit", methods=["POST"])
    @login_required
    def admin_question_edit(qid: str):
        if not current_user.is_superuser:
            abort(403)
        q = db.session.get(Question, qid)
        if not q:
            abort(404)
        new_text = request.form.get("text", "").strip()
        if new_text:
            q.text = new_text
        q.hint = request.form.get("hint", "").strip() or None
        db.session.commit()
        flash("Frage gespeichert.", "success")
        return redirect(url_for("admin_questions") + f"#{q.category_id}")

    @app.route("/admin/question/<qid>/delete", methods=["POST"])
    @login_required
    def admin_question_delete(qid: str):
        if not current_user.is_superuser:
            abort(403)
        q = db.session.get(Question, qid)
        if q:
            cat_id = q.category_id
            db.session.delete(q)
            db.session.commit()
            flash("Frage gelöscht.", "success")
            return redirect(url_for("admin_questions") + f"#{cat_id}")
        return redirect(url_for("admin_questions"))

    @app.route("/admin/category/new", methods=["POST"])
    @login_required
    def admin_category_new():
        if not current_user.is_superuser:
            abort(403)
        cat_id = request.form.get("id", "").strip()
        title = request.form.get("title", "").strip()
        parent = request.form.get("parent", "").strip()
        description = request.form.get("description", "").strip() or None
        if not cat_id or not title or not parent:
            flash("ID, Titel und Stufe sind Pflichtfelder.", "error")
            return redirect(url_for("admin_questions"))
        if db.session.get(Category, cat_id):
            flash(f"Kategorie-ID '{cat_id}' ist bereits vergeben.", "error")
            return redirect(url_for("admin_questions"))
        if parent not in WARP_LEVEL_ORDER:
            flash("Ungültige WARP-Stufe.", "error")
            return redirect(url_for("admin_questions"))
        max_sort = db.session.execute(
            db.select(db.func.max(Category.sort_order))
        ).scalar()
        cat = Category(
            id=cat_id,
            title=title,
            parent=parent,
            description=description,
            sort_order=(max_sort or 0) + 1,
        )
        db.session.add(cat)
        db.session.commit()
        flash(f"Kategorie '{title}' erfolgreich angelegt.", "success")
        return redirect(url_for("admin_questions") + f"#{cat_id}")

    @app.route("/admin/category/<cid>/edit", methods=["POST"])
    @login_required
    def admin_category_edit(cid: str):
        if not current_user.is_superuser:
            abort(403)
        cat = db.session.get(Category, cid)
        if not cat:
            abort(404)
        new_title = request.form.get("title", "").strip()
        if new_title:
            cat.title = new_title
        cat.description = request.form.get("description", "").strip() or None
        db.session.commit()
        flash("Kategorie gespeichert.", "success")
        return redirect(url_for("admin_questions") + f"#{cid}")

    @app.route("/admin/category/<cid>/delete", methods=["POST"])
    @login_required
    def admin_category_delete(cid: str):
        if not current_user.is_superuser:
            abort(403)
        cat = db.session.get(Category, cid)
        if cat:
            db.session.delete(cat)
            db.session.commit()
            flash("Kategorie und alle zugehörigen Fragen gelöscht.", "success")
        return redirect(url_for("admin_questions"))

    # ------------------------------------------------------------------
    # Project Routes
    # ------------------------------------------------------------------

    @app.route("/project/new", methods=["GET", "POST"])
    @login_required
    def new_project():
        if current_user.is_superuser:
            return redirect(url_for("admin_overview"))
        if current_user.is_admin:
            return redirect(url_for("inbox"))
        if request.method == "POST":
            name = request.form.get("name", "").strip() or "Neues Projekt"
            project = Project(
                user_id=current_user.id,
                name=name,
                date=dt.date.today().strftime("%Y-%m-%d"),
            )
            db.session.add(project)
            db.session.commit()
            return redirect(url_for("questionnaire", pid=project.id))
        return render_template("new_project.html", projects=current_user.projects)

    @app.route("/project/<int:pid>")
    @login_required
    def questionnaire(pid: int):
        project = _get_project_or_403(pid)
        projects = current_user.projects
        return render_template(
            "index.html",
            project=project,
            projects=projects,
            saved_answers=project.answers_dict(),
            saved_notes=project.notes_dict(),
            categories=_load_categories_from_db(),
            answer_options=ANSWER_OPTIONS,
            total_questions=_db_question_count(),
            today=dt.date.today().strftime("%Y-%m-%d"),
        )

    @app.route("/project/<int:pid>/answer", methods=["POST"])
    @login_required
    def save_answer(pid: int):
        project = _get_project_or_403(pid)
        data = request.get_json(silent=True) or {}
        question_id = data.get("question_id", "")
        answer_id = data.get("answer_id")
        note = data.get("note")
        if not question_id:
            return jsonify({"ok": False}), 400
        _upsert_answer(project.id, question_id, answer_id, note)
        return jsonify({"ok": True})

    @app.route("/project/<int:pid>/info", methods=["POST"])
    @login_required
    def save_project_info(pid: int):
        project = _get_project_or_403(pid)
        data = request.get_json(silent=True) or {}
        if "name" in data:
            project.name = data["name"].strip() or "Neues Projekt"
        if "owner" in data:
            project.owner = data["owner"].strip() or None
        if "date" in data:
            project.date = data["date"] or None
        db.session.commit()
        return jsonify({"ok": True})

    @app.route("/project/<int:pid>/delete", methods=["POST"])
    @login_required
    def delete_project(pid: int):
        project = _get_project_or_403(pid)
        db.session.delete(project)
        db.session.commit()
        if current_user.is_superuser:
            return redirect(url_for("admin_overview"))
        if current_user.is_admin:
            return redirect(url_for("inbox"))
        remaining = current_user.projects
        if remaining:
            return redirect(url_for("questionnaire", pid=remaining[0].id))
        return redirect(url_for("new_project"))

    @app.route("/project/<int:pid>/report/html", methods=["POST"])
    @login_required
    def project_report_html(pid: int):
        project = _get_project_or_403(pid)
        ctx = _build_report_context(project.to_form_dict())
        return render_template("report.html", **ctx)

    @app.route("/project/<int:pid>/report", methods=["POST"])
    @login_required
    def project_report_pdf(pid: int):
        try:
            from weasyprint import HTML  # type: ignore
        except ImportError:
            abort(500, description="WeasyPrint ist nicht installiert.")

        project = _get_project_or_403(pid)
        ctx = _build_report_context(project.to_form_dict())
        html = render_template("report.html", **ctx)
        pdf_bytes = HTML(string=html, base_url=request.host_url).write_pdf()
        filename = f"WARP_Report_{project.name.replace(' ', '_')}_{dt.date.today().isoformat()}.pdf"
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=filename,
        )

    # ------------------------------------------------------------------
    # KI-Dokumentgenerierung
    # ------------------------------------------------------------------

    _DOC_TEMPLATES = {
        'teststrategie':     'WARP_Teststrategie.docx',
        'mastertestkonzept': 'WARP_Mastertestkonzept.docx',
        'stufentestkonzept': 'WARP_Stufentestkonzept.docx',
    }
    _DOC_LABELS = {
        'teststrategie':     'Teststrategie',
        'mastertestkonzept': 'Mastertestkonzept',
        'stufentestkonzept': 'Stufentestkonzept',
    }

    def _build_ai_document(project: Project, doc_type: str) -> tuple[io.BytesIO, str]:
        import json as _json2
        import anthropic
        from docx import Document as DocxDoc
        from docx.oxml import OxmlElement
        from docx.oxml.ns import qn as _qn

        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY ist nicht gesetzt.")

        answers = project.answers_dict()
        notes   = project.notes_dict()
        db_cats = _load_categories_from_db()

        label_lookup = {opt["id"]: opt["label"] for opt in ANSWER_OPTIONS}
        cat_lines, strengths, improvements = [], [], []
        weak_questions: list[str] = []

        for cat in db_cats:
            scores = [score_lookup.get(answers.get(q['id'], ''), 0) for q in cat['questions']]
            answered = [s for q, s in zip(cat['questions'], scores) if answers.get(q['id'])]
            if not answered:
                continue
            pct = round(sum(scores) / (len(cat['questions']) * 100) * 100)
            cat_lines.append(f"  - {cat['title']} ({cat['parent']}): {pct}%")
            if pct >= 70:
                strengths.append(cat['title'])
            elif pct < 40:
                improvements.append(cat['title'])
            for q in cat['questions']:
                ans_id = answers.get(q['id'], '')
                score  = score_lookup.get(ans_id, 0)
                note   = notes.get(q['id'], '')
                if ans_id and score < 50:
                    line = f"    [{cat['title']}] {q['text'][:110]} → {label_lookup.get(ans_id, ans_id)}"
                    if note:
                        line += f" | Notiz: {note[:80]}"
                    weak_questions.append(line)

        # Kapitelstruktur aus der Vorlage lesen
        tpl_path = ROOT / "app" / "static" / "docs" / _DOC_TEMPLATES[doc_type]
        doc = DocxDoc(str(tpl_path))
        sections: list[tuple[str, str]] = []
        cur_head = cur_desc = None
        for para in doc.paragraphs:
            if para.style.name == 'Heading 1':
                if cur_head:
                    sections.append((cur_head, cur_desc or ''))
                cur_head, cur_desc = para.text.strip(), None
            elif para.style.name == 'Normal' and cur_head and cur_desc is None:
                cur_desc = para.text.strip()
        if cur_head:
            sections.append((cur_head, cur_desc or ''))

        sections_desc = '\n'.join(f'- "{h}": {d}' for h, d in sections)
        sections_json = '\n'.join(
            f'  "{h}": {{"intro": "...", "bullets": ["...", "...", "..."]}}'
            for h, _ in sections
        )

        context = (
            f"Projekt: {project.name}\n"
            f"Verantwortliche/r: {project.owner or 'nicht angegeben'}\n"
            f"Datum: {project.date or 'nicht angegeben'}\n\n"
            f"WARP-Kategorie-Scores (Erfüllungsgrad je Prozessbereich):\n"
            + ('\n'.join(cat_lines) or '  (keine Antworten)')
            + f"\n\nStärken (≥70 %): {', '.join(strengths) or '—'}\n"
            f"Handlungsfelder (<40 %): {', '.join(improvements) or '—'}"
        )

        weak_ctx = (
            "\n\nEinzelfragen mit Handlungsbedarf (Score <50 %):\n"
            + '\n'.join(weak_questions[:40])
        ) if weak_questions else ""

        prompt = f"""Du bist ein erfahrener Testmanagement-Berater bei Wavestone und erstellst auf Basis \
eines WARP-Reifegradassessments ein professionelles Beratungsdokument.

ASSESSMENT-ERGEBNISSE:
{context}{weak_ctx}

DOKUMENT-TYP: {_DOC_LABELS[doc_type]}

ANFORDERUNGEN PRO KAPITEL:
- Schreibe einen einleitenden Fließtext-Absatz (3–5 Sätze), der den Ist-Zustand des Projekts \
bewertet und die Relevanz des Kapitels begründet. Beziehe dich konkret auf die Score-Werte.
- Erstelle 5–8 handlungsorientierte Aufzählungspunkte. Jeder Punkt soll eine konkrete Maßnahme, \
Methode oder Empfehlung beschreiben – nicht nur benennen, sondern kurz erläutern WAS, WIE und WARUM.
- Verwende präzise Fachbegriffe aus dem Testmanagement (z. B. risikobasiertes Testen, \
Äquivalenzklassen, Grenzwertanalyse, Shift-Left, exploratives Testen, kontinuierliche Integration, \
Test Coverage, Defect-Escape-Rate, Regressionsstrategie, RACI, Testautomatisierungspyramide usw.).
- Bleibe tool-agnostisch: beschreibe Tool-KATEGORIEN mit Funktion und Integrationsbedarf, \
nenne wenn hilfreich bekannte Vertreter als Beispiele in Klammern (z. B. „Testmanagement-Tool \
(z. B. Azure DevOps, Jira/Xray)"), schreibe aber keine Produktempfehlung.
- Leite alle Inhalte aus den Assessment-Scores ab: Stärken festigen, Handlungsfelder konkret adressieren.
- Sprache: professionelles Deutsch, formeller Beratungsstil, aktive Formulierungen.

KAPITEL-BESCHREIBUNGEN AUS DER VORLAGE:
{sections_desc}

Antworte AUSSCHLIESSLICH mit validem JSON, ohne Erklärungen oder Markdown-Blöcke:
{{
{sections_json}
}}"""

        client = anthropic.Anthropic(api_key=api_key)
        msg = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=8192,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = msg.content[0].text.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        content: dict = _json2.loads(raw.strip())

        # Hilfsfunktion: neuen Absatz direkt nach einem XML-Element einfügen
        def _insert_para_after(ref_p_xml, text: str, indent: bool = False):
            new_p = OxmlElement('w:p')
            if indent:
                pPr = OxmlElement('w:pPr')
                ind = OxmlElement('w:ind')
                ind.set(_qn('w:left'), '360')
                pPr.append(ind)
                new_p.append(pPr)
            r = OxmlElement('w:r')
            t = OxmlElement('w:t')
            t.text = text
            t.set(_qn('xml:space'), 'preserve')
            r.append(t)
            new_p.append(r)
            ref_p_xml.addnext(new_p)
            return new_p

        # Vorlage befüllen: Intro in Normal-Absatz, Bullets als eingefügte Absätze
        # list() einmalig auswerten – neu eingefügte Elemente sollen nicht mititeriert werden
        filled: set[str] = set()
        cur_head = None
        for para in list(doc.paragraphs):
            if para.style.name == 'Heading 1':
                cur_head = para.text.strip()
            elif para.style.name == 'Normal' and cur_head and cur_head not in filled:
                chapter_data = content.get(cur_head)
                if not chapter_data:
                    continue
                intro   = chapter_data.get('intro', '') if isinstance(chapter_data, dict) else str(chapter_data)
                bullets = chapter_data.get('bullets', []) if isinstance(chapter_data, dict) else []

                # Intro in bestehenden Normal-Absatz schreiben
                for run in para.runs:
                    run.text = ''
                if para.runs:
                    para.runs[0].text = intro
                else:
                    para.add_run(intro)

                # Bullets als neue Absätze nach dem Intro einfügen (umgekehrte Reihenfolge wegen addnext)
                last_xml = para._p
                for bullet in bullets:
                    new_xml = _insert_para_after(last_xml, f'•  {bullet}', indent=True)
                    last_xml = new_xml

                filled.add(cur_head)

        buf = io.BytesIO()
        doc.save(buf)
        buf.seek(0)
        label  = _DOC_LABELS[doc_type]
        fname  = f"WARP_{label}_{project.name.replace(' ', '_')}.docx"
        return buf, fname

    @app.route("/project/<int:pid>/generate/<doc_type>", methods=["POST"])
    @login_required
    def generate_document(pid: int, doc_type: str):
        if doc_type not in _DOC_TEMPLATES:
            abort(404)
        project = _get_project_or_403(pid)
        try:
            buf, fname = _build_ai_document(project, doc_type)
            return send_file(
                buf,
                mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                as_attachment=True,
                download_name=fname,
            )
        except ValueError as exc:
            return render_template("error.html", message=str(exc)), 500
        except Exception as exc:
            import traceback
            print(traceback.format_exc())
            return render_template("error.html", message=f"Generierung fehlgeschlagen: {exc}"), 500

    # ------------------------------------------------------------------
    # Inbox – Webhook + Admin-Postkorb
    # ------------------------------------------------------------------

    @app.route("/api/inbox", methods=["POST"])
    def api_inbox_receive():
        api_key = os.environ.get("WARP_INBOX_API_KEY", "")
        if api_key:
            provided = request.headers.get("X-API-Key", "")
            if not provided or provided != api_key:
                return jsonify({"error": "Unauthorized"}), 401
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400
        user_name = data.get("userName", "").strip()
        user_email = data.get("userEmail", "").strip()
        recommendation = data.get("recommendation", "").strip()
        if not user_name or not user_email or not recommendation:
            return jsonify({"error": "Missing required fields: userName, userEmail, recommendation"}), 400
        msg = InboxMessage(
            source=data.get("source", "IMPULSE"),
            user_name=user_name,
            user_email=user_email,
            recommendation=recommendation,
            scores_json=_json.dumps(data.get("scores", {})),
            rationale=data.get("rationale", ""),
            top_factors_json=_json.dumps(data.get("topFactors", [])),
            maturity=data.get("maturity"),
            contact_pref=data.get("contactPref"),
            contact_phone=data.get("contactPhone"),
        )
        db.session.add(msg)
        db.session.commit()
        print(f"[WARP Postkorb] Neue Anfrage von {user_name} ({user_email}): {recommendation}")
        return jsonify({"ok": True, "id": msg.id}), 201

    @app.route("/api/inbox/count")
    @login_required
    def api_inbox_count():
        if not current_user.is_admin:
            return jsonify({"count": 0})
        count = db.session.execute(
            db.select(db.func.count()).select_from(InboxMessage).where(
                InboxMessage.status == "neu"
            )
        ).scalar() or 0
        return jsonify({"count": count})

    @app.route("/inbox")
    @login_required
    def inbox():
        if not current_user.is_admin:
            abort(403)
        messages = db.session.execute(
            db.select(InboxMessage).order_by(InboxMessage.received_at.desc())
        ).scalars().all()
        for m in messages:
            m.scores = _json.loads(m.scores_json or "{}")
            m.top_factors = _json.loads(m.top_factors_json or "[]")
        neu_count = sum(1 for m in messages if m.status == "neu")
        admins = db.session.execute(
            db.select(User).where(User.role.in_(['admin', 'superuser']))
            .order_by(User.display_name)
        ).scalars().all()
        return render_template("inbox.html", messages=messages, neu_count=neu_count, admins=admins)

    @app.route("/inbox/<int:mid>/assign", methods=["POST"])
    @login_required
    def inbox_assign(mid: int):
        if not current_user.is_admin:
            abort(403)
        msg = db.session.get(InboxMessage, mid)
        if not msg:
            abort(404)
        try:
            assignee_id = int(request.form.get("assignee_id", 0))
        except ValueError:
            abort(400)
        assignee = db.session.get(User, assignee_id)
        if not assignee or not assignee.is_admin:
            abort(400)
        msg.status = "in_bearbeitung"
        msg.claimed_by_id = assignee_id
        msg.claimed_at = dt.datetime.utcnow()
        db.session.commit()
        return redirect(url_for("inbox"))

    @app.route("/inbox/<int:mid>/claim", methods=["POST"])
    @login_required
    def inbox_claim(mid: int):
        if not current_user.is_admin:
            abort(403)
        msg = db.session.get(InboxMessage, mid)
        if not msg:
            abort(404)
        if msg.status == "neu":
            msg.status = "in_bearbeitung"
            msg.claimed_by_id = current_user.id
            msg.claimed_at = dt.datetime.utcnow()
            db.session.commit()
        return redirect(url_for("inbox"))

    @app.route("/inbox/<int:mid>/done", methods=["POST"])
    @login_required
    def inbox_done(mid: int):
        if not current_user.is_admin:
            abort(403)
        msg = db.session.get(InboxMessage, mid)
        if not msg:
            abort(404)
        msg.status = "erledigt"
        db.session.commit()
        return redirect(url_for("inbox"))

    @app.route("/inbox/<int:mid>/release", methods=["POST"])
    @login_required
    def inbox_release(mid: int):
        if not current_user.is_admin:
            abort(403)
        msg = db.session.get(InboxMessage, mid)
        if not msg:
            abort(404)
        msg.status = "neu"
        msg.claimed_by_id = None
        msg.claimed_at = None
        db.session.commit()
        return redirect(url_for("inbox"))

    @app.route("/inbox/<int:mid>/delete", methods=["POST"])
    @login_required
    def inbox_delete(mid: int):
        if not current_user.is_admin:
            abort(403)
        msg = db.session.get(InboxMessage, mid)
        if msg:
            db.session.delete(msg)
            db.session.commit()
        return redirect(url_for("inbox"))

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
