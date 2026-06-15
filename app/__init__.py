"""
WARP Tool - Flask Application

Routes:
  GET  /                          - Redirect zum letzten Projekt oder Neuanlage
  POST /project/new               - Neues Projekt anlegen
  GET  /project/<id>              - Fragenkatalog für ein Projekt
  POST /project/<id>/answer       - AJAX: Antwort/Notiz speichern
  POST /project/<id>/info         - AJAX: Projektinfos speichern
  POST /project/<id>/delete       - Projekt löschen
  POST /project/<id>/report/html  - HTML-Vorschau
  POST /project/<id>/report       - PDF-Download
  GET  /login                     - Login
  POST /login                     - Login verarbeiten
  GET  /register                  - Registrierung
  POST /register                  - Registrierung verarbeiten
  GET  /logout                    - Logout
"""

from __future__ import annotations

import io
import os
import datetime as dt
from pathlib import Path
from collections import OrderedDict
from typing import Any, Dict, List

from flask import (
    Flask, render_template, request, send_file, abort,
    redirect, url_for, jsonify,
)
from flask_login import (
    LoginManager, login_required, login_user, logout_user, current_user,
)

from .models import db, User, Project, Answer
from .data.questions import CATEGORIES, ANSWER_OPTIONS, TMMI_LEVEL_ORDER, total_question_count

ROOT = Path(__file__).parent.parent


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "warp-dev-secret-key-change-in-production")

    # Lokal: SQLite. Produktion (Render + Supabase): DATABASE_URL als Env-Var setzen.
    db_url = os.environ.get("DATABASE_URL", f"sqlite:///{ROOT / 'warp.db'}")
    # Render/Supabase liefern postgres://-URLs; SQLAlchemy 2.x braucht postgresql://
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # Supabase erfordert SSL; für SQLite ist diese Option irrelevant
    if not db_url.startswith("sqlite"):
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
            "connect_args": {"sslmode": "require"},
        }

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"
    login_manager.login_message = "Bitte melden Sie sich an."

    @login_manager.user_loader
    def load_user(user_id: str):
        return db.session.get(User, int(user_id))

    with app.app_context():
        # checkfirst=True ist Standard, aber bei mehreren Gunicorn-Workern kann es
        # trotzdem zu Race Conditions kommen → zusätzlicher try/except.
        try:
            db.create_all()
        except Exception:
            db.session.rollback()

        # Admin-Anlage race-condition-sicher: spezifisch nach 'admin' suchen,
        # UNIQUE-Fehler abfangen falls zwei Worker gleichzeitig versuchen zu schreiben.
        try:
            admin_user = db.session.execute(
                db.select(User).where(User.username == "admin")
            ).scalar_one_or_none()
            if not admin_user:
                default = User(username="admin", display_name="Administrator", is_admin=True)
                default.set_password("warp2024")
                db.session.add(default)
                db.session.commit()
                print("[WARP] Standard-Admin erstellt: admin / warp2024")
            elif not admin_user.is_admin:
                admin_user.is_admin = True
                db.session.commit()
        except Exception:
            db.session.rollback()

    score_lookup = {opt["id"]: opt["score"] for opt in ANSWER_OPTIONS}
    label_lookup = {opt["id"]: opt["label"] for opt in ANSWER_OPTIONS}

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _get_project_or_403(pid: int) -> Project:
        project = db.session.get(Project, pid)
        if not project:
            abort(403)
        if not current_user.is_admin and project.user_id != current_user.id:
            abort(403)
        return project

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

        # Gesamtanzahl Fragen je Stufe (Nenner für korrekte Durchschnittsberechnung)
        level_total_map: Dict[str, int] = {
            lv: sum(len(cat["questions"]) for cat in CATEGORIES if cat["parent"] == lv)
            for lv in TMMI_LEVEL_ORDER
        }
        total_questions = total_question_count()

        categories: List[Dict[str, Any]] = []
        all_scores_sum: float = 0.0
        level_scores_sum: Dict[str, float] = {lv: 0.0 for lv in TMMI_LEVEL_ORDER}

        for cat in CATEGORIES:
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

            # Dividiere durch Gesamtfragen der Kategorie (nicht nur beantwortete)
            cat_avg = cat_scores_sum / len(cat["questions"])
            categories.append({
                "id": cat["id"],
                "title": cat["title"],
                "description": cat["description"],
                "parent": cat["parent"],
                "questions": cat_questions,
                "answered": answered,
                "total": len(cat["questions"]),
                "score": round(cat_avg, 1),
                "distribution": [
                    {"id": opt["id"], "label": opt["label"], "count": distribution[opt["id"]]}
                    for opt in ANSWER_OPTIONS
                ],
            })

        # Dividiere durch alle Fragen (nicht nur beantwortete)
        overall = round(all_scores_sum / total_questions, 1)
        answered_count = sum(c["answered"] for c in categories)

        tmmi_levels: List[Dict[str, Any]] = [{
            "number": 1, "name": "Initial", "full_name": "Stufe 1 – Initial",
            "score": None, "categories": [], "achieved": True,
        }]
        all_lower_achieved = True
        for level_name in TMMI_LEVEL_ORDER:
            lv_score = round(level_scores_sum[level_name] / level_total_map[level_name], 1)
            lv_cats = [c for c in categories if c["parent"] == level_name]
            num = LEVEL_NUMBERS[level_name]
            short_name = level_name.split(" - ")[1]
            achieved = all_lower_achieved and (lv_score >= LEVEL_THRESHOLD)
            if not achieved:
                all_lower_achieved = False
            tmmi_levels.append({
                "number": num, "name": short_name,
                "full_name": level_name.replace(" - ", " – "),
                "score": lv_score, "categories": lv_cats, "achieved": achieved,
            })

        tmmi_level_reached = max(ld["number"] for ld in tmmi_levels if ld["achieved"])
        tmmi_level_label = next(ld["full_name"] for ld in tmmi_levels if ld["number"] == tmmi_level_reached)

        return {
            "project_name": project_name,
            "project_owner": project_owner,
            "project_date": project_date,
            "generated_at": dt.datetime.now().strftime("%d.%m.%Y, %H:%M"),
            "categories": categories,
            "overall_score": overall,
            "answered_count": answered_count,
            "total_count": total_question_count(),
            "maturity_label": tmmi_level_label,
            "maturity_index": tmmi_level_reached,
            "tmmi_levels": tmmi_levels,
            "tmmi_level_reached": tmmi_level_reached,
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
        if current_user.is_admin:
            return redirect(url_for("admin_overview"))
        projects = current_user.projects
        if projects:
            return redirect(url_for("questionnaire", pid=projects[0].id))
        return redirect(url_for("new_project"))

    @app.route("/admin")
    @login_required
    def admin_overview():
        if not current_user.is_admin:
            abort(403)
        users = db.session.execute(
            db.select(User).where(User.is_admin == False).order_by(User.id)  # noqa: E712
        ).scalars().all()
        return render_template("admin.html", users=users, total_questions=total_question_count())

    @app.route("/admin/user/new", methods=["POST"])
    @login_required
    def admin_user_new():
        if not current_user.is_admin:
            abort(403)
        username = request.form.get("username", "").strip()
        display_name = request.form.get("display_name", "").strip()
        password = request.form.get("password", "").strip()
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
                db.select(User).where(User.is_admin == False)  # noqa: E712
            ).scalars().all()
            return render_template("admin.html", users=users,
                                   total_questions=total_question_count(), error=error)
        u = User(username=username, display_name=display_name or None)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        return redirect(url_for("admin_overview"))

    @app.route("/admin/user/<int:uid>/delete", methods=["POST"])
    @login_required
    def admin_user_delete(uid: int):
        if not current_user.is_admin:
            abort(403)
        user = db.session.get(User, uid)
        if not user or user.is_admin:
            abort(403)
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("admin_overview"))

    @app.route("/admin/user/<int:uid>/toggle-lock", methods=["POST"])
    @login_required
    def admin_user_toggle_lock(uid: int):
        if not current_user.is_admin:
            abort(403)
        user = db.session.get(User, uid)
        if not user or user.is_admin:
            abort(403)
        user.is_locked = not user.is_locked
        db.session.commit()
        return redirect(url_for("admin_overview"))

    @app.route("/project/new", methods=["GET", "POST"])
    @login_required
    def new_project():
        if current_user.is_admin:
            return redirect(url_for("admin_overview"))
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
            categories=CATEGORIES,
            answer_options=ANSWER_OPTIONS,
            total_questions=total_question_count(),
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
        if current_user.is_admin:
            return redirect(url_for("admin_overview"))
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

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
