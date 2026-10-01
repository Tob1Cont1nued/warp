# language: de
Funktionalität: Registrierung
  Als neue Nutzerin oder neuer Nutzer möchte ich ein WARP-Konto anlegen können,
  damit ich eigene Assessments durchführen kann.

  Szenario: Registrierungs-Seite zeigt alle UI-Elemente
    Angenommen ich bin nicht eingeloggt
    Wenn ich die Registrierungs-Seite öffne
    Dann sehe ich das WARP-Logo auf der Registrierungs-Seite
    Und sehe ich die Felder Benutzername, Anzeigename, Passwort und Passwort-Bestätigung
    Und sehe ich den Registrieren-Button
    Und sehe ich den Link "Bereits registriert? Anmelden"

  Szenario: Neuer Benutzer landet nach Registrierung auf dem Dashboard
    Angenommen ich bin nicht eingeloggt
    Wenn ich mich mit einem neuen, eindeutigen Benutzernamen registriere
    Dann werde ich auf das Dashboard weitergeleitet

  Szenario: Link "Bereits registriert" führt zur Login-Seite
    Angenommen ich bin nicht eingeloggt
    Wenn ich die Registrierungs-Seite öffne
    Und ich auf "Bereits registriert? Anmelden" klicke
    Dann lande ich auf der Login-Seite

  Szenario: Bereits vergebener Benutzername zeigt Fehlermeldung
    Angenommen ich bin nicht eingeloggt
    Wenn ich mich mit einem bereits vergebenen Benutzernamen registriere
    Dann enthält die Fehlermeldung den Text "vergeben"

  Szenario: Nicht übereinstimmende Passwörter zeigen Fehlermeldung
    Angenommen ich bin nicht eingeloggt
    Wenn ich mich mit zwei unterschiedlichen Passwörtern registriere
    Dann enthält die Fehlermeldung den Text "überein"

  Szenario: Zu kurzes Passwort zeigt Fehlermeldung
    Angenommen ich bin nicht eingeloggt
    Wenn ich mich mit einem zu kurzen Passwort registriere
    Dann enthält die Fehlermeldung den Text "6 Zeichen"

  # ── Weitere mögliche Szenarien (siehe "Erweiterungsvorschläge" im PR/Chat) ──
  # - Registrierung ohne E-Mail-Adresse → Fehlermeldung (bereits als TC-AUTH-12
  #   im Unit-Test abgedeckt, hier als Frontend-Gegenstück ergänzbar)
  # - Doppelte Registrierung mit derselben E-Mail, aber anderem Benutzernamen
  # - Passwort-Stärke-Hinweis während der Eingabe (falls UI das anzeigt)
  # - Doppel-Klick auf "Registrieren" legt nicht zwei Konten an
