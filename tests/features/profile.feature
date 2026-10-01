# language: de
Funktionalität: Profil & Benachrichtigungen
  Als Benutzer möchte ich mein Profil und anstehende Postkorb-Benachrichtigungen
  von jeder Seite aus erreichen können.

  Szenario: Profil-Button ist auf mehreren Seiten sichtbar
    Angenommen ich bin als normaler Benutzer eingeloggt
    Dann sehe ich den Profil-Button auf dem Dashboard
    Und sehe ich den Profil-Button auf der Vorlagen-Seite

  Szenario: Dropdown zeigt Administration für Superuser
    Angenommen ich bin als Admin eingeloggt und auf dem Dashboard
    Wenn ich den Profil-Button öffne
    Dann sehe ich den Menüpunkt "Administration"

  Szenario: Postkorb-Glocke ist für Admins sichtbar
    Angenommen ich bin als Admin eingeloggt und auf dem Dashboard
    Dann sehe ich die Postkorb-Glocke

  Szenario: Glocke zeigt einen Badge bei neuer Nachricht
    Angenommen ich bin als Admin eingeloggt und auf dem Dashboard
    Wenn im Postkorb eine neue Nachricht eintrifft
    Und ich die Seite neu lade
    Dann zeigt die Glocke ein Badge größer als 0

  Szenario: Administration ist für einfache Admins nicht sichtbar
    Angenommen ich bin als Admin eingeloggt
    Und ich habe einen Benutzer mit der Rolle "admin" angelegt
    Wenn ich mich abmelde und mit diesem Konto neu anmelde
    Und ich den Profil-Button öffne
    Dann sehe ich den Menüpunkt "Administration" nicht

  Szenario: Glocke ist für normale Benutzer nicht sichtbar
    Angenommen ich bin als normaler Benutzer eingeloggt
    Dann sehe ich die Postkorb-Glocke nicht

  # ── Weitere mögliche Szenarien ──
  # - Badge-Zähler sinkt wieder auf 0, sobald alle Nachrichten im Postkorb
  #   als erledigt markiert sind (nächster Poll zeigt 0 statt Badge zu
  #   verstecken)
  # - Dropdown schließt sich bei Klick außerhalb / bei Escape-Taste
  # - "Mein Konto" im Dropdown führt tatsächlich zu /account
  # - Avatar/Initiale im Profil-Button stimmt mit dem angezeigten Namen überein
  # - Polling-Intervall (60s) wird in einem eigenen, längeren Testlauf verifiziert
  #   (aktuell wird nur das Verhalten nach einem Reload geprüft, nicht der Live-Poll)
