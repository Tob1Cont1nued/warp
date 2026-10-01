# language: de
Funktionalität: Fragenkatalog
  Als Benutzer möchte ich den WARP-Fragenkatalog zu meinem Projekt beantworten
  können, damit mein Reifegrad ermittelt wird.

  Szenario: Fragenkatalog-Seite zeigt alle UI-Elemente
    Angenommen ich bin als Benutzer mit einem eigenen Projekt eingeloggt
    Dann sehe ich die Projekt-Sidebar mit "Neues Projekt"-Button
    Und sehe ich im Profil-Dropdown den Abmelden-Link
    Und sehe ich mindestens eine Antwort-Auswahl und ein Notizfeld
    Und sehe ich den Fortschrittsbalken und den Auswertung-Tab

  Szenario: Antwort bleibt nach Neuladen der Seite erhalten
    Angenommen ich bin als Benutzer mit einem eigenen Projekt eingeloggt
    Wenn ich die erste Frage beantworte
    Und ich die Seite neu lade
    Dann ist dieselbe Antwort weiterhin ausgewählt

  Szenario: Vorlagen-Downloads sind vorhanden und verlinkt
    Angenommen ich bin als Benutzer mit einem eigenen Projekt eingeloggt
    Wenn ich die Vorlagen-Seite öffne
    Dann sehe ich genau 3 Download-Buttons, die auf .docx-Dateien verlinken

  Szenario: Nicht eingeloggter Benutzer wird zur Login-Seite umgeleitet
    Angenommen ich bin nicht eingeloggt
    Wenn ich direkt ein Projekt über seine URL aufrufe
    Dann werde ich zur Login-Seite umgeleitet

  Szenario: Benutzer kann nicht auf ein fremdes Projekt zugreifen
    Angenommen ich bin als Benutzer mit einem eigenen Projekt eingeloggt
    Wenn sich ein anderer Benutzer anmeldet und mein Projekt über die URL aufruft
    Dann bekommt dieser Benutzer den Status 403 Verboten

  Szenario: Nicht existierende Projekt-ID liefert 404
    Angenommen ich bin als Benutzer mit einem eigenen Projekt eingeloggt
    Wenn ich ein Projekt mit einer nicht existierenden ID aufrufe
    Dann bekomme ich den Status 404 Nicht gefunden

  # ── Weitere mögliche Szenarien ──
  # - Mehrere Fragen aus unterschiedlichen Kategorien gleichzeitig beantworten
  #   und prüfen, dass der Fortschrittsbalken korrekt mitzählt
  # - Notiz zu einer Frage speichern und nach Reload prüfen (analog zur Antwort)
  # - Autosave bei Netzwerkfehler/Timeout: Frontend zeigt einen Hinweis statt
  #   die Änderung stillschweigend zu verlieren
  # - Zwei Browser-Tabs mit demselben Projekt offen: Antwort in Tab 1 ändern,
  #   in Tab 2 reloaden und prüfen, dass kein Datenverlust auftritt
  # - Sehr langer Notiz-Text (Grenzwert der Textarea/des Feldes in der DB)
