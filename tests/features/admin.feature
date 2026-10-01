# language: de
Funktionalität: Administration
  Als Superuser möchte ich Benutzerkonten verwalten können, damit ich Zugänge
  vergeben, sperren und nachvollziehen kann, wer welches Projekt bearbeitet.

  Szenario: Admin-Seite zeigt alle UI-Elemente
    Angenommen ich bin als Admin eingeloggt
    Dann sehe ich das Formular zum Anlegen eines neuen Benutzers
    Und sehe ich mindestens eine Benutzerkarte in der Liste

  Szenario: Admin legt einen neuen Benutzer an
    Angenommen ich bin als Admin eingeloggt
    Wenn ich einen neuen Benutzer mit Benutzername und Passwort anlege
    Dann erscheint der neue Benutzer in der Benutzerliste

  Szenario: Admin sperrt einen Benutzer
    Angenommen ich bin als Admin eingeloggt
    Und ich habe einen neuen Benutzer angelegt
    Wenn ich diesen Benutzer sperre
    Dann zeigt die Benutzerkarte das Badge "gesperrt"

  Szenario: Admin kann ein eigenes Projekt anlegen
    Angenommen ich bin als Admin eingeloggt
    Wenn ich über "Neues Projekt" ein Projekt mit Namen anlege
    Dann werde ich auf die neue Projektseite weitergeleitet
    Und der Projektname ist auf der Seite sichtbar

  Szenario: Normaler Benutzer kann die Admin-Seite nicht aufrufen
    Angenommen ich bin als normaler Benutzer eingeloggt
    Wenn ich direkt die Admin-Seite aufrufe
    Dann bekomme ich den Status 403 Verboten

  Szenario: Nicht eingeloggter Benutzer wird zur Login-Seite umgeleitet
    Angenommen ich bin nicht eingeloggt
    Wenn ich direkt die Admin-Seite aufrufe
    Dann werde ich zur Login-Seite umgeleitet

  # ── Weitere mögliche Szenarien ──
  # - Admin entsperrt einen gesperrten Benutzer wieder (Gegenstück zu P3)
  # - Admin setzt die Rolle eines Benutzers (user → admin → superuser) und die
  #   neuen Rechte greifen sofort beim nächsten Request
  # - Admin löscht einen Benutzer inkl. dessen Projekten
  # - Superuser kann einen anderen Superuser nicht versehentlich herabstufen,
  #   wenn er der letzte verbleibende Superuser ist (falls diese Regel existiert)
  # - Validierung: Benutzername mit Leerzeichen/Sonderzeichen wird abgelehnt
