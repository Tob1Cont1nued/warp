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
    # role: 'user' | 'admin' | 'superuser'
    role = db.Column(db.String(20), default='user', nullable=False)
    is_locked = db.Column(db.Boolean, default=False, nullable=False)

    @property
    def is_admin(self) -> bool:
        """True für admin und superuser — darf Postkorb sehen/bearbeiten."""
        return self.role in ('admin', 'superuser')

    @property
    def is_superuser(self) -> bool:
        """True nur für superuser — darf alles (Nutzer, Fragenkatalog)."""
        return self.role == 'superuser'

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
        return {a.question_id: a.answer_id for a in self.answers if a.answer_id}

    def notes_dict(self) -> dict:
        return {a.question_id: a.note for a in self.answers if a.note}

    def to_form_dict(self) -> dict:
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


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.String(60), primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    parent = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=True)
    sort_order = db.Column(db.Integer, nullable=False, default=0)

    questions = db.relationship(
        "Question", back_populates="category",
        order_by="Question.sort_order",
        cascade="all, delete-orphan",
    )


class Question(db.Model):
    __tablename__ = "question"
    id = db.Column(db.String(60), primary_key=True)
    category_id = db.Column(db.String(60), db.ForeignKey("category.id"), nullable=False)
    text = db.Column(db.Text, nullable=False)
    hint = db.Column(db.Text, nullable=True)
    is_new = db.Column(db.Boolean, default=False, nullable=False)
    sort_order = db.Column(db.Integer, nullable=False, default=0)

    category = db.relationship("Category", back_populates="questions")


class InboxMessage(db.Model):
    __tablename__ = "inbox_message"
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(40), default="IMPULSE", nullable=False)
    user_name = db.Column(db.String(200), nullable=False)
    user_email = db.Column(db.String(200), nullable=False)
    recommendation = db.Column(db.String(200), nullable=False)
    scores_json = db.Column(db.Text, nullable=True)
    rationale = db.Column(db.Text, nullable=True)
    top_factors_json = db.Column(db.Text, nullable=True)
    maturity = db.Column(db.String(20), nullable=True)   # 'gut' | 'ausbaufaehig' | 'minimal'
    contact_pref = db.Column(db.String(20), nullable=True)  # 'email' | 'telefon' | 'beide'
    contact_phone = db.Column(db.String(60), nullable=True)
    received_at = db.Column(db.DateTime, default=dt.datetime.utcnow, nullable=False)
    status = db.Column(db.String(20), default="neu", nullable=False)
    claimed_by_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    claimed_at = db.Column(db.DateTime, nullable=True)

    claimed_by = db.relationship("User", foreign_keys=[claimed_by_id])
