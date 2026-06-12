import datetime as dt

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    display_name = db.Column(db.String(120), nullable=True)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_locked = db.Column(db.Boolean, default=False, nullable=False)

    projects = db.relationship(
        "Project", back_populates="user",
        order_by="Project.created_at.desc()",
        cascade="all, delete-orphan",
    )

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(200), nullable=False, default="Neues Projekt")
    owner = db.Column(db.String(120), nullable=True)
    date = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

    user = db.relationship("User", back_populates="projects")
    answers = db.relationship(
        "Answer", back_populates="project",
        cascade="all, delete-orphan",
    )

    def answers_dict(self) -> dict:
        """Returns {question_id: answer_id} for all saved answers."""
        return {a.question_id: a.answer_id for a in self.answers if a.answer_id}

    def notes_dict(self) -> dict:
        """Returns {question_id: note} for all saved notes."""
        return {a.question_id: a.note for a in self.answers if a.note}

    def to_form_dict(self) -> dict:
        """Converts project + answers into a form-compatible dict for report generation."""
        form = {
            "project_name": self.name,
            "project_owner": self.owner or "",
            "project_date": self.date or "",
        }
        for a in self.answers:
            if a.answer_id:
                form[f"answer-{a.question_id}"] = a.answer_id
            if a.note:
                form[f"note-{a.question_id}"] = a.note
        return form


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    question_id = db.Column(db.String(80), nullable=False)
    answer_id = db.Column(db.String(20), nullable=True)
    note = db.Column(db.Text, nullable=True)

    project = db.relationship("Project", back_populates="answers")

    __table_args__ = (
        db.UniqueConstraint("project_id", "question_id", name="uq_project_question"),
    )
