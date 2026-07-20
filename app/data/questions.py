"""
WARP Tool - Fragenkatalog Daten

Struktur:
  - 4 WARP-Stufen: Stufe 2 - Managed, Stufe 3 - Defined,
    Stufe 4 - Measured, Stufe 5 - Optimization
  - Unterkategorien (Process Areas)

Hinweis Auswertungslogik:
  Eine Stufe gilt als erreicht, wenn alle Process Areas dieser Stufe
  UND aller darunterliegenden Stufen ein definiertes Mindestreifeniveau
  erreichen. Stufe N+1 ist erst erreichbar, wenn Stufe N vollständig
  erfüllt ist.

Fragen, die im Original-Katalog nicht enthalten waren und zur
vollständigen Abdeckung der jeweiligen Process Area ergänzt wurden,
sind über das Feld "new": True markiert.

Erweitern: einfach neue Kategorien/Fragen anhängen.
"""

CATEGORIES = [
    # =========================================================================
    # STUFE 2: MANAGED (GEMANAGT)
    # =========================================================================
    {
        "id": "teststrategie",
        "title": "Teststrategie und Testkonzept",
        "parent": "Stufe 2 - Managed",
        "description": (
            "Eine dokumentierte, risikobasierte Teststrategie sorgt für ein "
            "stimmiges Verhältnis von Aufwand/Ressourcen zum vorhandenen Risiko "
            "und bildet die Grundlage für alle nachgelagerten Testaktivitäten."
        ),
        "questions": [
            {
                "id": "ts-1",
                "text": "Es existiert eine dokumentierte, projekt- oder organisationsweite Teststrategie.",
                "hint": None,
                "recommendations": {
                    "low": "Legen Sie eine schriftliche Teststrategie an, die Testziele, Teststufen, Testarten, Ressourcen und Risiken beschreibt. Bereits ein zweiseitiges Dokument schafft die notwendige Verbindlichkeit und Transparenz für alle Beteiligten.",
                    "mid": "Ergänzen Sie die vorhandene Teststrategie um fehlende Kernelemente (z.B. Risikobetrachtung, Ressourcenplanung) und stellen Sie sicher, dass sie allen Projektbeteiligten zugänglich ist.",
                },
            },
            {
                "id": "ts-2",
                "text": "Testlevel (Komponente, Integration, System, Akzeptanz) sind klar definiert und voneinander abgegrenzt.",
                "hint": None,
                "recommendations": {
                    "low": "Definieren Sie die Testebenen schriftlich: Legen Sie für jede Ebene fest, was getestet wird, wer testet, welche Werkzeuge eingesetzt werden und welche Ein-/Ausstiegskriterien gelten.",
                    "mid": "Schärfen Sie die Abgrenzung zwischen den bestehenden Testebenen und klären Sie Überschneidungen oder Zuständigkeitslücken. Dokumentieren Sie die Festlegungen verbindlich im Testkonzept.",
                },
            },
            {
                "id": "ts-3",
                "text": "Produktrisiken sind analysiert und in die Priorisierung der Testfälle einbezogen.",
                "hint": "Gibt es eine Risikoanalyse für die Software? Gibt es eine Priorisierung der Testfälle, die darauf basiert?",
                "recommendations": {
                    "low": "Führen Sie eine strukturierte Risikoanalyse durch (z.B. mit einer Risikomatrix: Eintrittswahrscheinlichkeit × Schadensausmaß) und nutzen Sie die Ergebnisse, um Testfälle nach Priorität zu ordnen.",
                    "mid": "Aktualisieren Sie die Risikoanalyse regelmäßig (z.B. bei jeder Releaseplanung) und stellen Sie sicher, dass die Priorisierung der Testfälle die jeweils aktuellen Risiken widerspiegelt.",
                },
            },
            {
                "id": "ts-4",
                "text": "Testarten (funktional, nicht-funktional wie Performance, Security, Usability) werden angemessen berücksichtigt.",
                "hint": None,
                "recommendations": {
                    "low": "Ermitteln Sie, welche nicht-funktionalen Anforderungen (Performance, Security, Usability, Reliability) für Ihre Software relevant sind, und planen Sie entsprechende Testaktivitäten explizit in die Teststrategie ein.",
                    "mid": "Überprüfen Sie, ob alle relevanten Testarten ausreichend abgedeckt sind — insbesondere ob nicht-funktionale Tests (z.B. Last- und Sicherheitstests) systematisch geplant und nicht nur ad hoc durchgeführt werden.",
                },
            },
            {
                "id": "ts-5",
                "text": "Die Teststrategie wird regelmäßig überprüft und an veränderte Rahmenbedingungen angepasst.",
                "hint": None,
                "recommendations": {
                    "low": "Etablieren Sie einen festen Review-Rhythmus für die Teststrategie (z.B. quartalsweise oder nach größeren Projektänderungen) und weisen Sie die Verantwortung für den Review explizit einer Person zu.",
                    "mid": "Formalisieren Sie den Review-Prozess: Definieren Sie konkrete Auslöser (z.B. Technologiewechsel, neue regulatorische Anforderungen) und einen Freigabeprozess für Änderungen an der Teststrategie.",
                },
            },
            {
                "id": "ts-6",
                "text": "Die Teststrategie ist mit der übergeordneten Projekt-/Unternehmensstrategie abgestimmt.",
                "hint": None,
                "recommendations": {
                    "low": "Binden Sie Projektleitung und relevante Stakeholder in die Erstellung der Teststrategie ein. Verankern Sie Qualitätsziele explizit im Projektauftrag und stellen Sie sicher, dass Testressourcen entsprechend eingeplant werden.",
                    "mid": "Holen Sie eine explizite Bestätigung der Stakeholder zur aktuellen Teststrategie ein und dokumentieren Sie die Abstimmung. Überprüfen Sie, ob die Teststrategie die strategischen Prioritäten der Projektleitung widerspiegelt.",
                },
            },
            {
                "id": "ts-7",
                "text": "Es gibt klare Entry-/Exit-Kriterien (Ein-/Ausstiegskriterien) je Teststufe.",
                "hint": None,
                "recommendations": {
                    "low": "Definieren Sie für jede Teststufe verbindliche Einstiegs- und Ausstiegskriterien mit messbaren Schwellwerten (z.B. Codeabdeckung ≥ 80 %, keine offenen Critical Bugs) und dokumentieren Sie diese im Testkonzept.",
                    "mid": "Konkretisieren Sie die vorhandenen Kriterien mit messbaren Schwellwerten und stellen Sie sicher, dass sie vor Beginn jeder Teststufe allen Beteiligten bekannt sind und verbindlich angewendet werden.",
                },
            },
            {
                "id": "ts-8",
                "text": "Besonders risikobehaftete Softwarekomponenten oder Prozesse werden zuerst getestet.",
                "hint": "Werden risikoreiche Softwarekomponenten zuerst getestet? Gibt es eine Übersicht?",
                "recommendations": {
                    "low": "Erstellen Sie eine Übersicht Ihrer Softwarekomponenten mit einer Risikobewertung (nach Kritikalität, Fehleranfälligkeit und Komplexität) und stellen Sie sicher, dass hochriskante Bereiche in der Testplanung Vorrang erhalten.",
                    "mid": "Überprüfen Sie, ob die aktuelle Testreihenfolge die Risikopriorisierung konsistent umsetzt — insbesondere ob auch unter Zeitdruck die kritischsten Komponenten zuerst getestet werden.",
                },
            },
            {
                "id": "ts-9",
                "text": "Fehlernachtests und Regressionstests werden gemäß Risikoeinschätzung durchgeführt.",
                "hint": "Gibt es eine Empfehlung, wie viel nach der Fehlerbehebung getestet wird?",
                "recommendations": {
                    "low": "Legen Sie verbindlich fest, welcher Umfang an Regressionstests nach Fehlerbehebungen auf Basis der Risikoeinschätzung durchgeführt wird. Automatisierte Regressionstests reduzieren den Aufwand langfristig erheblich.",
                    "mid": "Formalisieren Sie den Entscheidungsprozess für den Regressionsumfang: Definieren Sie, wer entscheidet, welche Tests nach einer Änderung ausgeführt werden, und evaluieren Sie Automatisierungspotenzial.",
                },
            },
            {
                "id": "ts-10",
                "text": "Es existiert ein definierter Eskalationsweg, wenn Testbedarfe nicht ausreichend berücksichtigt werden.",
                "hint": None,
                "recommendations": {
                    "low": "Definieren Sie einen klaren Eskalationsweg (z.B. Testleiter → Projektleiter → Steuerungskreis) mit konkreten Auslösern und Entscheidungsbefugnissen, und kommunizieren Sie ihn an alle Testbeteiligten.",
                    "mid": "Überprüfen Sie, ob der vorhandene Eskalationsweg bekannt und praktisch nutzbar ist. Stellen Sie sicher, dass er auch unter Zeitdruck tatsächlich genutzt wird und zu verbindlichen Entscheidungen führt.",
                },
            },
            {
                "id": "ts-11",
                "text": "Testziele und Qualitätsziele werden für jedes Projekt aus der übergeordneten Teststrategie abgeleitet.",
                "hint": None,
                "recommendations": {
                    "low": "Etablieren Sie einen strukturierten Prozess, bei dem zu Projektbeginn Testziele und messbare Qualitätsziele aus der übergeordneten Teststrategie abgeleitet und dokumentiert werden. Nutzen Sie eine einfache Vorlage, um sicherzustellen, dass dieser Schritt in jedem Projekt konsistent erfolgt.",
                    "mid": "Überprüfen Sie, ob die bereits abgeleiteten Projektziele tatsächlich mit der übergeordneten Teststrategie konsistent sind, und stellen Sie sicher, dass der Ableitungsprozess für alle Testmanager verbindlich und nachvollziehbar dokumentiert ist.",
                },
                "new": True,
            },
        ],
    },
    {
        "id": "testplanung",
        "title": "Testplanung",
        "parent": "Stufe 2 - Managed",
        "description": (
            "Passende Schätztechniken und eine enge Einbindung der Stakeholder "
            "ermöglichen eine realistische und zuverlässige Planung des "
            "Testvorgehens innerhalb von Zeit, Kosten und Ergebnis."
        ),
        "questions": [
            {
                "id": "tp-1",
                "text": "Testaufwände werden systematisch geschätzt (z.B. auf Basis von Erfahrungswerten, Metriken, Modellen).",
                "hint": None,
                "recommendations": {
                    "low": "Führen Sie eine dokumentierte Schätzmethodik ein, z.B. auf Basis von Analogieschätzungen anhand früherer Projekte oder einfacher Funktionspunkte. Selbst eine grobe strukturierte Schätzung ist besser als keine, da sie Überraschungen im Projektverlauf reduziert.",
                    "mid": "Erweitern Sie die bestehende Schätzpraxis um eine zweite Methode (z.B. Dreipunktschätzung oder Benchmarking mit Branchendaten) und dokumentieren Sie Schätzannahmen systematisch, um die Schätzgenauigkeit über Projekte hinweg zu verbessern.",
                },
            },
            {
                "id": "tp-2",
                "text": "Testaufwände fließen in die Projektplanung und Budgetierung mit ein.",
                "hint": None,
                "recommendations": {
                    "low": "Stellen Sie sicher, dass Testaufwände als eigenständige Position in der Projektplanung und Budgetierung erscheinen. Sprechen Sie frühzeitig mit der Projektleitung, um Testressourcen verbindlich einzuplanen und spätere Kürzungen zu verhindern.",
                    "mid": "Formalisieren Sie die Integration der Testaufwände in die Projektplanung durch einen definierten Prozessschritt und eine verantwortliche Person, die sicherstellt, dass Testbudgets realistisch kalkuliert und nicht nachträglich pauschal gekürzt werden.",
                },
            },
            {
                "id": "tp-3",
                "text": "Es werden Testpläne erstellt, die Umfang, Zeitplan, Ressourcen und Abhängigkeiten beschreiben.",
                "hint": "Gibt es einen zeitlichen Plan, wann welche Teststufe durchlaufen wird? Sind Ressourcen und Abwesenheiten berücksichtigt?",
                "recommendations": {
                    "low": "Erstellen Sie für jedes Projekt einen Testplan auf Basis einer Standardvorlage, der mindestens Testumfang, Zeitplan, Verantwortlichkeiten und Abhängigkeiten enthält. Ein einseitiger Testplan ist besser als gar keiner und schafft Verbindlichkeit für alle Beteiligten.",
                    "mid": "Überprüfen Sie die Vollständigkeit und Aktualität der vorhandenen Testpläne und stellen Sie sicher, dass Ressourcenplanung und kritische Abhängigkeiten (z.B. Lieferpunkte der Entwicklung) explizit beschrieben und mit allen Beteiligten abgestimmt sind.",
                },
            },
            {
                "id": "tp-4",
                "text": "Bei Planänderungen (z.B. Scope-Änderungen) wird der Testaufwand neu bewertet.",
                "hint": None,
                "recommendations": {
                    "low": "Definieren Sie einen klaren Trigger-Mechanismus: Legen Sie fest, welche Änderungen (z.B. Scope-Erweiterungen, Terminverschiebungen) eine Neubeurteilung des Testaufwands auslösen, und kommunizieren Sie diesen Prozess an Projektleitung und Stakeholder.",
                    "mid": "Formalisieren Sie den Neubewertungsprozess durch eine verantwortliche Person und eine dokumentierte Checkliste, damit bei Änderungen systematisch geprüft wird, welche Auswirkungen auf Testumfang, Ressourcen und Zeitplan entstehen.",
                },
            },
            {
                "id": "tp-5",
                "text": "Es gibt eine Nachverfolgung von geplantem vs. tatsächlichem Testaufwand.",
                "hint": None,
                "recommendations": {
                    "low": "Erfassen Sie den tatsächlichen Testaufwand konsequent (z.B. über Stundenbuchungen oder einfache Zeiterfassung) und vergleichen Sie ihn regelmäßig mit der Planung. Diese Transparenz ist die Grundlage für fundierte Schätzungen in künftigen Projekten.",
                    "mid": "Stellen Sie sicher, dass die Aufwandsnachverfolgung für alle Testaktivitäten granular genug erfolgt, um Abweichungsursachen zu identifizieren, und nutzen Sie die Erkenntnisse systematisch zur Kalibrierung zukünftiger Schätzungen.",
                },
            },
            {
                "id": "tp-6",
                "text": "Pufferzeiten für Nacharbeiten (Retest, Regressionstest) werden eingeplant.",
                "hint": None,
                "recommendations": {
                    "low": "Planen Sie explizit Pufferzeiten für Fehlernachtests und Regressionstests ein – erfahrungsgemäß sind 15–25 % des Testaufwands ein realistischer Ansatz. Machen Sie diese Puffer im Testplan sichtbar und kommunizieren Sie sie an die Projektleitung.",
                    "mid": "Überprüfen Sie, ob die eingeplanten Puffer auf Basis von Projekterfahrungswerten kalibriert sind und tatsächlich für Nacharbeiten reserviert bleiben – und nicht im Projektverlauf für andere Zwecke genutzt werden.",
                },
            },
            {
                "id": "tp-7",
                "text": "Stakeholder (Fachbereich, Product Owner, Entwicklung, Management) werden aktiv in die Testplanung eingebunden.",
                "hint": None,
                "recommendations": {
                    "low": "Laden Sie relevante Stakeholder (Fachbereich, Product Owner, Entwicklungsleitung) zu einem Kick-off-Workshop zur Testplanung ein und holen Sie aktiv Input zu Qualitätszielen, Risiken und Prioritäten ein. Stakeholder-Einbindung schafft Akzeptanz und verhindert späte Überraschungen.",
                    "mid": "Strukturieren Sie die Stakeholder-Einbindung mit einem klaren Format: Definieren Sie, wer wann und in welcher Form konsultiert wird, und dokumentieren Sie Rückmeldungen und Entscheidungen im Testplan.",
                },
            },
            {
                "id": "tp-8",
                "text": "Es besteht ein gemeinsames Verständnis von Qualitätszielen zwischen Stakeholdern und Testteam.",
                "hint": None,
                "recommendations": {
                    "low": "Erarbeiten Sie zu Projektbeginn gemeinsam mit allen relevanten Stakeholdern ein dokumentiertes Set von Qualitätszielen und lassen Sie es von allen Beteiligten bestätigen. Fehlende Einigkeit über Qualitätsziele ist eine der häufigsten Ursachen für Konflikte am Projektende.",
                    "mid": "Überprüfen Sie, ob das bestehende Verständnis der Qualitätsziele wirklich geteilt wird – z.B. durch eine kurze Abfrage oder einen Workshop – und stellen Sie sicher, dass Qualitätsziele messbar formuliert sind und bei Projektänderungen aktualisiert werden.",
                },
            },
            {
                "id": "tp-9",
                "text": "Eine Person des Testteams wird in die Projektplanung einbezogen, sodass Abhängigkeiten zwischen Testprozess und anderen Prozessen berücksichtigt werden können.",
                "hint": "Ist jemand aus dem Testteam von Anfang an im Projekt dabei?",
                "recommendations": {
                    "low": "Benennen Sie eine verantwortliche Person aus dem Testteam, die von Anfang an in die Projektplanung eingebunden ist und sicherstellt, dass Testabhängigkeiten (z.B. Lieferpunkte, Umgebungsverfügbarkeit) im Gesamtplan berücksichtigt werden.",
                    "mid": "Stellen Sie sicher, dass die eingebundene Testperson nicht nur informiert wird, sondern aktiv an Planungsentscheidungen mitwirkt und bei Änderungen konsultiert wird, die sich auf den Testprozess auswirken.",
                },
            },
            {
                "id": "tp-10",
                "text": "Risiken für die Testplanung selbst (z.B. Ressourcenverfügbarkeit, Lieferverzögerungen) werden identifiziert und bewertet.",
                "hint": None,
                "recommendations": {
                    "low": "Führen Sie zu Projektbeginn eine strukturierte Risikoidentifikation für die Testplanung durch: Analysieren Sie potenzielle Risiken wie Ressourcenengpässe, verspätete Lieferungen oder instabile Umgebungen und dokumentieren Sie Gegenmaßnahmen.",
                    "mid": "Überprüfen Sie, ob die identifizierten Planungsrisiken regelmäßig aktualisiert werden und ob Gegenmaßnahmen tatsächlich umgesetzt und auf ihre Wirksamkeit hin überwacht werden.",
                },
                "new": True,
            },
        ],
    },
    {
        "id": "ueberwachung",
        "title": "Testüberwachung und -steuerung",
        "parent": "Stufe 2 - Managed",
        "description": (
            "Regelmäßige, zielgruppengerechte Berichterstattung und definierte "
            "Kommunikationswege geben dem Auftraggeber und den Stakeholdern "
            "die Informationen, um Entscheidungen über die Produktqualität zu treffen."
        ),
        "questions": [
            {
                "id": "ueb-1",
                "text": "Es gibt ein standardisiertes Reporting-Format für Testfortschritt und -status.",
                "hint": None,
                "recommendations": {
                    "low": "Entwickeln Sie eine standardisierte Reportingvorlage, die Testfortschritt, Testabdeckung, offene Defects und Risiken übersichtlich darstellt. Eine einheitliche Vorlage spart Zeit, erhöht die Transparenz und erleichtert den Vergleich über Projekte hinweg.",
                    "mid": "Überprüfen Sie das vorhandene Reporting-Format auf Vollständigkeit und Verständlichkeit für die Zielgruppen und optimieren Sie es auf Basis von Rückmeldungen der Stakeholder – insbesondere hinsichtlich Übersichtlichkeit und Entscheidungsrelevanz.",
                },
            },
            {
                "id": "ueb-2",
                "text": "Testberichte werden regelmäßig (z.B. täglich/wöchentlich) erstellt und verteilt.",
                "hint": None,
                "recommendations": {
                    "low": "Etablieren Sie einen festen Reporting-Rhythmus (z.B. wöchentlich) mit einer verantwortlichen Person und einem definierten Verteilerkreis. Regelmäßige Berichte schaffen Vertrauen und ermöglichen frühzeitiges Eingreifen bei Problemen.",
                    "mid": "Überprüfen Sie, ob der bestehende Rhythmus zur Projektdynamik passt – in intensiven Testphasen kann ein tägliches Reporting sinnvoll sein – und stellen Sie sicher, dass Berichte tatsächlich gelesen und als Basis für Entscheidungen genutzt werden.",
                },
            },
            {
                "id": "ueb-3",
                "text": "Berichte enthalten aussagekräftige Informationen zu Testabdeckung, offenen Defects und Risiken.",
                "hint": None,
                "recommendations": {
                    "low": "Stellen Sie sicher, dass Ihre Testberichte neben dem reinen Fortschritt auch Testabdeckung, offene kritische Defects und aktuelle Risiken enthalten. Ergänzen Sie eine kurze Bewertung, die Handlungsempfehlungen für die Stakeholder ableitet.",
                    "mid": "Überprüfen Sie die Berichte auf inhaltliche Qualität: Sind die dargestellten Informationen tatsächlich entscheidungsrelevant, oder enthalten sie vor allem Datenmüll? Reduzieren Sie Informationsüberflutung und schärfen Sie den Fokus auf steuerungsrelevante Kennzahlen.",
                },
            },
            {
                "id": "ueb-4",
                "text": "Abschlussberichte (Test Summary Reports) werden am Ende von Testphasen erstellt.",
                "hint": None,
                "recommendations": {
                    "low": "Erstellen Sie am Ende jeder Testphase einen Test Summary Report, der Testergebnisse, Defect-Statistiken, Abdeckungsgrad und offene Risiken zusammenfasst. Selbst ein knapper Bericht schafft wichtige Dokumentation für Freigabeentscheidungen und zukünftige Projekte.",
                    "mid": "Standardisieren Sie den Test Summary Report durch eine Vorlage und stellen Sie sicher, dass er als Grundlage für die Go-Live-Entscheidung genutzt und von Entscheidungsträgern aktiv bestätigt wird.",
                },
            },
            {
                "id": "ueb-5",
                "text": "Berichte sind zielgruppengerecht aufbereitet (Management vs. operative Ebene).",
                "hint": None,
                "recommendations": {
                    "low": "Erstellen Sie mindestens zwei Varianten Ihrer Testberichte: eine Executive Summary für das Management (eine Seite, Ampelstatus, Risiken) und einen operativen Detailbericht für das Entwicklungs- und Testteam. Unterschiedliche Zielgruppen benötigen unterschiedliche Informationstiefe.",
                    "mid": "Holen Sie aktives Feedback von Management und operativem Team zu den vorhandenen Berichten ein und optimieren Sie Format und Inhalt gezielt für die jeweilige Entscheidungssituation der Zielgruppe.",
                },
            },
            {
                "id": "ueb-6",
                "text": "Testergebnisse werden von Stakeholdern als Entscheidungsgrundlage (z.B. für Go-Live) akzeptiert und genutzt.",
                "hint": None,
                "recommendations": {
                    "low": "Definieren Sie explizit, welche Testergebnisse welche Entscheidungen auslösen (z.B. Testabdeckung ≥ X % und keine offenen Critical Bugs = Go-Live-Freigabe) und kommunizieren Sie diese Kriterien vorab an alle Entscheidungsträger.",
                    "mid": "Überprüfen Sie, ob Testergebnisse in der Praxis tatsächlich als Entscheidungsgrundlage genutzt werden oder ob Go-Live-Entscheidungen unabhängig davon getroffen werden, und wirken Sie aktiv auf eine verbindliche Nutzung hin.",
                },
            },
            {
                "id": "ueb-7",
                "text": "Es gibt definierte Kommunikationswege zwischen Testteam, Entwicklung und Management.",
                "hint": None,
                "recommendations": {
                    "low": "Dokumentieren Sie die Kommunikationswege zwischen Testteam, Entwicklung und Management schriftlich: Wer informiert wen, auf welchem Weg, in welcher Häufigkeit? Eine klare Kommunikationsmatrix verhindert Informationslücken und Missverständnisse.",
                    "mid": "Überprüfen Sie, ob die definierten Kommunikationswege in der Praxis genutzt werden und ob Informationen tatsächlich die richtigen Empfänger zur richtigen Zeit erreichen. Passen Sie die Kanäle und Formate bei Bedarf an.",
                },
            },
            {
                "id": "ueb-8",
                "text": "Es existieren standardisierte Meetings (z.B. Daily, Testfortschrittsmeetings, Defect Triage).",
                "hint": "Gibt es ein Statusmeeting über den Testfortschritt und Fehler?",
                "recommendations": {
                    "low": "Etablieren Sie mindestens ein wöchentliches Testfortschrittsmeeting und eine regelmäßige Defect-Triage mit festen Teilnehmern, Agenda und Entscheidungsprotokoll. Strukturierte Meetings verkürzen Kommunikationswege und beschleunigen die Fehlerbehebung.",
                    "mid": "Überprüfen Sie, ob die bestehenden Meetings effektiv sind: Werden Entscheidungen getroffen, Aktionspunkte verfolgt und Ergebnisse dokumentiert? Reduzieren Sie bei Bedarf Frequenz oder Teilnehmerkreis, um die Effizienz zu steigern.",
                },
            },
            {
                "id": "ueb-9",
                "text": "Relevante Informationen (Anforderungsänderungen, Risiken) werden zeitnah an das Testteam weitergegeben.",
                "hint": "Fragen Sie regelmäßig nach veränderten/aktualisierten Anforderungen oder neuen Entwicklungen?",
                "recommendations": {
                    "low": "Richten Sie einen klaren Prozess ein, über den Anforderungsänderungen und Risikoinformationen das Testteam rechtzeitig erreichen – z.B. durch eine Verteilerliste oder einen definierten Benachrichtigungskanal. Verspätete Informationen führen zu aufwändigen Nacharbeiten.",
                    "mid": "Überprüfen Sie, ob Informationen wirklich zeitnah ankommen und vom Testteam effektiv verarbeitet werden. Implementieren Sie bei Bedarf einen formalen Change-Notification-Prozess mit definierten SLAs für Reaktionszeiten.",
                },
            },
            {
                "id": "ueb-10",
                "text": "Das Testteam gibt vorausschauend Hinweise auf Verzögerungen/Probleme an die Stakeholder.",
                "hint": "Ist im Status eine Risikoabfrage vorhanden? Wie werden Probleme im Test adressiert?",
                "recommendations": {
                    "low": "Schulen Sie das Testteam darin, Risiken und Verzögerungen frühzeitig zu erkennen und aktiv zu kommunizieren, anstatt sie reaktiv zu melden. Etablieren Sie eine Kultur, in der proaktive Eskalation als professionelles Verhalten gilt.",
                    "mid": "Formalisieren Sie das proaktive Risikoreporting durch eine feste Agenda-Position in Statusmeetings und ein standardisiertes Format, das zwischen Risikowahrscheinlichkeit, Auswirkung und empfohlener Gegenmaßnahme unterscheidet.",
                },
            },
            {
                "id": "ueb-11",
                "text": "Abweichungen vom Testplan (Zeit, Aufwand, Abdeckung) werden erkannt und es werden Korrekturmaßnahmen eingeleitet.",
                "hint": None,
                "recommendations": {
                    "low": "Definieren Sie Schwellenwerte, bei denen Abweichungen vom Testplan (z.B. Aufwandsüberschreitung > 20 %, Abdeckungslücken) eine formale Eskalation auslösen. Ohne definierte Trigger werden Abweichungen oft zu spät erkannt.",
                    "mid": "Stellen Sie sicher, dass erkannte Abweichungen nicht nur gemeldet, sondern systematisch analysiert und mit konkreten Korrekturmaßnahmen hinterlegt werden, deren Umsetzung nachverfolgt und auf Wirksamkeit geprüft wird.",
                },
                "new": True,
            },
        ],
    },
    {
        "id": "testfalldesign_durchfuehrung",
        "title": "Testfalldesign und -durchführung",
        "parent": "Stufe 2 - Managed",
        "description": (
            "Setzt die Teststrategie um, indem Testfälle systematisch aus "
            "Anforderungen abgeleitet, nachvollziehbar dokumentiert und "
            "Ergebnisse über ein definiertes Fehlermanagement verfolgt werden."
        ),
        "questions": [
            {
                "id": "tfd-1",
                "text": "Testfälle werden systematisch aus Anforderungen/User Stories abgeleitet.",
                "hint": None,
                "recommendations": {
                    "low": "Führen Sie einen definierten Ableitungsprozess ein: Für jede Anforderung oder User Story werden explizit Testfälle abgeleitet und die Verbindung dokumentiert. Eine einfache Tabelle mit Anforderungs-ID und zugehörigen Testfall-IDs reicht als Ausgangspunkt.",
                    "mid": "Überprüfen Sie, ob die Ableitung konsistent und vollständig erfolgt – insbesondere für Akzeptanzkriterien und Negativszenarien – und ob alle Teammitglieder denselben Ableitungsprozess anwenden.",
                },
            },
            {
                "id": "tfd-2",
                "text": "Es gibt definierte Qualitätskriterien für Testfälle (z.B. Klarheit, Nachvollziehbarkeit, Wiederholbarkeit).",
                "hint": None,
                "recommendations": {
                    "low": "Definieren Sie schriftliche Qualitätskriterien für Testfälle (z.B. klare Ausgangssituation, eindeutiges erwartetes Ergebnis, Wiederholbarkeit ohne Rückfragen) und machen Sie diese für alle Tester verbindlich zugänglich.",
                    "mid": "Überprüfen Sie bestehende Testfälle stichprobenartig auf Einhaltung der definierten Qualitätskriterien und nutzen Sie die Ergebnisse, um gezielte Verbesserungen und bei Bedarf kurze Schulungen für das Team einzuleiten.",
                },
            },
            {
                "id": "tfd-3",
                "text": "Jeder Testfall enthält: Ausgangssituation, Beschreibung der Aktionen und das erwartete Ergebnis.",
                "hint": None,
                "recommendations": {
                    "low": "Stellen Sie sicher, dass alle neuen Testfälle nach einem einheitlichen Template erstellt werden, das explizit Ausgangssituation, durchzuführende Aktionen und das erwartete Ergebnis fordert. Ergänzen Sie bestehende Testfälle schrittweise um fehlende Angaben.",
                    "mid": "Überprüfen Sie den vorhandenen Testfallbestand stichprobenartig auf Vollständigkeit der drei Pflichtbestandteile und definieren Sie im Rahmen eines Reviews einen Plan, um Lücken strukturiert zu schließen.",
                },
            },
            {
                "id": "tfd-4",
                "text": "Das zugehörige Testobjekt (=Teil der Testbasis, das getestet wird) ist im Testfall genannt.",
                "hint": None,
                "recommendations": {
                    "low": "Ergänzen Sie alle neuen Testfälle um ein Pflichtfeld 'Testobjekt', das angibt, welche Anforderung, Funktion oder welches Modul getestet wird. Das erleichtert die Zuordnung von Testfällen zu Fehlerursachen erheblich.",
                    "mid": "Überprüfen Sie den bestehenden Testfallbestand auf Vollständigkeit des Testobjekt-Feldes und stellen Sie sicher, dass die verwendeten Testobjektbezeichnungen konsistent mit der Anforderungsdokumentation sind.",
                },
            },
            {
                "id": "tfd-5",
                "text": "Die Abdeckung der Testfälle in Bezug auf Anforderungen ist messbar und nachvollziehbar (Traceability-Matrix).",
                "hint": "Ist der Weg von Anforderung zu Testfall zu Fehler nachvollziehbar?",
                "recommendations": {
                    "low": "Erstellen Sie eine einfache Traceability-Matrix (z.B. in Excel), die Anforderungen, zugehörige Testfälle und deren Status verknüpft. Diese Matrix zeigt sofort, welche Anforderungen ungetestet sind, und ist die Grundlage für eine fundierte Abdeckungsanalyse.",
                    "mid": "Überprüfen Sie, ob die Traceability-Matrix aktuell gepflegt wird und ob sie tatsächlich genutzt wird, um Testabdeckungslücken vor dem Release zu identifizieren und gezielt zu schließen.",
                },
            },
            {
                "id": "tfd-6",
                "text": "Testfälle für unterschiedliche Testarten (positiv/negativ, Grenzwerte, Fehlerfälle) werden systematisch erstellt.",
                "hint": None,
                "recommendations": {
                    "low": "Stellen Sie sicher, dass bei der Testfallplanung systematisch nicht nur positive Szenarien, sondern auch Negativfälle, Grenzwerte und Fehlerfälle berücksichtigt werden. Eine kurze Checkliste als Designhilfe hilft Testern, keine Testarten zu vergessen.",
                    "mid": "Überprüfen Sie, ob Testfälle für alle relevanten Testarten ausgewogen verteilt sind, und analysieren Sie stichprobenartig die Testfallbibliothek auf Schwerpunkte und Lücken. Ergänzen Sie fehlende Testarten gezielt.",
                },
            },
            {
                "id": "tfd-7",
                "text": "Es existiert ein definierter Defect-Management-Prozess (Erfassung, Klassifikation, Priorisierung, Behebung, Verifikation), der dem Team bekannt ist.",
                "hint": "Wie sind die Phasen des Fehlerlebenszyklus? Wer entscheidet, ob ein Fehler geschlossen wird?",
                "recommendations": {
                    "low": "Dokumentieren Sie einen klaren Defect-Management-Prozess, der die Phasen Erfassung, Klassifikation, Priorisierung, Behebung und Verifikation beschreibt und jeweils Verantwortlichkeiten benennt. Stellen Sie sicher, dass alle Beteiligten mit dem Prozess vertraut sind.",
                    "mid": "Überprüfen Sie, ob der dokumentierte Prozess in der Praxis konsequent eingehalten wird, und klären Sie Unklarheiten – insbesondere zu Zuständigkeiten für das Schließen und die Eskalation von Defects – durch gezielte Schulungen oder Teamvereinbarungen.",
                },
            },
            {
                "id": "tfd-8",
                "text": "Ein einheitliches Tool zur Fehlererfassung wird genutzt und ist für alle Verantwortlichen einsehbar.",
                "hint": "Sind die Fehler für alle einsehbar? Sind Schweredefinitionen transparent und bekannt?",
                "recommendations": {
                    "low": "Etablieren Sie ein einheitliches Fehlermanagement-Tool (z.B. Jira, Azure DevOps oder als Übergangslösung ein einfaches Excel-Template), das für alle Projektbeteiligten zugänglich und schreibberechtigt ist.",
                    "mid": "Überprüfen Sie, ob das vorhandene Tool konsistent genutzt wird und ob alle relevanten Stakeholder die nötigen Zugriffsrechte haben. Klären Sie, ob Schweredefinitionen und Status-Übergänge für alle sichtbar und einheitlich verstanden werden.",
                },
            },
            {
                "id": "tfd-9",
                "text": "Kriterien für Schweregrad und Priorität von Defects sind klar definiert.",
                "hint": None,
                "recommendations": {
                    "low": "Definieren Sie schriftlich und für alle sichtbar, was die verschiedenen Schweregrade (Critical, Major, Minor, Trivial) und Prioritäten bedeuten und wann sie anzuwenden sind. Beispiele aus dem Projektkontext helfen dabei, Missverständnisse zu vermeiden.",
                    "mid": "Überprüfen Sie, ob die vorhandenen Definitionen tatsächlich einheitlich angewendet werden, indem Sie aktuelle Defects stichprobenartig begutachten. Klären Sie Inkonsistenzen im Team und aktualisieren Sie die Definitionen bei Bedarf.",
                },
            },
            {
                "id": "tfd-10",
                "text": "Die Mindestattribute jedes Fehlers sind: Ersteller/Tester, ID, Datum, Schwere, Beschreibung (erwartetes vs. tatsächliches Ergebnis), Titel, Status.",
                "hint": "Welche Attribute werden in einem Fehler ausgefüllt?",
                "recommendations": {
                    "low": "Legen Sie verbindlich fest, welche Pflichtfelder jeder Fehlerbericht enthalten muss (mindestens: Titel, Ersteller, Datum, Schweregrad, Beschreibung mit erwartetem vs. tatsächlichem Ergebnis, Status) und konfigurieren Sie das Tool entsprechend.",
                    "mid": "Überprüfen Sie bestehende Fehlerberichte auf Vollständigkeit der Mindestattribute und schulen Sie das Team dort, wo regelmäßig Felder fehlen oder unvollständig ausgefüllt werden.",
                },
            },
            {
                "id": "tfd-11",
                "text": "Es gibt einen definierten Workflow inkl. Eskalationsmechanismen für offene/kritische Defects.",
                "hint": None,
                "recommendations": {
                    "low": "Definieren Sie einen klaren Defect-Workflow mit allen möglichen Status-Übergängen und Verantwortlichkeiten sowie explizite Eskalationspfade für Defects, die nicht innerhalb definierter SLAs behoben werden.",
                    "mid": "Überprüfen Sie, ob der vorhandene Workflow tatsächlich gelebt wird – insbesondere ob Eskalationsmechanismen bekannt sind und bei kritischen offenen Defects genutzt werden – und passen Sie SLAs und Eskalationspfade bei Bedarf an.",
                },
            },
            {
                "id": "tfd-12",
                "text": "Der Umgang mit Fehlernachtests (komplett/partiell) ist definiert.",
                "hint": "Was wird nach der Behebung eines Fehlers getestet? Gibt es Richtlinien zum Umfang des Nachtests?",
                "recommendations": {
                    "low": "Definieren Sie schriftlich, welcher Nachtest-Umfang nach einer Fehlerbehebung durchgeführt wird: Wann reicht ein partieller Nachtest, wann ist ein vollständiger Regressionstest erforderlich? Klare Regeln reduzieren Unsicherheiten und Ad-hoc-Entscheidungen.",
                    "mid": "Überprüfen Sie, ob die Nachtest-Regeln konsequent angewendet werden, und analysieren Sie, ob Defects nach der Behebung ausreichend verifiziert werden, bevor sie geschlossen werden.",
                },
            },
            {
                "id": "tfd-13",
                "text": "Testergebnisse (Pass/Fail) werden pro Testfall dokumentiert und sind nachvollziehbar.",
                "hint": None,
                "recommendations": {
                    "low": "Stellen Sie sicher, dass für jeden ausgeführten Testfall das Ergebnis (Pass/Fail) mit Datum und ausführender Person dokumentiert wird. Das ist die Mindestvoraussetzung für eine nachvollziehbare Testdurchführung und fundierte Freigabeentscheidungen.",
                    "mid": "Überprüfen Sie, ob die Testergebnisdokumentation vollständig und aktuell ist, und stellen Sie sicher, dass fehlgeschlagene Testfälle klar mit zugehörigen Defects verknüpft sind, um Lücken in der Nachverfolgung zu vermeiden.",
                },
                "new": True,
            },
        ],
    },
    {
        "id": "testumgebung",
        "title": "Testumgebung",
        "parent": "Stufe 2 - Managed",
        "description": (
            "Die Testumgebung ist auf die Ziele der einzelnen Teststufen "
            "abgestimmt, wird verwaltet und steht in den definierten "
            "Testzeiträumen verlässlich zur Verfügung."
        ),
        "questions": [
            {
                "id": "tum-1",
                "text": "Für Testaktivitäten stehen dedizierte, produktionsähnliche Testumgebungen zur Verfügung.",
                "hint": None,
                "recommendations": {
                    "low": "Stellen Sie sicher, dass separate Testumgebungen (unabhängig von Entwicklungs- und Produktionsumgebungen) vorhanden sind und deren Konfiguration der Produktionsumgebung möglichst nahekommt. Umgebungsunterschiede sind eine häufige Ursache für Fehler, die erst in Produktion auftreten.",
                    "mid": "Überprüfen Sie systematisch, inwieweit Testumgebungen von der Produktionsumgebung abweichen (z.B. andere Datenbankversionen, fehlende Integrationen), und priorisieren Sie die Beseitigung kritischer Abweichungen.",
                },
            },
            {
                "id": "tum-2",
                "text": "Es gibt klar definierte Anforderungen an die Testumgebung.",
                "hint": "Wie viele User können gleichzeitig die Umgebung nutzen? Welche Verfügbarkeiten gibt es?",
                "recommendations": {
                    "low": "Erstellen Sie eine schriftliche Spezifikation der Anforderungen an die Testumgebung (Hardware, Software, Konfiguration, Datenbankstand, Schnittstellen, Verfügbarkeit) und stimmen Sie diese mit Betrieb und Architektur ab.",
                    "mid": "Überprüfen Sie, ob die vorhandenen Anforderungen vollständig und aktuell sind, und stellen Sie sicher, dass alle wesentlichen Anforderungen an Verfügbarkeit, Performance und Konfiguration der Testumgebung explizit dokumentiert und mit allen Verantwortlichen vereinbart sind.",
                },
            },
            {
                "id": "tum-3",
                "text": "Es gibt einen definierten Prozess für Bereitstellung, Konfiguration und Verwaltung von Testumgebungen, inkl. zugeordneter Verantwortlichkeiten (z.B. Umgebungsmanager).",
                "hint": "Wer ist für die Umgebung verantwortlich? Wer informiert über Downtimes und Testzeiten?",
                "recommendations": {
                    "low": "Benennen Sie einen Umgebungsmanager mit klarer Verantwortlichkeit für Bereitstellung, Konfiguration und Betrieb der Testumgebungen. Dokumentieren Sie den Bereitstellungsprozess schriftlich, damit die Umgebung reproduzierbar aufgesetzt werden kann.",
                    "mid": "Überprüfen Sie, ob der vorhandene Prozess für Umgebungsbereitstellung vollständig dokumentiert, für alle Beteiligten zugänglich und tatsächlich konsistent angewendet wird. Identifizieren Sie Engpässe und automatisieren Sie manuelle Schritte, wo möglich.",
                },
            },
            {
                "id": "tum-4",
                "text": "Die Verfügbarkeit der Testumgebungen wird geplant und überwacht (Umgebungsmanagement).",
                "hint": "Steht die Umgebung während des Tests uneingeschränkt zur Verfügung?",
                "recommendations": {
                    "low": "Erstellen Sie einen Umgebungsnutzungsplan, der festlegt, wann welches Team die Testumgebung nutzt, und richten Sie ein einfaches Monitoring (z.B. Benachrichtigungen bei Ausfällen) ein, um Downtimes frühzeitig zu erkennen.",
                    "mid": "Überprüfen Sie, ob Umgebungsausfälle und -konflikte regelmäßig analysiert werden, und implementieren Sie eine vorausschauende Umgebungsplanung, die Testphasen und Wartungsfenster koordiniert.",
                },
            },
            {
                "id": "tum-5",
                "text": "Es existiert ein Konzept für Testdatenmanagement (Erstellung, Anonymisierung, Aktualisierung).",
                "hint": "Sind Testdaten auf allen Umgebungen für den Test vorhanden? Sind diese vollständig nutzbar?",
                "recommendations": {
                    "low": "Definieren Sie, wie Testdaten erstellt, bereitgestellt und – insbesondere bei personenbezogenen Daten – anonymisiert werden. Selbst ein einfaches Konzept, das sicherstellt, dass Testdaten vollständig und rechtskonform vorhanden sind, ist ein wichtiger erster Schritt.",
                    "mid": "Überprüfen Sie, ob Testdaten aktuell, vollständig und für alle Testszenarien geeignet sind, und stellen Sie sicher, dass Anonymisierungsverfahren datenschutzkonform umgesetzt und bei Datenbankaktualisierungen konsistent angewendet werden.",
                },
            },
            {
                "id": "tum-6",
                "text": "Konflikte bei der gemeinsamen Nutzung von Testumgebungen durch mehrere Teams werden aktiv gemanagt.",
                "hint": None,
                "recommendations": {
                    "low": "Führen Sie eine einfache Umgebungsbuchungsübersicht ein (z.B. gemeinsamer Kalender), über die Teams die Nutzungszeiten koordinieren und Konflikte sichtbar machen können. Eine transparente Planung verhindert Blockierungen und Testunterbrechungen.",
                    "mid": "Überprüfen Sie, ob Nutzungskonflikte proaktiv erkannt und gelöst werden, und erwägen Sie technische Lösungen (z.B. Isolation durch Container oder eigene Umgebungen pro Team), um strukturelle Konflikte dauerhaft zu beseitigen.",
                },
            },
            {
                "id": "tum-7",
                "text": "Änderungen der Testumgebung werden rechtzeitig an den Testmanager herangetragen und können bei Bedarf eingefroren werden (Change Management/Freeze).",
                "hint": "Gibt es ein Change Management für Änderungen? Kann ein Freeze der Umgebung eingefordert werden?",
                "recommendations": {
                    "low": "Definieren Sie einen klaren Prozess, über den geplante Änderungen an der Testumgebung mindestens einige Werktage vorab an den Testmanager gemeldet werden, und legen Sie fest, unter welchen Bedingungen ein Umgebungsfreeze eingefordert werden kann.",
                    "mid": "Überprüfen Sie, ob der bestehende Change-Management-Prozess für Testumgebungen eingehalten wird und ob Änderungen tatsächlich rechtzeitig kommuniziert werden. Etablieren Sie klare SLAs für Vorankündigungsfristen.",
                },
            },
            {
                "id": "tum-8",
                "text": "Anforderungen an die Testumgebung werden frühzeitig spezifiziert und mit Architektur/Betrieb abgestimmt.",
                "hint": None,
                "recommendations": {
                    "low": "Stellen Sie sicher, dass Testumgebungsanforderungen bereits in der Projektplanungsphase – nicht erst kurz vor Testbeginn – spezifiziert und mit Architektur und Betrieb abgestimmt werden. Späte Anforderungen führen zu langen Vorlaufzeiten und Testverzögerungen.",
                    "mid": "Etablieren Sie einen festen Meilenstein in Ihrer Projektplanung, zu dem Testumgebungsanforderungen vollständig vorliegen und mit allen beteiligten Stellen (Betrieb, Architektur, Sicherheit) formell bestätigt sind.",
                },
                "new": True,
            },
        ],
    },

    # =========================================================================
    # STUFE 3: DEFINED (DEFINIERT)
    # =========================================================================
    {
        "id": "testorganisation",
        "title": "Testorganisation",
        "parent": "Stufe 3 - Defined",
        "description": (
            "Die Testorganisation ist Wissensträger und sorgt dafür, dass "
            "Testressourcen, Testprodukte (Prozesse, Werkzeuge, Templates, "
            "Richtlinien) und Testdienstleistungen organisationsweit vorhanden sind."
        ),
        "questions": [
            {
                "id": "org-1",
                "text": "Es gibt eine klar definierte Aufbauorganisation für das Testen (Rollen, Verantwortlichkeiten, Reporting-Linien).",
                "hint": "Gibt es klar definierte Verantwortlichkeiten? Kennen Sie Ihre Rolle und Aufgaben?",
                "recommendations": {
                    "low": "Erstellen Sie ein Organisationsdiagramm für das Testen, das Rollen, Verantwortlichkeiten und Reporting-Linien klar zeigt, und stellen Sie es allen Testbeteiligten zur Verfügung. Klarheit über Zuständigkeiten ist die Grundlage für eine funktionierende Zusammenarbeit.",
                    "mid": "Überprüfen Sie, ob die bestehende Aufbauorganisation für alle Beteiligten bekannt und aktuell ist, und klären Sie Unklarheiten zu Schnittstellen und Verantwortlichkeiten durch eine aktuelle Rollenmatrix.",
                },
            },
            {
                "id": "org-2",
                "text": "Es existiert eine zentrale Testfunktion oder ein Testkompetenzzentrum (Test Center of Excellence).",
                "hint": "Existiert eine Organisations- oder Projekteinheit, die für Testprodukte und Hilfestellungen verantwortlich ist?",
                "recommendations": {
                    "low": "Benennen Sie eine zentrale Stelle (auch wenn es zunächst nur eine Person ist), die übergreifend für Teststandards, Werkzeuge, Templates und Beratung zuständig ist. Eine zentrale Anlaufstelle für Testthemen verhindert parallele Lösungen und sichert Qualitätsstandards.",
                    "mid": "Überprüfen Sie, ob die vorhandene zentrale Testfunktion alle wesentlichen Aufgaben wahrnimmt (Standardisierung, Tool-Governance, Beratung, Schulung) und ob sie von den Projekten aktiv genutzt wird. Schärfen Sie das Leistungsangebot bei Bedarf.",
                },
            },
            {
                "id": "org-3",
                "text": "Rollen wie Testmanager, Testanalyst und Testautomatisierer sind klar voneinander abgegrenzt, inklusive Namen.",
                "hint": "Gibt es eine Rollenübersicht (Tester, Testdesigner, Entwickler, Releasemanager, Umgebungsmanager, Projektleiter, Testmanager, Defectmanager)?",
                "recommendations": {
                    "low": "Erstellen Sie eine Rollenbeschreibung für alle wesentlichen Testrollen (mindestens Testmanager, Testanalyst, Testautomatisierer) mit klaren Aufgaben, Verantwortlichkeiten und Abgrenzungen zu anderen Rollen – und ordnen Sie alle Personen explizit zu.",
                    "mid": "Überprüfen Sie, ob die vorhandenen Rollenbeschreibungen aktuell sind und ob Abgrenzungen in der Praxis funktionieren. Klären Sie Überschneidungen und Lücken und stellen Sie sicher, dass alle Beteiligten ihre Rolle kennen.",
                },
            },
            {
                "id": "org-4",
                "text": "Die Unabhängigkeit der Testorganisation von der Entwicklung ist angemessen sichergestellt.",
                "hint": None,
                "recommendations": {
                    "low": "Analysieren Sie, inwieweit das Testteam derzeit von der Entwicklung abhängig ist (z.B. Reporting-Linien, Werkzeugzugang, Budgethoheit), und identifizieren Sie die dringendsten Maßnahmen zur Stärkung der Unabhängigkeit.",
                    "mid": "Überprüfen Sie, ob die organisatorische Unabhängigkeit in der Praxis ausreichend wirkt – insbesondere ob Tester unter Druck gesetzt werden, Defects zu schließen oder Freigaben zu erteilen – und ergreifen Sie strukturelle oder kulturelle Maßnahmen bei Bedarf.",
                },
            },
            {
                "id": "org-5",
                "text": "Es gibt eine organisationsweite Teststandardisierung (Vorlagen, Prozesse, Tools), die den Testern bekannt ist.",
                "hint": "Existiert eine Übersicht der Produkte und Dienstleistungen (z.B. Templates) der Abteilung?",
                "recommendations": {
                    "low": "Erstellen Sie eine zentrale Übersicht der verfügbaren Teststandards, Vorlagen und Prozesse und kommunizieren Sie sie aktiv an alle Tester. Standardisierung erhöht die Konsistenz und spart Aufwand durch Wiederverwendung.",
                    "mid": "Überprüfen Sie, ob die vorhandenen Standards tatsächlich angewendet werden, und erheben Sie stichprobenartig, welche Vorlagen und Prozesse in Projekten genutzt werden und wo Abweichungen entstehen. Passen Sie den Standardisierungsgrad an den tatsächlichen Bedarf an.",
                },
            },
            {
                "id": "org-6",
                "text": "Testressourcen werden sinnvoll über Projekte hinweg verteilt.",
                "hint": None,
                "recommendations": {
                    "low": "Erstellen Sie eine Übersicht der verfügbaren Testressourcen (Personen, Kompetenzen) und der Projekte, in denen sie eingesetzt sind, um eine transparente und faire Ressourcenverteilung zu ermöglichen und Überlastungen frühzeitig zu erkennen.",
                    "mid": "Implementieren Sie einen regelmäßigen Ressourcenabgleich (z.B. monatlich), bei dem die Testleitung Kapazitäten und Projektbedarfe gegenüberstellt und bei Engpässen proaktiv Lösungen erarbeitet.",
                },
            },
            {
                "id": "org-7",
                "text": "Geeignete Tools für Testmanagement, Testautomatisierung und Defect-Tracking werden eingesetzt und sind dem Testteam bekannt.",
                "hint": "Welche Testwerkzeuge werden genutzt? Sind diese zugänglich für das gesamte Team?",
                "recommendations": {
                    "low": "Stellen Sie sicher, dass alle Testteammitglieder wissen, welche Tools zur Verfügung stehen, wie sie lizensiert sind und wie man Zugang erhält. Eine einfache Tool-Übersicht mit Links und Ansprechpartnern reicht als Ausgangspunkt.",
                    "mid": "Überprüfen Sie, ob die vorhandenen Tools tatsächlich effektiv genutzt werden, und identifizieren Sie durch Interviews oder Nutzungsanalysen Schulungsbedarf und ungenutzte Potenziale.",
                },
            },
            {
                "id": "org-8",
                "text": "Die eingesetzten Tools sind integriert (z.B. Anbindung an CI/CD-Pipeline, ALM-Tools).",
                "hint": None,
                "recommendations": {
                    "low": "Identifizieren Sie die wesentlichen Integrationspunkte zwischen Ihren Testwerkzeugen (z.B. Verbindung zwischen Fehlermanagement und Testmanagement-Tool) und planen Sie schrittweise Integrationen, die den größten Effizienzgewinn bringen.",
                    "mid": "Überprüfen Sie, ob vorhandene Integrationen stabil und aktuell sind, und evaluieren Sie, ob eine Anbindung an CI/CD-Pipelines oder ALM-Tools den Automatisierungsgrad und die Rückmeldungsgeschwindigkeit weiter verbessern würde.",
                },
            },
            {
                "id": "org-9",
                "text": "Es gibt eine strategische Auswahl und Bewertung von Testwerkzeugen (Tool-Strategie), bei der relevante Stakeholder (Einkauf, Projekt, Testteam) vom Nutzen überzeugt sind.",
                "hint": None,
                "recommendations": {
                    "low": "Definieren Sie Auswahlkriterien für Testwerkzeuge (z.B. Integrierbarkeit, Wartungsaufwand, Lizenzkosten, Benutzerfreundlichkeit) und stellen Sie sicher, dass Tool-Entscheidungen strukturiert und dokumentiert getroffen werden – nicht ad hoc.",
                    "mid": "Entwickeln Sie eine formale Tool-Strategie, die Einsatzbereiche, Standardwerkzeuge und Entscheidungsprozesse für neue Tools beschreibt, und binden Sie Einkauf, IT und Fachteams in Evaluierungsentscheidungen ein.",
                },
            },
            {
                "id": "org-10",
                "text": "Es gibt Schulungen zur effektiven Nutzung der Testwerkzeuge.",
                "hint": None,
                "recommendations": {
                    "low": "Stellen Sie sicher, dass neue Testteammitglieder eine strukturierte Einführung in die eingesetzten Tools erhalten und dass Schulungsmaterial (z.B. Kurzanleitungen, Tutorials) zugänglich ist.",
                    "mid": "Überprüfen Sie, ob alle Teammitglieder die Tools effektiv nutzen, und schließen Sie Wissenslücken durch gezielte Schulungen oder interne Wissensaustausch-Sessions zu fortgeschrittenen Funktionen und Best Practices.",
                },
            },
            {
                "id": "org-11",
                "text": "Es existiert ein definiertes, organisationsweites Standard-Testprozessmodell, von dem Projekte ihre eigenen Prozesse ableiten.",
                "hint": None,
                "recommendations": {
                    "low": "Entwickeln Sie ein einfaches, dokumentiertes Standard-Testprozessmodell, das die wesentlichen Phasen, Aktivitäten und Artefakte des Testprozesses beschreibt, und kommunizieren Sie es als verbindlichen Ausgangspunkt für alle Projekte.",
                    "mid": "Überprüfen Sie, ob das vorhandene Prozessmodell tatsächlich in Projekten als Ableitung genutzt wird, und stellen Sie sicher, dass es regelmäßig aktualisiert wird und die aktuellen Best Practices widerspiegelt.",
                },
                "new": True,
            },
        ],
    },
    {
        "id": "testschulung",
        "title": "Testschulungsprogramm",
        "parent": "Stufe 3 - Defined",
        "description": (
            "Beschreibt die richtige Mischung aus unterschiedlichen "
            "Fähigkeiten und Fachwissen sowie ein organisationsweites "
            "Schulungs- und Entwicklungskonzept für Testpersonal."
        ),
        "questions": [
            {
                "id": "sch-1",
                "text": "Die Tester verfügen über anerkannte Qualifikationen (z.B. ISTQB-Zertifizierungen, mind. Foundation Level).",
                "hint": None,
                "recommendations": {
                    "low": "Ermitteln Sie den aktuellen Qualifikationsstand der Tester und erstellen Sie einen Plan zur schrittweisen Einführung von ISTQB-Zertifizierungen (Foundation Level als Einstieg). Anerkannte Zertifizierungen schaffen ein gemeinsames Grundverständnis und sind branchenübergreifend anerkannt.",
                    "mid": "Überprüfen Sie, ob alle Tester mindestens über den ISTQB Foundation Level verfügen, und planen Sie für erfahrene Tester gezielte Weiterqualifizierungen auf Advanced Level (z.B. Test Manager, Test Analyst).",
                },
            },
            {
                "id": "sch-2",
                "text": "Es gibt ein Schulungs- und Weiterbildungskonzept für Testpersonal, das bei Bedarf genutzt werden kann.",
                "hint": "Gibt es Schulungen zu Testvorgaben? Ist eine Schulungsteilnahme bei Bedarf möglich?",
                "recommendations": {
                    "low": "Erstellen Sie ein einfaches Schulungskonzept, das beschreibt, welche Schulungen für welche Testrollen relevant sind, und stellen Sie sicher, dass Tester auf Anfrage an Schulungen teilnehmen können. Selbst ein jährliches Budget für Weiterbildung ist ein wichtiger erster Schritt.",
                    "mid": "Überprüfen Sie, ob das Schulungskonzept aktuell ist und aktiv genutzt wird, und stellen Sie sicher, dass Schulungsbedarfe systematisch erhoben und in jährlichen Entwicklungsplänen berücksichtigt werden.",
                },
            },
            {
                "id": "sch-3",
                "text": "Wissen wird innerhalb des Testteams aktiv ausgetauscht (z.B. durch Reviews, Pairing, interne Schulungen).",
                "hint": None,
                "recommendations": {
                    "low": "Etablieren Sie regelmäßige Formate für Wissensaustausch im Testteam – z.B. monatliche kurze Vorstellungen von Best Practices, Tools oder Lessons Learned. Aktiver Wissenstransfer verhindert Wissenssilos und steigert die Teamkompetenz nachhaltig.",
                    "mid": "Strukturieren Sie den Wissensaustausch mit einem Jahresplan und unterschiedlichen Formaten (Peer Review, Pairing, interne Workshops) und messen Sie, ob neues Wissen tatsächlich in der täglichen Arbeit angewendet wird.",
                },
            },
            {
                "id": "sch-4",
                "text": "Karrierepfade für Testrollen sind definiert.",
                "hint": None,
                "recommendations": {
                    "low": "Definieren Sie mindestens zwei bis drei Entwicklungsstufen für typische Testrollen (z.B. Junior Tester, Senior Tester, Testmanager) mit klaren Anforderungen und Entwicklungszielen. Das erhöht die Attraktivität der Testrollen und die Mitarbeiterbindung.",
                    "mid": "Überprüfen Sie, ob die definierten Karrierepfade mit HR abgestimmt sind und aktiv in Mitarbeitergesprächen genutzt werden, um individuelle Entwicklungsschritte zu vereinbaren und zu verfolgen.",
                },
            },
            {
                "id": "sch-5",
                "text": "Soft Skills (z.B. Kommunikation, kritisches Denken) werden bei der Personalentwicklung berücksichtigt.",
                "hint": None,
                "recommendations": {
                    "low": "Integrieren Sie Soft-Skill-Aspekte (z.B. Kommunikation, kritisches Denken, Stakeholder-Management) explizit in die Anforderungsprofile und Entwicklungspläne von Testpersonal und ermöglichen Sie den Zugang zu entsprechenden Schulungsangeboten.",
                    "mid": "Überprüfen Sie, ob Soft Skills tatsächlich bewertet und gefördert werden – z.B. durch 360°-Feedback oder gezielte Entwicklungsgespräche – und stellen Sie sicher, dass die Personalentwicklung fachliche und soziale Kompetenzen ausgewogen berücksichtigt.",
                },
            },
            {
                "id": "sch-6",
                "text": "Die fachliche Weiterentwicklung der Tester wird regelmäßig evaluiert (z.B. in Mitarbeitergesprächen) in Bezug auf Test- und IT-Fähigkeiten.",
                "hint": None,
                "recommendations": {
                    "low": "Stellen Sie sicher, dass die fachliche Weiterentwicklung von Testern in jährlichen Mitarbeitergesprächen explizit thematisiert wird und konkrete Entwicklungsvereinbarungen mit Terminen und Verantwortlichkeiten getroffen werden.",
                    "mid": "Überprüfen Sie, ob die getroffenen Entwicklungsvereinbarungen tatsächlich verfolgt und umgesetzt werden, und ergänzen Sie bei Bedarf unterjährige Folgegespräche, um Fortschritte zu überprüfen und Hindernisse zu beseitigen.",
                },
            },
            {
                "id": "sch-7",
                "text": "Der individuelle und organisationsweite Schulungsbedarf wird systematisch ermittelt und mit dem Testprozessmodell abgeglichen.",
                "hint": None,
                "recommendations": {
                    "low": "Führen Sie eine strukturierte Bedarfsanalyse durch, in der für jede Testrolle geprüft wird, welche Kompetenzen im Soll- und Ist-Zustand vorhanden sind, und leiten Sie daraus einen konkreten Schulungsplan ab.",
                    "mid": "Überprüfen Sie, ob der ermittelte Schulungsbedarf regelmäßig (z.B. jährlich) aktualisiert wird und ob er tatsächlich mit den Anforderungen des Standard-Testprozessmodells abgeglichen wird, um Kompetenzlücken gezielt zu schließen.",
                },
                "new": True,
            },
        ],
    },
    {
        "id": "lebenszyklus",
        "title": "Testlebenszyklus und Integration",
        "parent": "Stufe 3 - Defined",
        "description": (
            "Ein hoher Grad der Beteiligung des Testteams im Projekt- und "
            "Entwicklungsprozess sowie eine an die Entwicklungsmethodik "
            "angepasste, einheitliche Testmethodik sorgen dafür, dass "
            "Testaktivitäten fern vom kritischen Pfad stattfinden."
        ),
        "questions": [
            {
                "id": "lc-1",
                "text": "Testing wird bereits in frühen Phasen des Projekts/der Entwicklung einbezogen.",
                "hint": None,
                "recommendations": {
                    "low": "Binden Sie Testverantwortliche ab der ersten Projektphase ein – z.B. durch Teilnahme an Kick-offs, Anforderungsworkshops und Architekturentscheidungen. Frühzeitige Einbindung reduziert Nacharbeiten und ermöglicht proaktive Qualitätssicherung.",
                    "mid": "Überprüfen Sie, ob die frühe Einbindung des Testteams strukturell verankert ist (z.B. als fester Bestandteil des Projektprozesses) und nicht von der Initiative einzelner Personen abhängt.",
                },
            },
            {
                "id": "lc-2",
                "text": "Tester sind in Sprint-Planungen, Refinements und Reviews aktiv eingebunden.",
                "hint": None,
                "recommendations": {
                    "low": "Stellen Sie sicher, dass Tester als gleichwertige Teammitglieder in alle Sprint-Events eingeladen werden und aktiv an Refinements und Reviews teilnehmen. Das verbessert die Testfallqualität und führt zu realistischeren Aufwandsschätzungen.",
                    "mid": "Überprüfen Sie, ob Tester in den Agile Events tatsächlich aktiv beitragen (z.B. Akzeptanzkriterien mitgestalten, Aufwandsschätzungen für Testaktivitäten einbringen) und nicht nur als Zuhörer anwesend sind.",
                },
            },
            {
                "id": "lc-3",
                "text": "Testverantwortliche wirken bei der Definition von Akzeptanzkriterien mit.",
                "hint": None,
                "recommendations": {
                    "low": "Sorgen Sie dafür, dass Testverantwortliche bei der Definition von Akzeptanzkriterien (z.B. im Rahmen von User Stories) aktiv mitwirken, bevor diese festgelegt werden. Klare, testbare Akzeptanzkriterien reduzieren Interpretationsspielräume erheblich.",
                    "mid": "Überprüfen Sie die Qualität der vorhandenen Akzeptanzkriterien: Sind sie messbar, eindeutig und direkt als Testbasis nutzbar? Falls nicht, etablieren Sie ein gemeinsames Format (z.B. Given-When-Then) und schulen Sie das Team darin.",
                },
            },
            {
                "id": "lc-4",
                "text": "Es gibt eine definierte Verantwortlichkeit für Testaktivitäten über den gesamten Lebenszyklus (Shift-Left/Shift-Right).",
                "hint": None,
                "recommendations": {
                    "low": "Benennen Sie für jedes Projekt eine verantwortliche Person, die Testaktivitäten über den gesamten Lebenszyklus koordiniert und sicherstellt, dass keine Testphase vergessen wird – von der Anforderungsanalyse bis zum produktiven Betrieb.",
                    "mid": "Überprüfen Sie, ob die Verantwortlichkeiten für Shift-Left (frühe Qualitätssicherung) und Shift-Right (Monitoring im Betrieb) tatsächlich gelebt werden, und schärfen Sie die Rollenbeschreibungen entsprechend.",
                },
            },
            {
                "id": "lc-5",
                "text": "Entwickler sind aktiv in Testaktivitäten (z.B. Unit-/Komponententests, Reviews) eingebunden.",
                "hint": None,
                "recommendations": {
                    "low": "Führen Sie ein gemeinsames Verständnis dafür ein, dass Entwickler für Unit- und Komponententests verantwortlich sind, und machen Sie die Codeabdeckung durch Unit-Tests zu einem messbaren und kommunizierten Qualitätsziel.",
                    "mid": "Überprüfen Sie, ob Entwickler aktiv an Reviews von Testfällen und Akzeptanzkriterien teilnehmen, und stärken Sie die Zusammenarbeit zwischen Test und Entwicklung durch gemeinsame Formate wie Pair Testing.",
                },
            },
            {
                "id": "lc-6",
                "text": "Das Testteam wird frühzeitig in Anforderungs- und Architekturdiskussionen einbezogen und kennt die zuständigen Architekten und Entwickler.",
                "hint": "Gibt es Softwarearchitekten? Wenn ja, wer ist das? Sind die Entwickler bekannt?",
                "recommendations": {
                    "low": "Laden Sie Testverantwortliche systematisch zu Anforderungsreviews und Architektur-Workshops ein. Das Testteam kann potenzielle Testbarkeitsprobleme frühzeitig identifizieren und so kostspielige Nacharbeiten verhindern.",
                    "mid": "Überprüfen Sie, ob Testbarkeit als explizites Kriterium bei Architekturentscheidungen berücksichtigt wird, und stellen Sie sicher, dass das Testteam eine aktive Rolle bei der Bewertung von Anforderungen auf Vollständigkeit und Testbarkeit einnimmt.",
                },
            },
            {
                "id": "lc-7",
                "text": "Es gibt regelmäßige Abstimmungsformate zwischen Test und Business/Fachbereich.",
                "hint": None,
                "recommendations": {
                    "low": "Etablieren Sie ein regelmäßiges Abstimmungsformat zwischen Testteam und Fachbereich (z.B. monatlich 30 Minuten), in dem neue Anforderungen, Qualitätsziele und offene Fragen besprochen werden. Direkter Austausch verhindert Missverständnisse und Fehlinterpretationen.",
                    "mid": "Überprüfen Sie, ob die vorhandenen Abstimmungsformate effektiv sind und ob der Fachbereich tatsächlich als gleichwertiger Partner in Qualitätsentscheidungen eingebunden ist. Passen Sie Frequenz und Format bei Bedarf an.",
                },
            },
            {
                "id": "lc-8",
                "text": "Es gibt verschiedene definierte Testlevel/Teststufen, die im Projekt verfolgt werden (Unit-, Komponenten-, Integrations-, Regressionstests), deren Ziele dokumentiert sind und zur Teststrategie passen.",
                "hint": None,
                "recommendations": {
                    "low": "Definieren Sie schriftlich, welche Testlevel im Projekt verfolgt werden (mindestens Unit, Integration, System), beschreiben Sie für jedes Level Ziele, Verantwortlichkeiten und Abdeckungserwartungen, und verankern Sie sie im Testkonzept.",
                    "mid": "Überprüfen Sie, ob alle definierten Testlevel tatsächlich konsequent durchgeführt werden und ob die Ziele der einzelnen Level aufeinander abgestimmt sind, um Lücken und Redundanzen zu minimieren.",
                },
            },
            {
                "id": "lc-9",
                "text": "Eine einheitliche Testmethodik (z.B. nach ISTQB-Standard) wird angewendet und vom Projekt- und Testteam unterstützt.",
                "hint": None,
                "recommendations": {
                    "low": "Wählen Sie eine einheitliche Testmethodik (z.B. risikobasiertes Testen nach ISTQB oder testgetriebene Entwicklung im agilen Kontext), dokumentieren Sie sie und schulen Sie alle Testbeteiligten darin, damit eine konsistente Vorgehensweise gewährleistet ist.",
                    "mid": "Überprüfen Sie, ob die vorhandene Testmethodik von allen Beteiligten verstanden und konsistent angewendet wird, und identifizieren Sie Bereiche, in denen Abweichungen zu Qualitätslücken führen.",
                },
            },
            {
                "id": "lc-10",
                "text": "Testtechniken (z.B. Äquivalenzklassenbildung, Grenzwertanalyse, Entscheidungstabellen) werden systematisch eingesetzt, ggf. unterstützt durch Checklisten oder formale Designtechniken.",
                "hint": None,
                "recommendations": {
                    "low": "Führen Sie eine strukturierte Einführung in grundlegende Testtechniken (Äquivalenzklassenbildung, Grenzwertanalyse, Entscheidungstabellen) durch und stellen Sie Checklisten zur Verfügung, die Tester bei der systematischen Anwendung unterstützen.",
                    "mid": "Überprüfen Sie, ob Testtechniken tatsächlich systematisch und nicht nur intuitiv angewendet werden, und erwägen Sie die Einführung von Designreviews, bei denen Testfälle auf methodisch korrekte Anwendung der Techniken geprüft werden.",
                },
            },
            {
                "id": "lc-11",
                "text": "Das Vorgehen ist an die jeweilige Entwicklungsmethodik (Wasserfall, Agile, SAFe) angepasst und schriftlich festgehalten.",
                "hint": None,
                "recommendations": {
                    "low": "Dokumentieren Sie, wie der Testprozess an die verwendete Entwicklungsmethodik (z.B. Scrum, Kanban, Wasserfall) angepasst ist – insbesondere hinsichtlich Testplanung, Testdurchführung und Reporting im Kontext der Entwicklungszyklen.",
                    "mid": "Überprüfen Sie, ob die dokumentierte Anpassung tatsächlich gelebt wird, und aktualisieren Sie die Beschreibung bei Änderungen der Entwicklungsmethodik oder bei erkannten Inkongruenzen zwischen definiertem und praktiziertem Vorgehen.",
                },
            },
            {
                "id": "lc-12",
                "text": "Es gibt definierte Vorgehensweisen für explorative Tests.",
                "hint": None,
                "recommendations": {
                    "low": "Definieren Sie einen strukturierten Ansatz für explorative Tests (z.B. Session-Based Testing mit Charters), der festlegt, wann explorative Tests sinnvoll sind, wie sie dokumentiert werden und wie die Ergebnisse in den Testbericht einfließen.",
                    "mid": "Überprüfen Sie, ob explorative Tests systematisch durchgeführt und dokumentiert werden, und stellen Sie sicher, dass Erkenntnisse aus explorativen Tests in die Testfallbibliothek und den Fehlermanagement-Prozess einfließen.",
                },
            },
            {
                "id": "lc-13",
                "text": "Testtechniken werden je nach Risiko und Testobjekt bewusst ausgewählt.",
                "hint": None,
                "recommendations": {
                    "low": "Führen Sie bei der Testfallplanung eine bewusste Auswahl der Testtechnik durch und dokumentieren Sie die Entscheidung (z.B. 'Für dieses Modul wurde Äquivalenzklassenbildung gewählt, weil...'). Das schärft das methodische Bewusstsein und die Ergebnisnachvollziehbarkeit.",
                    "mid": "Etablieren Sie eine Designphase in der Testfallentwicklung, in der die Wahl der Testtechniken explizit begründet und in einem Review auf Angemessenheit geprüft wird. Nutzen Sie Risikoanalysen als Ausgangspunkt für die Technikselektion.",
                },
            },
            {
                "id": "lc-14",
                "text": "Es existiert ein definiertes Vorgehen für Regressionstests.",
                "hint": None,
                "recommendations": {
                    "low": "Definieren Sie schriftlich, wann Regressionstests durchgeführt werden (z.B. bei jedem Release oder nach bestimmten Änderungstypen), welcher Testumfang mindestens erforderlich ist und wer für die Durchführung verantwortlich ist.",
                    "mid": "Überprüfen Sie, ob das Regressionstestverfahren in der Praxis konsequent angewendet wird, und analysieren Sie, ob der Umfang der Regressionstests risikobasiert optimiert werden kann – insbesondere durch Testautomatisierung.",
                },
            },
            {
                "id": "lc-15",
                "text": "Es gibt eine einheitliche Terminologie/ein Glossar, das von allen Beteiligten verwendet wird.",
                "hint": None,
                "recommendations": {
                    "low": "Erstellen Sie ein zentrales, für alle zugängliches Testglossar mit den wesentlichen Begriffen (z.B. Testfall, Testebene, Defect, Entry-/Exit-Kriterien) und verpflichten Sie alle Beteiligten zur konsistenten Nutzung. Begriffliche Unklarheiten sind eine häufige Ursache für Missverständnisse.",
                    "mid": "Überprüfen Sie das bestehende Glossar auf Vollständigkeit und Aktualität, stellen Sie sicher, dass neue Projektmitglieder darauf hingewiesen werden, und ergänzen Sie projekt- oder domänenspezifische Begriffe systematisch.",
                },
            },
            {
                "id": "lc-16",
                "text": "Testaktivitäten sind an definierten Meilensteinen des Entwicklungsprozesses verankert (z.B. Definition of Ready/Done).",
                "hint": None,
                "recommendations": {
                    "low": "Verankern Sie Testaktivitäten explizit in den Meilensteinen des Entwicklungsprozesses (z.B. Definition of Ready, Sprint Review, Release Gate) und definieren Sie, welche Testnachweise zu jedem Meilenstein vorliegen müssen.",
                    "mid": "Überprüfen Sie, ob die verankerten Testaktivitäten an Meilensteinen tatsächlich eingehalten werden, und stellen Sie sicher, dass Meilensteine nicht ohne vollständige Testabnahme passiert werden können.",
                },
                "new": True,
            },
        ],
    },
    {
        "id": "nichtfunktional",
        "title": "Nicht-funktionales Testen",
        "parent": "Stufe 3 - Defined",
        "description": (
            "Nicht-funktionale Anforderungen werden systematisch identifiziert, "
            "priorisiert und mit eigenen Strategien, Methoden und "
            "Akzeptanzkriterien getestet."
        ),
        "questions": [
            {
                "id": "nf-1",
                "text": "Nicht-funktionale Anforderungen (Performance, Security, Usability, Skalierbarkeit etc.) werden systematisch identifiziert und priorisiert.",
                "hint": None,
                "recommendations": {
                    "low": "Führen Sie zu Projektbeginn eine strukturierte Erhebung nicht-funktionaler Anforderungen durch – z.B. anhand einer Checkliste, die Qualitätsmerkmale wie Performance, Security, Usability, Skalierbarkeit und Verfügbarkeit abdeckt. Ohne explizite Identifikation werden nicht-funktionale Anforderungen regelmäßig vergessen.",
                    "mid": "Überprüfen Sie, ob die identifizierten nicht-funktionalen Anforderungen vollständig und für den Kontext des Produkts angemessen priorisiert sind, und stellen Sie sicher, dass sie als gleichwertige Anforderungen in die Testplanung einfließen.",
                },
                "new": True,
            },
            {
                "id": "nf-2",
                "text": "Für nicht-funktionale Testarten existieren spezifische Teststrategien, Methoden und Werkzeuge.",
                "hint": None,
                "recommendations": {
                    "low": "Definieren Sie für die relevantesten nicht-funktionalen Testarten (z.B. Last- und Performance-Tests, Security-Tests) je eine spezifische Strategie mit Zielen, Methoden, Werkzeugen und Verantwortlichkeiten – zunächst auch nur für die kritischsten Bereiche.",
                    "mid": "Überprüfen Sie, ob die vorhandenen Strategien für nicht-funktionale Tests vollständig, aktuell und mit geeigneten Werkzeugen unterstützt sind, und stellen Sie sicher, dass Verantwortlichkeiten klar geregelt sind.",
                },
                "new": True,
            },
            {
                "id": "nf-3",
                "text": "Es gibt definierte Akzeptanzkriterien (z.B. Schwellenwerte) für nicht-funktionale Eigenschaften.",
                "hint": None,
                "recommendations": {
                    "low": "Definieren Sie für die relevantesten nicht-funktionalen Anforderungen messbare Akzeptanzkriterien mit konkreten Schwellenwerten (z.B. 'Seitenaufbauzeit < 2 Sekunden unter Last von 1.000 gleichzeitigen Nutzern') und dokumentieren Sie diese verbindlich.",
                    "mid": "Überprüfen Sie, ob alle nicht-funktionalen Akzeptanzkriterien tatsächlich messbar und realistisch sind, und stellen Sie sicher, dass sie vor dem Release geprüft werden und als Freigabekriterium gelten.",
                },
                "new": True,
            },
            {
                "id": "nf-4",
                "text": "Nicht-funktionale Tests sind in den Testplanungs- und Reporting-Prozess integriert.",
                "hint": None,
                "recommendations": {
                    "low": "Integrieren Sie nicht-funktionale Tests als eigene Positionen in Testpläne und Statusberichte. Sie sollten denselben Planungs-, Reporting- und Freigabeprozess durchlaufen wie funktionale Tests, um sicherzustellen, dass sie nicht ad hoc oder zu spät durchgeführt werden.",
                    "mid": "Überprüfen Sie, ob nicht-funktionale Testergebnisse tatsächlich regelmäßig berichtet und in Freigabeentscheidungen berücksichtigt werden, und stellen Sie sicher, dass Planung und Reporting für alle Testarten konsistent sind.",
                },
                "new": True,
            },
        ],
    },
    {
        "id": "peer_reviews",
        "title": "Peer Reviews",
        "parent": "Stufe 3 - Defined",
        "description": (
            "Definierte, dokumentierte Review-Verfahren mit Checklisten "
            "tragen zur frühen Fehlervermeidung bei und sorgen für "
            "wiederverwendbare, wartbare Testfälle."
        ),
        "questions": [
            {
                "id": "pr-1",
                "text": "Reviews von Testfällen werden durchgeführt (z.B. Peer-Review).",
                "hint": None,
                "recommendations": {
                    "low": "Etablieren Sie einen einfachen Peer-Review-Prozess für neu erstellte Testfälle: Jeder Testfall wird von mindestens einer weiteren Person auf Richtigkeit, Vollständigkeit und Verständlichkeit geprüft, bevor er in Ausführung geht.",
                    "mid": "Strukturieren Sie den Review-Prozess durch eine Checkliste mit prüfbaren Qualitätskriterien und stellen Sie sicher, dass Reviewergebnisse dokumentiert und Review-Erkenntnisse systematisch für die Verbesserung der Testfallqualität genutzt werden.",
                },
            },
            {
                "id": "pr-2",
                "text": "Bei der Testfallerstellung werden Wiederverwendbarkeit und Wartbarkeit berücksichtigt.",
                "hint": None,
                "recommendations": {
                    "low": "Schulen Sie Tester in Prinzipien der wartbaren Testfallgestaltung (z.B. Modularisierung, keine hartkodierten Testdaten, klare Benennung) und führen Sie eine entsprechende Vorlage ein, die diese Aspekte strukturell fördert.",
                    "mid": "Überprüfen Sie den Testfallbestand stichprobenartig auf Wiederverwendbarkeit und Wartbarkeit, identifizieren Sie Testfälle mit hohem Wartungsaufwand, und entwickeln Sie Maßnahmen zur Modernisierung und Modularisierung der Testbibliothek.",
                },
            },
            {
                "id": "pr-3",
                "text": "Es existiert ein definiertes, dokumentiertes Verfahren für Peer Reviews (z.B. von Anforderungen, Architektur, Code, Testbasis).",
                "hint": None,
                "recommendations": {
                    "low": "Erstellen Sie ein dokumentiertes Review-Verfahren, das beschreibt, was wie und von wem reviewt wird, welche Kriterien anzuwenden sind und wie Ergebnisse dokumentiert werden. Ein klares Verfahren macht Reviews effizienter und konsistenter.",
                    "mid": "Überprüfen Sie, ob das vorhandene Review-Verfahren für alle relevanten Artefakte (Anforderungen, Testfälle, Code) vollständig beschrieben ist, und evaluieren Sie dessen Wirksamkeit anhand der gefundenen Fehler und der Bearbeitungsdauer.",
                },
                "new": True,
            },
            {
                "id": "pr-4",
                "text": "Für Reviews werden Checklisten oder Leitfäden genutzt, um Konsistenz sicherzustellen.",
                "hint": None,
                "recommendations": {
                    "low": "Erstellen Sie einfache Review-Checklisten für die wichtigsten Review-Objekte (z.B. Testfälle, User Stories), die die häufigsten Fehlerquellen und Qualitätskriterien abdecken, und stellen Sie sie dem Team als Hilfsmittel zur Verfügung.",
                    "mid": "Überprüfen Sie die vorhandenen Checklisten auf Vollständigkeit und Aktualität, und ergänzen Sie sie regelmäßig um neue Erkenntnisse aus zurückliegenden Reviews und Projekterfahrungen.",
                },
                "new": True,
            },
            {
                "id": "pr-5",
                "text": "Ergebnisse aus Reviews werden erfasst, nachverfolgt und in Metriken berücksichtigt.",
                "hint": None,
                "recommendations": {
                    "low": "Führen Sie eine einfache Erfassung von Review-Ergebnissen ein (z.B. Anzahl gefundener Fehler, Bearbeitungszeit), und stellen Sie sicher, dass identifizierte Mängel nachverfolgt und korrigiert werden, bevor das Artefakt freigegeben wird.",
                    "mid": "Integrieren Sie Review-Metriken in das reguläre Testberichtswesen und nutzen Sie die Daten, um die Wirksamkeit von Reviews zu bewerten und den Review-Prozess gezielt zu verbessern.",
                },
                "new": True,
            },
        ],
    },

    # =========================================================================
    # STUFE 4: MEASURED (GEMESSEN)
    # =========================================================================
    {
        "id": "testmetriken",
        "title": "Testmetriken",
        "parent": "Stufe 4 - Measured",
        "description": (
            "Durch organisationsweit definierte, zentral verwaltete Metriken "
            "ist eine objektive Messung von Fortschritt, Fehlern und Prozess "
            "sowie eine darauf basierende Entscheidungsfindung möglich."
        ),
        "questions": [
            {
                "id": "tme-1",
                "text": "Testmetriken werden systematisch erhoben (z.B. Testabdeckung, Defect Density, Durchlaufzeiten).",
                "hint": None,
                "recommendations": {
                    "low": "Definieren Sie eine erste Auswahl relevanter Testmetriken (z.B. Testabdeckung, Defect Density, Testfortschritt) und stellen Sie sicher, dass diese Kennzahlen in jedem Projekt regelmäßig erhoben und dokumentiert werden.",
                    "mid": "Überprüfen Sie, ob die erhobenen Metriken vollständig, korrekt und konsistent erhoben werden, und stellen Sie sicher, dass die Datenerhebung systematisch und nicht nur gelegentlich erfolgt.",
                },
            },
            {
                "id": "tme-2",
                "text": "Metriken werden genutzt, um Entscheidungen zu treffen (z.B. Release-Freigabe).",
                "hint": None,
                "recommendations": {
                    "low": "Stellen Sie sicher, dass Testergebnisse und -metriken aktiv in Entscheidungen einbezogen werden – z.B. durch explizite Aufnahme in Meeting-Agenden oder durch definierte Freigabekriterien auf Basis von Metrikwerten.",
                    "mid": "Überprüfen Sie, ob Metriken tatsächlich entscheidungsleitend sind oder nur zur Dokumentation dienen, und stärken Sie ihre Wirksamkeit durch verbindliche Schwellenwerte, die vor einem Release erfüllt sein müssen.",
                },
            },
            {
                "id": "tme-3",
                "text": "Es gibt definierte Zielwerte/Benchmarks für relevante Metriken.",
                "hint": None,
                "recommendations": {
                    "low": "Definieren Sie für jede erhobene Metrik einen realistischen Zielwert (z.B. Testabdeckung ≥ 80 %, kritische Defects bei Release = 0) und kommunizieren Sie diese Ziele an alle Stakeholder als verbindliche Qualitätserwartungen.",
                    "mid": "Überprüfen Sie, ob die vorhandenen Zielwerte auf Basis von Projekterfahrungen kalibriert und regelmäßig angepasst werden, und stellen Sie sicher, dass sie ambitioniert genug sind, um echte Qualitätssteigerungen zu bewirken.",
                },
            },
            {
                "id": "tme-4",
                "text": "Metriken werden regelmäßig analysiert, um Prozessverbesserungen abzuleiten.",
                "hint": None,
                "recommendations": {
                    "low": "Führen Sie nach jeder Testphase eine kurze Metrikanalyse durch und leiten Sie mindestens eine konkrete Maßnahme zur Prozessverbesserung ab. Ohne systematische Analyse bleiben Metriken nur Zahlen ohne Wirkung.",
                    "mid": "Strukturieren Sie die Metrikanalyse als festen Bestandteil von Retrospektiven oder Projektabschlüssen und stellen Sie sicher, dass abgeleitete Maßnahmen dokumentiert, umgesetzt und auf Wirksamkeit geprüft werden.",
                },
            },
            {
                "id": "tme-5",
                "text": "Es wird zwischen Prozess-, Produkt- und Projektmetriken unterschieden.",
                "hint": None,
                "recommendations": {
                    "low": "Kategorisieren Sie Ihre vorhandenen Metriken systematisch in Prozess- (z.B. Testdurchlaufzeit), Produkt- (z.B. Defect Density) und Projektmetriken (z.B. Aufwandsabweichung) und stellen Sie sicher, dass alle drei Kategorien abgedeckt sind.",
                    "mid": "Überprüfen Sie, ob die Unterscheidung zwischen den Metrik-Kategorien konsequent in Berichten und Analysen angewendet wird, und stellen Sie sicher, dass jede Kategorie die richtigen Empfänger und Entscheidungen unterstützt.",
                },
            },
            {
                "id": "tme-6",
                "text": "Die erhobenen Metriken sind für alle Stakeholder nachvollziehbar und konsistent definiert.",
                "hint": None,
                "recommendations": {
                    "low": "Erstellen Sie für jede Metrik eine eindeutige Definition (Bezeichnung, Berechnungsformel, Datenquelle, Erhebungsfrequenz) und stellen Sie diese für alle Stakeholder zugänglich zur Verfügung. Unklare Definitionen führen zu Missverständnissen und inkonsistenten Interpretationen.",
                    "mid": "Überprüfen Sie, ob alle Metriken tatsächlich einheitlich verstanden und interpretiert werden, z.B. durch kurze Interviews mit verschiedenen Stakeholdern, und klären Sie Inkonsistenzen durch aktualisierte Definitionen und Schulungen.",
                },
            },
            {
                "id": "tme-7",
                "text": "Trends (z.B. Defect-Trends, Fortschrittstrends) werden über Zeit dargestellt und ausgewertet.",
                "hint": None,
                "recommendations": {
                    "low": "Stellen Sie Metrikwerte über mehrere Zeitpunkte visuell dar (z.B. Liniendiagramme für Defect-Trends oder Testfortschritt) und interpretieren Sie die Trends in Statusberichten explizit. Trends liefern mehr Information als Einzelwerte.",
                    "mid": "Überprüfen Sie, ob Trend-Analysen systematisch für alle relevanten Metriken durchgeführt werden, und nutzen Sie Trends proaktiv, um Qualitätsrisiken frühzeitig zu erkennen und Gegenmaßnahmen einzuleiten.",
                },
            },
            {
                "id": "tme-8",
                "text": "Der Reifegrad der Testautomatisierung wird regelmäßig bewertet (z.B. Automatisierungsgrad, Wartungsaufwand).",
                "hint": None,
                "recommendations": {
                    "low": "Führen Sie eine erste Bestandsaufnahme der Testautomatisierung durch (Automatisierungsgrad, abgedeckte Testebenen, Wartungsaufwand) und definieren Sie Zielwerte für die nächsten 12 Monate. Ein bewusster Ausgangspunkt ist die Grundlage für gezielte Verbesserungen.",
                    "mid": "Überprüfen Sie den Automatisierungsgrad regelmäßig (z.B. quartalsweise) anhand definierter Kriterien und nutzen Sie die Ergebnisse, um gezielte Investitionen in Testautomatisierung zu priorisieren und den ROI zu bewerten.",
                },
            },
            {
                "id": "tme-9",
                "text": "Die benötigten Daten werden synchron ermittelt, zentral gespeichert und es gibt Prüfungen zur Validierung der genutzten Daten (Stichproben).",
                "hint": "Werden die zugrundeliegenden Daten zentral gespeichert und stichprobenartig auf Validität geprüft?",
                "recommendations": {
                    "low": "Stellen Sie sicher, dass Metrikdaten zentral und konsistent gespeichert werden (z.B. in einem gemeinsamen Dashboard oder Repository) und nicht dezentral in einzelnen Dateien. Verteilte Datenhaltung führt zu Inkonsistenzen und erhöhtem Aufwand.",
                    "mid": "Implementieren Sie stichprobenartige Validierungen der Metrikdaten, um Fehler in der Datenerhebung frühzeitig zu erkennen, und stellen Sie sicher, dass Aktualisierungen synchron und zeitnah erfolgen.",
                },
            },
            {
                "id": "tme-10",
                "text": "Mindestens 7 der folgenden Metriken werden genutzt: Testüberdeckungsverhältnis, Anzahl Testfälle geplant/bereits erstellt, Testfortschritt (Ist/Plan), Testdurchführungsverhältnis, Fehlerschwere, Anzahl Produktionsfehler, verbrauchter Budgetanteil, Testphasen/verbrauchte Stunden, Leerlaufrate, Testendekriterien.",
                "hint": "Welche Metriken werden genutzt?",
                "recommendations": {
                    "low": "Erweitern Sie Ihr Metrikset auf mindestens 7 Kennzahlen, die verschiedene Aspekte des Testprozesses abdecken (z.B. Testabdeckung, Defect-Rate, Testfortschritt, Aufwandseffizienz). Stellen Sie sicher, dass jede Metrik einen klaren Nutzen für Entscheidungen hat.",
                    "mid": "Überprüfen Sie, ob alle eingesetzten Metriken tatsächlich regelmäßig erhoben und genutzt werden, und eliminieren Sie Metriken ohne Entscheidungsrelevanz. Stellen Sie sicher, dass das Metrikset aktuelle Best Practices widerspiegelt.",
                },
            },
            {
                "id": "tme-11",
                "text": "Ein organisationsweites Metrikprogramm definiert verbindliche Kennzahlen, die projektübergreifend vergleichbar sind.",
                "hint": None,
                "recommendations": {
                    "low": "Definieren Sie einen organisationsweiten Mindeststandard für Testmetriken, der projektübergreifend verbindlich gilt und eine vergleichende Auswertung über Projekte hinweg ermöglicht. Selbst ein kleines Set von 3–5 Pflichtmetriken ist ein wirksamer erster Schritt.",
                    "mid": "Überprüfen Sie, ob das Metrikprogramm in allen Projekten angewendet wird und ob die Daten tatsächlich projektübergreifend vergleichbar und konsistent erhoben werden. Identifizieren Sie Abweichungen und setzen Sie Korrekturmaßnahmen durch.",
                },
                "new": True,
            },
        ],
    },
    {
        "id": "produktqualitaet",
        "title": "Produktqualitätsbewertung",
        "parent": "Stufe 4 - Measured",
        "description": (
            "Quantitativ definierte Qualitätsmodelle und -ziele ermöglichen "
            "eine messbare Bewertung der Produktqualität sowie eine "
            "systematische Auswertung von Fehlerursachen und -mustern."
        ),
        "questions": [
            {
                "id": "pq-1",
                "text": "Es existieren definierte Qualitätsmodelle bzw. Qualitätsmerkmale (z.B. nach ISO/IEC 25010), anhand derer die Produktqualität bewertet wird.",
                "hint": None,
                "recommendations": {
                    "low": "Führen Sie ein definiertes Qualitätsmodell ein (z.B. ISO/IEC 25010) als Referenzrahmen für die Bewertung von Produktqualität. Wählen Sie die für Ihr Produkt relevantesten Qualitätsmerkmale aus und machen Sie sie zur Grundlage für Qualitätsziele und Testplanung.",
                    "mid": "Überprüfen Sie, ob das vorhandene Qualitätsmodell vollständig auf das Produkt angewendet wird, und stellen Sie sicher, dass alle relevanten Qualitätsmerkmale explizit bewertet und in Statusberichten kommuniziert werden.",
                },
                "new": True,
            },
            {
                "id": "pq-2",
                "text": "Qualitätsziele für das Produkt werden quantitativ definiert und im Projektverlauf gemessen.",
                "hint": None,
                "recommendations": {
                    "low": "Formulieren Sie Qualitätsziele für das Produkt in messbaren Größen (z.B. 'Fehlerrate im Produktivbetrieb < 0,1 % pro Release', 'Verfügbarkeit ≥ 99,5 %') und verfolgen Sie die Zielerreichung regelmäßig im Projektverlauf.",
                    "mid": "Überprüfen Sie, ob die quantitativen Qualitätsziele realistisch, messbar und für alle Stakeholder verbindlich sind, und stellen Sie sicher, dass Zielabweichungen frühzeitig erkannt und kommuniziert werden.",
                },
                "new": True,
            },
            {
                "id": "pq-3",
                "text": "Die tatsächliche Produktqualität wird mit den definierten Qualitätszielen verglichen und Abweichungen werden bewertet.",
                "hint": None,
                "recommendations": {
                    "low": "Führen Sie regelmäßige Soll-Ist-Vergleiche zwischen den definierten Qualitätszielen und den tatsächlich gemessenen Qualitätswerten durch und dokumentieren Sie die Ergebnisse. Das schafft Transparenz über den tatsächlichen Qualitätsstand des Produkts.",
                    "mid": "Strukturieren Sie den Soll-Ist-Vergleich als festen Bestandteil des Release-Prozesses und stellen Sie sicher, dass Abweichungen nicht nur dokumentiert, sondern auch systematisch analysiert und mit konkreten Korrekturmaßnahmen hinterlegt werden.",
                },
                "new": True,
            },
            {
                "id": "pq-4",
                "text": "Defect-Daten werden ausgewertet, um Muster (z.B. fehleranfällige Module) zu identifizieren.",
                "hint": None,
                "recommendations": {
                    "low": "Analysieren Sie regelmäßig die vorhandenen Defect-Daten auf wiederkehrende Muster (z.B. häufig fehleranfällige Module, bestimmte Fehlertypen oder -ursachen) und nutzen Sie diese Erkenntnisse zur gezielten Schärfung der Testfallplanung.",
                    "mid": "Formalisieren Sie die Defect-Analyse als periodischen Prozessschritt (z.B. nach jedem Release) und stellen Sie sicher, dass Erkenntnisse zu fehleranfälligen Bereichen in die Risikoanalyse und Testpriorisierung einfließen.",
                },
            },
            {
                "id": "pq-5",
                "text": "Root-Cause-Analysen werden bei kritischen Defects durchgeführt.",
                "hint": None,
                "recommendations": {
                    "low": "Definieren Sie, ab welchem Schweregrad (z.B. Critical oder High) ein Defect eine Root-Cause-Analyse auslöst, und führen Sie diese systematisch durch – auch wenn es zunächst nur eine kurze strukturierte Analyse (z.B. 5-Whys) ist.",
                    "mid": "Stellen Sie sicher, dass Root-Cause-Analysen tatsächlich durchgeführt und die Ergebnisse dokumentiert werden, und leiten Sie aus den identifizierten Ursachen präventive Maßnahmen ab, deren Umsetzung nachverfolgt wird.",
                },
            },
        ],
    },
    {
        "id": "erweiterte_reviews",
        "title": "Erweiterte Reviews",
        "parent": "Stufe 4 - Measured",
        "description": (
            "Quantitative Review-Daten ermöglichen es, die Wirksamkeit von "
            "Reviews im Vergleich zu dynamischen Tests zu bewerten und den "
            "Review-Prozess gezielt zu verbessern."
        ),
        "questions": [
            {
                "id": "er-1",
                "text": "Für Reviews (Anforderungen, Design, Code) werden quantitative Daten (z.B. Fehlerdichte pro Review, Reviewdauer) erhoben.",
                "hint": None,
                "recommendations": {
                    "low": "Beginnen Sie damit, grundlegende Kennzahlen für Reviews zu erheben: Anzahl gefundener Defects pro Review-Session, Reviewdauer und Art der gefundenen Mängel. Selbst einfache Daten ermöglichen erste Aussagen zur Wirksamkeit von Reviews.",
                    "mid": "Erweitern Sie die erhobenen Review-Daten um weiterführende Kennzahlen (z.B. Fehlerdichte je Seitenzahl, Verhältnis von Major zu Minor Defects) und stellen Sie sicher, dass die Daten systematisch erfasst und auswertbar sind.",
                },
                "new": True,
            },
            {
                "id": "er-2",
                "text": "Review-Daten werden genutzt, um die Wirksamkeit von Reviews im Vergleich zu dynamischen Tests zu bewerten.",
                "hint": None,
                "recommendations": {
                    "low": "Vergleichen Sie die in Reviews gefundenen Defects mit den durch dynamische Tests gefundenen, um einzuschätzen, welcher Ansatz für welche Artefakttypen effektiver ist. Diese Analyse ist die Grundlage für eine optimierte Ressourcenallokation.",
                    "mid": "Führen Sie eine strukturierte Wirksamkeitsanalyse der Reviews im Vergleich zu dynamischen Tests durch und nutzen Sie die Ergebnisse, um den Ressourceneinsatz für Reviews und Tests gezielt zu steuern.",
                },
                "new": True,
            },
            {
                "id": "er-3",
                "text": "Auf Basis von Review-Metriken werden gezielte Verbesserungen am Review-Prozess vorgenommen.",
                "hint": None,
                "recommendations": {
                    "low": "Leiten Sie aus den erhobenen Review-Metriken mindestens eine konkrete Verbesserungsmaßnahme je Quartal ab (z.B. Überarbeitung einer Checkliste, Anpassung des Review-Zeitrahmens, gezielte Schulung) und verfolgen Sie deren Umsetzung.",
                    "mid": "Etablieren Sie einen formalen Zyklus aus Review-Metrik-Analyse und Prozessverbesserung, in dem Maßnahmen priorisiert, umgesetzt und auf ihre Wirksamkeit hin evaluiert werden, bevor neue Verbesserungsrunden starten.",
                },
                "new": True,
            },
        ],
    },

    # =========================================================================
    # STUFE 5: OPTIMIZATION (OPTIMIERUNG)
    # =========================================================================
    {
        "id": "fehlervermeidung",
        "title": "Fehlervermeidung",
        "parent": "Stufe 5 - Optimization",
        "description": (
            "Systematische, organisationsweite Ursachenanalysen und ein "
            "definierter Prozess zur Ableitung präventiver Maßnahmen "
            "verhindern das wiederholte Auftreten von Fehlerursachen."
        ),
        "questions": [
            {
                "id": "fv-1",
                "text": "Root-Cause-Analysen werden nicht nur fallweise, sondern systematisch und organisationsweit für wiederkehrende Fehlerursachen durchgeführt.",
                "hint": None,
                "recommendations": {
                    "low": "Definieren Sie, wann und wie organisationsweite Root-Cause-Analysen für wiederkehrende Fehlerursachen durchgeführt werden, und etablieren Sie einen einfachen, strukturierten Prozess (z.B. Ishikawa-Diagramm, 5-Whys) mit benannten Verantwortlichkeiten.",
                    "mid": "Überprüfen Sie, ob Root-Cause-Analysen tatsächlich systematisch – und nicht nur fallweise nach besonders schweren Vorfällen – durchgeführt werden, und stellen Sie sicher, dass die Ergebnisse organisationsweit zugänglich gemacht werden.",
                },
                "new": True,
            },
            {
                "id": "fv-2",
                "text": "Es existiert ein definierter Prozess, um aus Fehlerursachen präventive Maßnahmen abzuleiten und deren Wirksamkeit zu verfolgen.",
                "hint": None,
                "recommendations": {
                    "low": "Definieren Sie einen expliziten Prozessschritt nach jeder Root-Cause-Analyse, bei dem präventive Maßnahmen abgeleitet, Verantwortliche benannt, Umsetzungsfristen festgelegt und die Wirksamkeit nach der Umsetzung bewertet werden.",
                    "mid": "Überprüfen Sie, ob der bestehende Prozess zur Maßnahmenableitung konsequent angewendet wird, und stellen Sie sicher, dass die Wirksamkeit jeder Maßnahme explizit evaluiert und die Ergebnisse für künftige Analysen genutzt werden.",
                },
                "new": True,
            },
            {
                "id": "fv-3",
                "text": "Lessons Learned aus abgeschlossenen Projekten werden systematisch in den Testprozess eingearbeitet.",
                "hint": None,
                "recommendations": {
                    "low": "Führen Sie am Ende jedes Projekts eine strukturierte Lessons-Learned-Session durch und dokumentieren Sie die wichtigsten Erkenntnisse. Stellen Sie sicher, dass mindestens eine Maßnahme pro Projekt konkret im Testprozess oder in Schulungsunterlagen umgesetzt wird.",
                    "mid": "Formalisieren Sie den Transfer von Lessons Learned in den Testprozess: Definieren Sie, wer für die Einarbeitung in Standards und Vorlagen verantwortlich ist, und überprüfen Sie bei künftigen Projekten, ob frühere Erkenntnisse berücksichtigt wurden.",
                },
            },
            {
                "id": "fv-4",
                "text": "Erkenntnisse zur Fehlervermeidung werden organisationsweit kommuniziert und in Schulungen/Standards integriert.",
                "hint": None,
                "recommendations": {
                    "low": "Etablieren Sie einen regelmäßigen Kommunikationskanal (z.B. interner Newsletter, Wiki-Seite oder monatliche Kurzsession), über den Erkenntnisse zur Fehlervermeidung und Best Practices mit allen Testteams geteilt werden.",
                    "mid": "Stellen Sie sicher, dass Erkenntnisse zur Fehlervermeidung nicht nur kommuniziert, sondern auch systematisch in Schulungsunterlagen und Standards integriert werden, und überprüfen Sie, ob neues Wissen tatsächlich in der täglichen Arbeit ankommt.",
                },
                "new": True,
            },
        ],
    },
    {
        "id": "qualitaetskontrolle",
        "title": "Qualitätskontrolle",
        "parent": "Stufe 5 - Optimization",
        "description": (
            "Statistische Methoden werden eingesetzt, um die Stabilität und "
            "Vorhersagbarkeit von Testprozessen zu überwachen und "
            "Prognosen auf Basis historischer Daten abzuleiten."
        ),
        "questions": [
            {
                "id": "qk-1",
                "text": "Statistische Methoden werden eingesetzt, um die Stabilität und Vorhersagbarkeit von Testprozessen zu überwachen (z.B. Kontrollkarten, Streubreiten).",
                "hint": None,
                "recommendations": {
                    "low": "Führen Sie einfache statistische Grundmethoden ein (z.B. Kontrollkarten für Defect-Trends oder Testdurchlaufzeiten), um Ausreißer und Instabilitäten im Testprozess sichtbar zu machen. Statistische Kontrolle beginnt mit der konsequenten Visualisierung von Prozessdaten über Zeit.",
                    "mid": "Erweitern Sie den Einsatz statistischer Methoden auf weitere Prozessindikatoren und stellen Sie sicher, dass die Ergebnisse von ausreichend Personen interpretiert und in Entscheidungen einbezogen werden können.",
                },
                "new": True,
            },
            {
                "id": "qk-2",
                "text": "Abweichungen vom erwarteten (statistisch normalen) Prozessverhalten werden erkannt und Ursachen gezielt untersucht.",
                "hint": None,
                "recommendations": {
                    "low": "Definieren Sie für relevante Prozessmetriken statistische Kontrollgrenzen und legen Sie fest, wer bei Überschreitung dieser Grenzen informiert wird und welche Schritte zur Ursachenuntersuchung einzuleiten sind.",
                    "mid": "Überprüfen Sie, ob erkannte Abweichungen tatsächlich systematisch untersucht werden und ob die Erkenntnisse in Prozessverbesserungen einfließen. Stellen Sie sicher, dass der Untersuchungsprozess klar definiert und zeitnah umgesetzt wird.",
                },
                "new": True,
            },
            {
                "id": "qk-3",
                "text": "Prognosen zu Qualität und Aufwand basieren auf historischen, statistisch abgesicherten Daten.",
                "hint": None,
                "recommendations": {
                    "low": "Beginnen Sie damit, historische Projektdaten (z.B. Aufwände, Defect-Raten, Testdurchlaufzeiten) systematisch zu erfassen und auszuwerten, um Prognosen für künftige Projekte auf einer soliden Datenbasis zu fundieren.",
                    "mid": "Überprüfen Sie, ob vorhandene Prognosemodelle regelmäßig mit tatsächlichen Ergebnissen abgeglichen und kalibriert werden, und stellen Sie sicher, dass die verwendeten historischen Daten repräsentativ und qualitativ hochwertig sind.",
                },
                "new": True,
            },
        ],
    },
    {
        "id": "prozessoptimierung",
        "title": "Testprozessoptimierung",
        "parent": "Stufe 5 - Optimization",
        "description": (
            "Der Testprozess wird kontinuierlich überwacht, bewertet und "
            "verbessert. Testware wird versioniert, wiederverwendet und "
            "gepflegt, und Verbesserungsmaßnahmen werden pilotiert, bevor "
            "sie organisationsweit ausgerollt werden."
        ),
        "questions": [
            {
                "id": "po-1",
                "text": "Der Testprozess ist dokumentiert und für alle Beteiligten zugänglich.",
                "hint": None,
                "recommendations": {
                    "low": "Dokumentieren Sie den Testprozess in einem zentralen, für alle Testbeteiligten zugänglichen Dokument oder Wiki. Selbst eine kurze Prozessbeschreibung, die wesentliche Aktivitäten, Verantwortlichkeiten und Artefakte benennt, schafft Orientierung und Verbindlichkeit.",
                    "mid": "Überprüfen Sie, ob die Testprozessdokumentation vollständig, aktuell und für alle Beteiligten auffindbar ist. Stellen Sie sicher, dass bei Prozessänderungen die Dokumentation zeitnah aktualisiert wird und alle Betroffenen informiert werden.",
                },
            },
            {
                "id": "po-2",
                "text": "Der Testprozess wird kontinuierlich überwacht, bewertet und verbessert (z.B. Retrospektiven).",
                "hint": None,
                "recommendations": {
                    "low": "Führen Sie nach jeder Testphase oder jedem Release eine kurze Retrospektive durch, die konkrete Verbesserungspotenziale identifiziert, und stellen Sie sicher, dass mindestens eine Maßnahme pro Retrospektive umgesetzt wird.",
                    "mid": "Formalisieren Sie den kontinuierlichen Verbesserungsprozess durch einen festen Zyklus (z.B. vierteljährliche Prozessreviews) und stellen Sie sicher, dass Verbesserungsmaßnahmen nachverfolgt und auf ihre Wirksamkeit hin evaluiert werden.",
                },
            },
            {
                "id": "po-3",
                "text": "Es gibt definierte Prozesse für Change-Management innerhalb des Testprozesses.",
                "hint": None,
                "recommendations": {
                    "low": "Definieren Sie, wie Änderungen am Testprozess beantragt, bewertet, genehmigt und kommuniziert werden, und benennen Sie eine verantwortliche Person für Prozessänderungen. Ohne Change-Management entstehen unkontrollierte Prozessvarianzen.",
                    "mid": "Überprüfen Sie, ob der vorhandene Change-Management-Prozess tatsächlich für alle Testprozessänderungen genutzt wird, und stellen Sie sicher, dass Änderungen vollständig dokumentiert und allen Betroffenen kommuniziert werden.",
                },
            },
            {
                "id": "po-4",
                "text": "Es existieren standardisierte Vorlagen und Checklisten für Testaktivitäten.",
                "hint": None,
                "recommendations": {
                    "low": "Erstellen Sie eine Bibliothek standardisierter Vorlagen für die wichtigsten Testaktivitäten (Testplan, Testfall, Testbericht, Defect-Report) und machen Sie diese für alle Testbeteiligten verbindlich und leicht zugänglich.",
                    "mid": "Überprüfen Sie, ob die vorhandenen Vorlagen tatsächlich konsequent genutzt werden, und aktualisieren Sie sie regelmäßig auf Basis von Rückmeldungen aus der Praxis. Eliminieren Sie überflüssige Vorlagen und stellen Sie sicher, dass die Bibliothek übersichtlich und gepflegt bleibt.",
                },
            },
            {
                "id": "po-5",
                "text": "Die Einhaltung des definierten Testprozesses wird überprüft (Audits, Reviews).",
                "hint": None,
                "recommendations": {
                    "low": "Führen Sie regelmäßige, stichprobenartige Überprüfungen durch, ob der definierte Testprozess in Projekten eingehalten wird, und kommunizieren Sie Abweichungen konstruktiv mit dem Ziel, die Prozessdisziplin zu stärken.",
                    "mid": "Formalisieren Sie die Prozessüberprüfung durch geplante interne Audits mit definiertem Umfang, Prüfkriterien und Maßnahmenverfolgung. Nutzen Sie die Ergebnisse, um sowohl Abweichungen zu korrigieren als auch Prozessschwächen zu beheben.",
                },
            },
            {
                "id": "po-6",
                "text": "Neue Tools/Technologien werden evaluiert und bei Bedarf eingeführt.",
                "hint": None,
                "recommendations": {
                    "low": "Etablieren Sie einen strukturierten Evaluierungsprozess für neue Testwerkzeuge, der Auswahlkriterien, Testphasen (Proof of Concept), Stakeholder-Freigaben und Einführungsplanung umfasst. Spontane Tooleinführungen ohne strukturierte Bewertung führen häufig zu Mehraufwand.",
                    "mid": "Überprüfen Sie, ob neue Tools nach der Einführung systematisch auf ihren Mehrwert hin evaluiert werden, und stellen Sie sicher, dass nicht genutzte oder redundante Tools konsolidiert und abgelöst werden.",
                },
            },
            {
                "id": "po-7",
                "text": "Testartefakte (Testfälle, Testdaten, Testskripte) werden versioniert und verwaltet, inkl. eines für das Testteam zugänglichen Versionsmanagements für Testobjekte/Anforderungen.",
                "hint": "Ist sofort klar, welche Fehler zu welcher Anforderungsversion gehören?",
                "recommendations": {
                    "low": "Führen Sie eine systematische Versionierung von Testfällen, Testskripten und Testdaten ein (z.B. über ein Versionsmanagementsystem oder Testmanagement-Tool), sodass jederzeit nachvollziehbar ist, welche Version eines Tests zu welchem Softwarestand gehört.",
                    "mid": "Überprüfen Sie, ob die Versionierung konsequent und konsistent für alle relevanten Testartefakte durchgeführt wird, und stellen Sie sicher, dass veraltete Versionen archiviert und nicht mehr aktiv verwendet werden.",
                },
            },
            {
                "id": "po-8",
                "text": "Es gibt ein zentrales Repository für Testware sowie ein beschriebenes, dem Team bekanntes Verfahren zur Verwaltung von Testware, Testbasis und Testobjekten.",
                "hint": None,
                "recommendations": {
                    "low": "Richten Sie ein zentrales Repository für alle Testartefakte (Testfälle, Skripte, Testdaten, Testpläne) ein und definieren Sie eine einfache, für das Team verständliche Verzeichnisstruktur und Namenskonvention. Ein zentrales Repository verhindert Duplikate und Versionskonflikte.",
                    "mid": "Überprüfen Sie, ob das Repository von allen Teammitgliedern tatsächlich genutzt wird und ob das Verwaltungsverfahren ausreichend dokumentiert und bekannt ist. Stellen Sie sicher, dass Zugriffsrechte und Backup-Prozesse angemessen definiert sind.",
                },
            },
            {
                "id": "po-9",
                "text": "Die Wiederverwendbarkeit von Testfällen wird aktiv gefördert (z.B. durch modulare Strukturierung).",
                "hint": None,
                "recommendations": {
                    "low": "Strukturieren Sie neue Testfälle von Anfang an modular (z.B. durch Nutzung von Schritten oder Bausteinen), sodass einzelne Testsequenzen in verschiedenen Testfällen wiederverwendet werden können. Das reduziert Redundanzen und Wartungsaufwand erheblich.",
                    "mid": "Analysieren Sie den vorhandenen Testfallbestand auf Redundanzen und Wiederverwendungspotenzial, refaktorisieren Sie häufig verwendete Testsequenzen in wiederverwendbare Bausteine, und überprüfen Sie den Erfolg anhand reduzierter Wartungsaufwände.",
                },
            },
            {
                "id": "po-10",
                "text": "Testfälle und Testdaten werden gepflegt und bei Anforderungsänderungen aktualisiert; Testfälle beziehen sich jeweils auf eine Version/Dokument der Testbasis.",
                "hint": None,
                "recommendations": {
                    "low": "Definieren Sie einen festen Prozessschritt, bei dem Testfälle und Testdaten bei jeder Anforderungsänderung auf Aktualität geprüft und bei Bedarf aktualisiert werden. Veraltete Testfälle erzeugen False Positives und Vertrauensverlust in die Testergebnisse.",
                    "mid": "Überprüfen Sie regelmäßig (z.B. quartalsweise) den gesamten Testfallbestand auf Aktualität, und stellen Sie sicher, dass jeder Testfall auf die Version der Testbasis verweist, aus der er abgeleitet wurde.",
                },
            },
            {
                "id": "po-11",
                "text": "Es existiert eine Rückverfolgbarkeit (Traceability) zwischen Anforderungen, Testfällen und Testergebnissen.",
                "hint": None,
                "recommendations": {
                    "low": "Stellen Sie sicher, dass für alle Anforderungen nachvollziehbar ist, durch welche Testfälle sie abgedeckt werden und mit welchem Ergebnis diese ausgeführt wurden. Eine einfache Traceability-Matrix in einem Tool oder Spreadsheet ist ein ausreichender erster Schritt.",
                    "mid": "Überprüfen Sie, ob die Traceability vollständig und aktuell ist, und stellen Sie sicher, dass sie bei Anforderungsänderungen automatisch oder durch einen definierten Prozessschritt aktualisiert wird.",
                },
            },
            {
                "id": "po-12",
                "text": "Veraltete oder redundante Testfälle werden regelmäßig identifiziert und bereinigt.",
                "hint": None,
                "recommendations": {
                    "low": "Führen Sie mindestens einmal pro Release oder Quartal eine Bereinigung der Testfallbibliothek durch: Identifizieren Sie veraltete, doppelte oder nie ausgeführte Testfälle und entscheiden Sie, ob sie aktualisiert, zusammengeführt oder gelöscht werden.",
                    "mid": "Formalisieren Sie die Testfallpflege als regelmäßigen Prozessschritt mit definierten Kriterien (z.B. Testfälle, die seit mehreren Releases nicht ausgeführt wurden oder denen keine aktive Anforderung zugeordnet ist) und nutzen Sie Metriken zur Steuerung der Bereinigung.",
                },
            },
            {
                "id": "po-13",
                "text": "Testumgebungen können schnell zurückgesetzt/bereitgestellt werden (z.B. durch Automatisierung, Containerisierung).",
                "hint": None,
                "recommendations": {
                    "low": "Implementieren Sie automatisierte Skripte oder Infrastructure-as-Code-Lösungen, um Testumgebungen reproduzierbar und schnell bereitzustellen oder zurückzusetzen. Ein manuell aufzubauendes Testsystem ist ein Risikofaktor für die Testplanung.",
                    "mid": "Überprüfen Sie die aktuelle Bereitstellungszeit für Testumgebungen und identifizieren Sie Optimierungspotenziale durch Containerisierung (z.B. Docker, Kubernetes) oder Pipeline-Automatisierung, um die Flexibilität der Testplanung zu erhöhen.",
                },
            },
            {
                "id": "po-14",
                "text": "Verbesserungsmaßnahmen am Testprozess werden anhand von Pilotprojekten getestet, bevor sie organisationsweit ausgerollt werden.",
                "hint": None,
                "recommendations": {
                    "low": "Definieren Sie für geplante Prozessverbesserungen immer zunächst ein Pilotprojekt, in dem die Maßnahme unter realen Bedingungen erprobt wird, bevor sie organisationsweit eingeführt wird. Pilotierungen reduzieren das Risiko teurer Fehlentscheidungen erheblich.",
                    "mid": "Überprüfen Sie, ob Pilotprojekte mit klaren Erfolgskriterien und Evaluationsplänen durchgeführt werden, und stellen Sie sicher, dass die Erkenntnisse aus Piloten systematisch dokumentiert und in den organisationsweiten Rollout einfließen.",
                },
                "new": True,
            },
            {
                "id": "po-15",
                "text": "Es gibt einen formalen Mechanismus, über den Mitarbeitende Verbesserungsvorschläge für den Testprozess einreichen können.",
                "hint": None,
                "recommendations": {
                    "low": "Richten Sie einen einfachen, niedrigschwelligen Kanal ein (z.B. ein Formular, eine Mailbox oder ein Backlog im Team-Wiki), über den Mitarbeitende Verbesserungsvorschläge für den Testprozess einreichen können, und kommunizieren Sie aktiv, dass Vorschläge erwünscht und willkommen sind.",
                    "mid": "Stellen Sie sicher, dass eingereichte Vorschläge zeitnah geprüft, priorisiert und bewertet werden, und geben Sie dem Einreichenden regelmäßig Rückmeldung über den Status seines Vorschlags. Transparenz im Umgang mit Vorschlägen fördert eine aktive Verbesserungskultur.",
                },
                "new": True,
            },
        ],
    },
]


# Antwort-Optionen mit linearer Wertung
ANSWER_OPTIONS = [
    {"id": "voll",   "label": "Trifft voll zu",       "score": 100},
    {"id": "teil",   "label": "Trifft zum Teil zu",   "score":  50},
    {"id": "kaum",   "label": "Trifft kaum zu",       "score":  25},
    {"id": "nicht",  "label": "Trifft nicht zu",      "score":   0},
]

# Reihenfolge der WARP-Stufen (für Auswertung/Stufenlogik)
WARP_LEVEL_ORDER = [
    "Stufe 2 - Managed",
    "Stufe 3 - Defined",
    "Stufe 4 - Measured",
    "Stufe 5 - Optimization",
]


def total_question_count() -> int:
    return sum(len(c["questions"]) for c in CATEGORIES)


def categories_by_parent() -> dict:
    """Gibt ein Dict zurück: {parent_name: [category, ...]}"""
    result: dict = {}
    for cat in CATEGORIES:
        parent = cat.get("parent", "Sonstige")
        result.setdefault(parent, []).append(cat)
    return result