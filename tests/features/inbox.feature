# language: de
Funktionalität: Postkorb
  Als Admin möchte ich eingehende IMPULSE-Nachrichten im Postkorb sehen und
  bearbeiten können, damit nichts verloren geht.

  Szenario: Admin sieht den Postkorb-Link in der Sidebar
    Angenommen ich bin als Admin eingeloggt und auf dem Dashboard
    Dann sehe ich den Postkorb-Link in der Sidebar

  Szenario: Admin öffnet den Postkorb über die Sidebar
    Angenommen ich bin als Admin eingeloggt und auf dem Dashboard
    Wenn ich auf den Postkorb-Link in der Sidebar klicke
    Dann lande ich auf der Postkorb-Seite
    Und die Überschrift enthält "Postkorb"
    Und jeder vorhandene Antworten-Button hat eine gültige E-Mail-Adresse hinterlegt

  Szenario: Normaler Benutzer sieht keinen Postkorb-Link
    Angenommen ich bin als normaler Benutzer eingeloggt
    Dann sehe ich den Postkorb-Link in der Sidebar nicht

  Szenario: Normaler Benutzer kann den Postkorb nicht direkt aufrufen
    Angenommen ich bin als normaler Benutzer eingeloggt
    Wenn ich direkt die Postkorb-Seite aufrufe
    Dann werde ich blockiert

  Szenario: Nicht eingeloggter Benutzer wird zur Login-Seite umgeleitet
    Angenommen ich bin nicht eingeloggt
    Wenn ich direkt die Postkorb-Seite aufrufe
    Dann werde ich zur Login-Seite umgeleitet

  # ── Weitere mögliche Szenarien ──
  # - Admin "beansprucht" (claim) eine Nachricht → Button zeigt "freigeben"
  #   statt "übernehmen", andere Admins sehen den Bearbeiter-Namen
  # - Zwei Admins versuchen gleichzeitig dieselbe Nachricht zu claimen
  #   (Race Condition) → nur einer gewinnt, der andere sieht eine Meldung
  # - Admin markiert eine Nachricht als erledigt → verschwindet aus "Neu",
  #   taucht unter "Erledigt" wieder auf
  # - Admin legt aus einer Postkorb-Nachricht direkt ein Projekt an
  #   (create-project-Button) und die Nachricht verknüpft sich mit dem Projekt
  # - Filtern/Suchen im Postkorb nach Status oder Absender (falls vorhanden)
