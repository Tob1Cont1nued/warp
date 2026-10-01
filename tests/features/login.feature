# language: de
Funktionalität: Login
  Als Benutzer möchte ich mich mit Benutzername und Passwort anmelden können,
  damit ich auf mein WARP-Konto zugreifen kann.

  Szenario: Login-Seite zeigt alle UI-Elemente
    Angenommen ich bin nicht eingeloggt
    Wenn ich die Login-Seite öffne
    Dann sehe ich das WARP-Logo mit Tagline
    Und sehe ich die Felder für Benutzername und Passwort
    Und sehe ich den Anmelden-Button
    Und sehe ich den Link "Noch kein Konto? Registrieren"

  Szenario: Admin-Login führt zum Dashboard
    Angenommen ich bin nicht eingeloggt
    Wenn ich mich mit einem Admin-Konto anmelde
    Dann werde ich auf das Dashboard weitergeleitet

  Szenario: Benutzer-Login führt zum Dashboard
    Angenommen ich bin nicht eingeloggt
    Wenn ich mich mit einem normalen Benutzerkonto anmelde
    Dann werde ich auf das Dashboard weitergeleitet

  Szenario: Falsches Passwort zeigt Fehlermeldung
    Angenommen ich bin nicht eingeloggt
    Wenn ich mich mit einem gültigen Benutzernamen aber falschem Passwort anmelde
    Dann sehe ich eine Fehlermeldung
    Und ich bleibe auf der Login-Seite

  Szenario: Unbekannter Benutzername zeigt Fehlermeldung
    Angenommen ich bin nicht eingeloggt
    Wenn ich mich mit einem nicht existierenden Benutzernamen anmelde
    Dann sehe ich eine Fehlermeldung

  Szenario: Gesperrter Benutzer bekommt spezifische Meldung
    Angenommen ein Admin hat ein Benutzerkonto angelegt und gesperrt
    Wenn ich mich mit dem gesperrten Konto anmelde
    Dann enthält die Fehlermeldung den Text "gesperrt"
    Und ich bleibe auf der Login-Seite
