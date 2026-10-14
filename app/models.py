import datetime as dt

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    display_name = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(200), unique=True, nullable=True)
    password_hash = db.Column(db.String(200), nullable=False)
    # role: 'user' | 'admin' | 'superuser'
    role = db.Column(db.String(20), default='user', nullable=False)
    is_locked = db.Column(db.Boolean, default=False, nullable=False)
    reset_token = db.Column(db.String(100), unique=True, nullable=True)
    reset_token_expires = db.Column(db.DateTime, nullable=True)

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
    is_complete = db.Column(db.Boolean, default=False, nullable=False)
    catalog_type = db.Column(db.String(20), nullable=False, default='assessment')

    user = db.relationship("User", back_populates="projects")
    answers = db.relationship(
        "Answer", back_populates="project",
        cascade="all, delete-orphan",
    )
    workshop_questions = db.relationship(
        "WorkshopQuestion", back_populates="project",
        cascade="all, delete-orphan",
        order_by="WorkshopQuestion.sort_order",
    )
    process_model = db.relationship(
        "ProcessModel", uselist=False, cascade="all, delete-orphan",
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
    catalog_type = db.Column(db.String(20), nullable=False, default='assessment')

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
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=True)

    claimed_by = db.relationship("User", foreign_keys=[claimed_by_id])
    project = db.relationship("Project", foreign_keys=[project_id])


class WorkshopQuestion(db.Model):
    __tablename__ = "workshop_question"
    id = db.Column(db.String(80), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    text = db.Column(db.Text, nullable=False)
    hint = db.Column(db.Text, nullable=True)
    sort_order = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

    project = db.relationship("Project", back_populates="workshop_questions")


class GeneratedDocument(db.Model):
    __tablename__ = "generated_document"
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    doc_type = db.Column(db.String(60), nullable=False)
    generated_at = db.Column(db.DateTime, default=dt.datetime.utcnow, nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    file_data = db.Column(db.LargeBinary, nullable=False)

    __table_args__ = (
        db.UniqueConstraint("project_id", "doc_type", name="uq_project_doctype"),
    )


class ProcessModel(db.Model):
    __tablename__ = "process_model"
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False, default="Deployment-Prozess")
    version = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow, nullable=False)

    phases = db.relationship(
        "ProcessPhase", back_populates="model",
        cascade="all, delete-orphan", order_by="ProcessPhase.sort_order",
    )
    roles = db.relationship(
        "ProcessRole", back_populates="model",
        cascade="all, delete-orphan", order_by="ProcessRole.name",
    )
    interfaces = db.relationship(
        "ProcessInterface", back_populates="model",
        cascade="all, delete-orphan", order_by="ProcessInterface.name",
    )
    dependencies = db.relationship(
        "ProcessDependency", back_populates="model",
        cascade="all, delete-orphan",
    )
    environments = db.relationship(
        "ProcessEnvironment", back_populates="model",
        cascade="all, delete-orphan", order_by="ProcessEnvironment.sort_order",
    )
    steps = db.relationship(
        "ProcessStep", back_populates="model",
        cascade="all, delete-orphan",
    )
    areas = db.relationship(
        "ProcessArea", back_populates="model",
        cascade="all, delete-orphan",
    )


class ProcessPhase(db.Model):
    __tablename__ = "process_phase"
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey("process_model.id"), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    sort_order = db.Column(db.Integer, nullable=False, default=0)

    model = db.relationship("ProcessModel", back_populates="phases")
    # Kein delete-orphan hier: Steps gehören primär zu ProcessModel (siehe dort), die
    # Phase ist nur eine optionale Zuordnung. Ein Step darf die Phase wechseln oder
    # verlieren, ohne gelöscht zu werden.
    steps = db.relationship(
        "ProcessStep", back_populates="phase", order_by="ProcessStep.sort_order",
    )


class ProcessRole(db.Model):
    __tablename__ = "process_role"
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey("process_model.id"), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    deputy_role_id = db.Column(db.Integer, db.ForeignKey("process_role.id"), nullable=True)

    model = db.relationship("ProcessModel", back_populates="roles")
    deputy_role = db.relationship("ProcessRole", remote_side=[id])


class ProcessStep(db.Model):
    """Ein Knoten auf der Prozesskarte. Gehört immer zu einem ProcessModel (für Kaskaden-Löschung),
    die Phase ist optional – frei hinzugefügte Punkte können zunächst ohne Phase bestehen."""
    __tablename__ = "process_step"
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey("process_model.id"), nullable=False)
    phase_id = db.Column(db.Integer, db.ForeignKey("process_phase.id"), nullable=True)
    responsible_role_id = db.Column(db.Integer, db.ForeignKey("process_role.id"), nullable=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_test_step = db.Column(db.Boolean, default=False, nullable=False)
    sort_order = db.Column(db.Integer, nullable=False, default=0)
    x = db.Column(db.Float, nullable=True)
    y = db.Column(db.Float, nullable=True)
    # Akzentfarbe des Punkts auf der Prozesskarte (Hex), None = Standardfarbe.
    color = db.Column(db.String(20), nullable=True)

    model = db.relationship("ProcessModel", back_populates="steps")
    phase = db.relationship("ProcessPhase", back_populates="steps")
    responsible_role = db.relationship("ProcessRole")


class ProcessDependency(db.Model):
    """Abhängigkeit eines Schritts: entweder von einem anderen Schritt oder von einem
    benannten System/Umgebung/Datenquelle (dann depends_on_label statt depends_on_step_id)."""
    __tablename__ = "process_dependency"
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey("process_model.id"), nullable=False)
    step_id = db.Column(db.Integer, db.ForeignKey("process_step.id"), nullable=False)
    depends_on_step_id = db.Column(db.Integer, db.ForeignKey("process_step.id"), nullable=True)
    depends_on_label = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)
    # Typ der Kante auf der Prozesskarte, steuert die Farbe. Frei wählbar, siehe
    # EDGE_KINDS in app/__init__.py für die vordefinierte Palette.
    kind = db.Column(db.String(30), nullable=False, default="default")

    model = db.relationship("ProcessModel", back_populates="dependencies")
    step = db.relationship("ProcessStep", foreign_keys=[step_id])
    depends_on_step = db.relationship("ProcessStep", foreign_keys=[depends_on_step_id])


class ProcessInterface(db.Model):
    __tablename__ = "process_interface"
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey("process_model.id"), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    source_system = db.Column(db.String(200), nullable=True)
    target_system = db.Column(db.String(200), nullable=True)
    owner_role_id = db.Column(db.Integer, db.ForeignKey("process_role.id"), nullable=True)
    description = db.Column(db.Text, nullable=True)

    model = db.relationship("ProcessModel", back_populates="interfaces")
    owner_role = db.relationship("ProcessRole")


class ProcessEnvironment(db.Model):
    """Umgebung wie Entwicklung, Test oder Integration. stage ist frei wählbar, z.B. 'entwicklung', 'test', 'integration', 'prod'."""
    __tablename__ = "process_environment"
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey("process_model.id"), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    stage = db.Column(db.String(40), nullable=False)
    description = db.Column(db.Text, nullable=True)
    sort_order = db.Column(db.Integer, nullable=False, default=0)

    model = db.relationship("ProcessModel", back_populates="environments")
    versions = db.relationship(
        "ProcessEnvironmentVersion", back_populates="environment",
        cascade="all, delete-orphan", order_by="ProcessEnvironmentVersion.deployed_at.desc()",
    )


class ProcessEnvironmentVersion(db.Model):
    """Versionsstand, der zu einem Zeitpunkt auf einer Umgebung bereitliegt."""
    __tablename__ = "process_environment_version"
    id = db.Column(db.Integer, primary_key=True)
    environment_id = db.Column(db.Integer, db.ForeignKey("process_environment.id"), nullable=False)
    version = db.Column(db.String(100), nullable=False)
    deployed_at = db.Column(db.DateTime, nullable=True)
    deployed_by_role_id = db.Column(db.Integer, db.ForeignKey("process_role.id"), nullable=True)
    note = db.Column(db.Text, nullable=True)

    environment = db.relationship("ProcessEnvironment", back_populates="versions")
    deployed_by_role = db.relationship("ProcessRole")


class ProcessArea(db.Model):
    """Frei platzierbares, beschriftetes Rechteck auf der Prozesskarte zum optischen
    Gruppieren von Punkten (z.B. eine Phase oder ein Team-Bereich). layer bestimmt,
    ob es hinter ('back') oder vor ('front') den Punkten liegt."""
    __tablename__ = "process_area"
    id = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey("process_model.id"), nullable=False)
    label = db.Column(db.String(200), nullable=False, default="Bereich")
    x = db.Column(db.Float, nullable=False, default=0)
    y = db.Column(db.Float, nullable=False, default=0)
    width = db.Column(db.Float, nullable=False, default=220)
    height = db.Column(db.Float, nullable=False, default=140)
    color = db.Column(db.String(20), nullable=True)
    opacity = db.Column(db.Float, nullable=False, default=0.16)
    layer = db.Column(db.String(10), nullable=False, default="back")

    model = db.relationship("ProcessModel", back_populates="areas")
