"""
WARP – Benutzerverwaltung

Verwendung:
    python manage_users.py list
    python manage_users.py add <username> <passwort> [Anzeigename]
    python manage_users.py password <username> <neues_passwort>
    python manage_users.py delete <username>
    python manage_users.py make-admin <username>
    python manage_users.py remove-admin <username>
"""
import sys
from app import app
from app.models import db, User


def cmd_list() -> None:
    with app.app_context():
        users = db.session.execute(db.select(User).order_by(User.id)).scalars().all()
        if not users:
            print("Keine Benutzer vorhanden.")
            return
        print(f"{'ID':<5} {'Benutzername':<20} {'Admin':<7} Anzeigename")
        print("-" * 55)
        for u in users:
            admin_flag = "✓" if u.is_admin else ""
            print(f"{u.id:<5} {u.username:<20} {admin_flag:<7} {u.display_name or '—'}")


def cmd_add(username: str, password: str, display_name: str | None) -> None:
    with app.app_context():
        existing = db.session.execute(
            db.select(User).where(User.username == username)
        ).scalar_one_or_none()
        if existing:
            print(f"[FEHLER] Benutzer '{username}' existiert bereits.")
            return
        u = User(username=username, display_name=display_name or None)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        print(f"Benutzer '{username}' erstellt.")


def cmd_password(username: str, new_password: str) -> None:
    with app.app_context():
        u = db.session.execute(
            db.select(User).where(User.username == username)
        ).scalar_one_or_none()
        if not u:
            print(f"[FEHLER] Benutzer '{username}' nicht gefunden.")
            return
        u.set_password(new_password)
        db.session.commit()
        print(f"Passwort für '{username}' geändert.")


def cmd_delete(username: str) -> None:
    with app.app_context():
        u = db.session.execute(
            db.select(User).where(User.username == username)
        ).scalar_one_or_none()
        if not u:
            print(f"[FEHLER] Benutzer '{username}' nicht gefunden.")
            return
        db.session.delete(u)
        db.session.commit()
        print(f"Benutzer '{username}' gelöscht.")


def cmd_set_admin(username: str, is_admin: bool) -> None:
    with app.app_context():
        u = db.session.execute(
            db.select(User).where(User.username == username)
        ).scalar_one_or_none()
        if not u:
            print(f"[FEHLER] Benutzer '{username}' nicht gefunden.")
            return
        u.is_admin = is_admin
        db.session.commit()
        status = "zum Admin ernannt" if is_admin else "Admin-Rechte entfernt"
        print(f"Benutzer '{username}' wurde {status}.")


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
    elif args[0] == "list":
        cmd_list()
    elif args[0] == "add" and len(args) >= 3:
        cmd_add(args[1], args[2], " ".join(args[3:]) if len(args) > 3 else None)
    elif args[0] == "password" and len(args) == 3:
        cmd_password(args[1], args[2])
    elif args[0] == "delete" and len(args) == 2:
        cmd_delete(args[1])
    elif args[0] == "make-admin" and len(args) == 2:
        cmd_set_admin(args[1], True)
    elif args[0] == "remove-admin" and len(args) == 2:
        cmd_set_admin(args[1], False)
    else:
        print(__doc__)
