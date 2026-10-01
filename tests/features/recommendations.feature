# language: de
Funktionalität: Handlungsempfehlungen
  Als Benutzer möchte ich auf dem Auswertung-Tab konkrete Handlungsempfehlungen
  zu schwach beantworteten Fragen sehen, damit ich weiß, wo ich ansetzen muss.

  Hintergrund:
    Angenommen ich bin als normaler Benutzer eingeloggt und auf dem Dashboard
    Und ich lege über "+" ein neues Projekt an

  Szenario: Empfehlungskarte erscheint bei niedrigen Antworten
    Wenn ich Fragen mit niedriger Bewertung in mehreren Kategorien beantworte
    Und ich den Auswertung-Tab öffne
    Dann sehe ich die Handlungsempfehlungen-Karte

  Szenario: Empfehlungskarte bleibt ohne niedrige Antworten versteckt
    Wenn ich keine Fragen beantworte
    Und ich den Auswertung-Tab öffne
    Dann sehe ich die Handlungsempfehlungen-Karte nicht

  Szenario: Empfehlungen werden nach Kategorie gruppiert
    Wenn ich Fragen mit niedriger Bewertung in mehreren Kategorien beantworte
    Und ich den Auswertung-Tab öffne
    Dann sehe ich mindestens eine Kategorie-Überschrift

  Szenario: Kategorie-Überschrift zeigt die Anzahl der Empfehlungen
    Wenn ich eine Frage mit "Trifft nicht zu" beantworte
    Und ich den Auswertung-Tab öffne
    Dann enthält die erste Kategorie-Überschrift das Wort "Empfehlung"

  Szenario: Kategorie lässt sich ein- und wieder ausklappen
    Wenn ich Fragen mit niedriger Bewertung in mehreren Kategorien beantworte
    Und ich den Auswertung-Tab öffne
    Dann ist der Inhalt der ersten Kategorie sichtbar
    Wenn ich auf die erste Kategorie-Überschrift klicke
    Dann ist der Inhalt der ersten Kategorie nicht mehr sichtbar
    Wenn ich erneut auf die erste Kategorie-Überschrift klicke
    Dann ist der Inhalt der ersten Kategorie wieder sichtbar

  Szenario: Gesamte Empfehlungsliste lässt sich ein- und wieder ausklappen
    Wenn ich Fragen mit niedriger Bewertung in mehreren Kategorien beantworte
    Und ich den Auswertung-Tab öffne
    Dann ist die Empfehlungsliste sichtbar
    Wenn ich auf den Gesamt-Toggle-Button klicke
    Dann ist die Empfehlungsliste nicht mehr sichtbar
    Wenn ich erneut auf den Gesamt-Toggle-Button klicke
    Dann ist die Empfehlungsliste wieder sichtbar

  # ── Weitere mögliche Szenarien ──
  # - Empfehlungstext selbst stichprobenartig gegen die hinterlegten
  #   Kategorie-Empfehlungen aus app/data/questions.py prüfen (Inhalt, nicht
  #   nur Sichtbarkeit)
  # - Sehr viele niedrige Antworten (alle 137 Fragen "Trifft nicht zu") →
  #   Performance/Rendering-Zeit der Empfehlungsliste bleibt im Rahmen
  # - Empfehlungen aktualisieren sich live, wenn eine Antwort auf dem
  #   Fragenkatalog-Tab geändert wird, ohne den Auswertung-Tab neu zu laden
  # - Sortierung der Kategorien (z. B. nach Schweregrad oder WARP-Stufe)
