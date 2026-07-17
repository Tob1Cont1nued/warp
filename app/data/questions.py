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
            },
            {
                "id": "tp-2",
                "text": "Testaufwände fließen in die Projektplanung und Budgetierung mit ein.",
                "hint": None,
            },
            {
                "id": "tp-3",
                "text": "Es werden Testpläne erstellt, die Umfang, Zeitplan, Ressourcen und Abhängigkeiten beschreiben.",
                "hint": "Gibt es einen zeitlichen Plan, wann welche Teststufe durchlaufen wird? Sind Ressourcen und Abwesenheiten berücksichtigt?",
            },
            {
                "id": "tp-4",
                "text": "Bei Planänderungen (z.B. Scope-Änderungen) wird der Testaufwand neu bewertet.",
                "hint": None,
            },
            {
                "id": "tp-5",
                "text": "Es gibt eine Nachverfolgung von geplantem vs. tatsächlichem Testaufwand.",
                "hint": None,
            },
            {
                "id": "tp-6",
                "text": "Pufferzeiten für Nacharbeiten (Retest, Regressionstest) werden eingeplant.",
                "hint": None,
            },
            {
                "id": "tp-7",
                "text": "Stakeholder (Fachbereich, Product Owner, Entwicklung, Management) werden aktiv in die Testplanung eingebunden.",
                "hint": None,
            },
            {
                "id": "tp-8",
                "text": "Es besteht ein gemeinsames Verständnis von Qualitätszielen zwischen Stakeholdern und Testteam.",
                "hint": None,
            },
            {
                "id": "tp-9",
                "text": "Eine Person des Testteams wird in die Projektplanung einbezogen, sodass Abhängigkeiten zwischen Testprozess und anderen Prozessen berücksichtigt werden können.",
                "hint": "Ist jemand aus dem Testteam von Anfang an im Projekt dabei?",
            },
            {
                "id": "tp-10",
                "text": "Risiken für die Testplanung selbst (z.B. Ressourcenverfügbarkeit, Lieferverzögerungen) werden identifiziert und bewertet.",
                "hint": None,
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
            },
            {
                "id": "ueb-2",
                "text": "Testberichte werden regelmäßig (z.B. täglich/wöchentlich) erstellt und verteilt.",
                "hint": None,
            },
            {
                "id": "ueb-3",
                "text": "Berichte enthalten aussagekräftige Informationen zu Testabdeckung, offenen Defects und Risiken.",
                "hint": None,
            },
            {
                "id": "ueb-4",
                "text": "Abschlussberichte (Test Summary Reports) werden am Ende von Testphasen erstellt.",
                "hint": None,
            },
            {
                "id": "ueb-5",
                "text": "Berichte sind zielgruppengerecht aufbereitet (Management vs. operative Ebene).",
                "hint": None,
            },
            {
                "id": "ueb-6",
                "text": "Testergebnisse werden von Stakeholdern als Entscheidungsgrundlage (z.B. für Go-Live) akzeptiert und genutzt.",
                "hint": None,
            },
            {
                "id": "ueb-7",
                "text": "Es gibt definierte Kommunikationswege zwischen Testteam, Entwicklung und Management.",
                "hint": None,
            },
            {
                "id": "ueb-8",
                "text": "Es existieren standardisierte Meetings (z.B. Daily, Testfortschrittsmeetings, Defect Triage).",
                "hint": "Gibt es ein Statusmeeting über den Testfortschritt und Fehler?",
            },
            {
                "id": "ueb-9",
                "text": "Relevante Informationen (Anforderungsänderungen, Risiken) werden zeitnah an das Testteam weitergegeben.",
                "hint": "Fragen Sie regelmäßig nach veränderten/aktualisierten Anforderungen oder neuen Entwicklungen?",
            },
            {
                "id": "ueb-10",
                "text": "Das Testteam gibt vorausschauend Hinweise auf Verzögerungen/Probleme an die Stakeholder.",
                "hint": "Ist im Status eine Risikoabfrage vorhanden? Wie werden Probleme im Test adressiert?",
            },
            {
                "id": "ueb-11",
                "text": "Abweichungen vom Testplan (Zeit, Aufwand, Abdeckung) werden erkannt und es werden Korrekturmaßnahmen eingeleitet.",
                "hint": None,
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
            },
            {
                "id": "tfd-2",
                "text": "Es gibt definierte Qualitätskriterien für Testfälle (z.B. Klarheit, Nachvollziehbarkeit, Wiederholbarkeit).",
                "hint": None,
            },
            {
                "id": "tfd-3",
                "text": "Jeder Testfall enthält: Ausgangssituation, Beschreibung der Aktionen und das erwartete Ergebnis.",
                "hint": None,
            },
            {
                "id": "tfd-4",
                "text": "Das zugehörige Testobjekt (=Teil der Testbasis, das getestet wird) ist im Testfall genannt.",
                "hint": None,
            },
            {
                "id": "tfd-5",
                "text": "Die Abdeckung der Testfälle in Bezug auf Anforderungen ist messbar und nachvollziehbar (Traceability-Matrix).",
                "hint": "Ist der Weg von Anforderung zu Testfall zu Fehler nachvollziehbar?",
            },
            {
                "id": "tfd-6",
                "text": "Testfälle für unterschiedliche Testarten (positiv/negativ, Grenzwerte, Fehlerfälle) werden systematisch erstellt.",
                "hint": None,
            },
            {
                "id": "tfd-7",
                "text": "Es existiert ein definierter Defect-Management-Prozess (Erfassung, Klassifikation, Priorisierung, Behebung, Verifikation), der dem Team bekannt ist.",
                "hint": "Wie sind die Phasen des Fehlerlebenszyklus? Wer entscheidet, ob ein Fehler geschlossen wird?",
            },
            {
                "id": "tfd-8",
                "text": "Ein einheitliches Tool zur Fehlererfassung wird genutzt und ist für alle Verantwortlichen einsehbar.",
                "hint": "Sind die Fehler für alle einsehbar? Sind Schweredefinitionen transparent und bekannt?",
            },
            {
                "id": "tfd-9",
                "text": "Kriterien für Schweregrad und Priorität von Defects sind klar definiert.",
                "hint": None,
            },
            {
                "id": "tfd-10",
                "text": "Die Mindestattribute jedes Fehlers sind: Ersteller/Tester, ID, Datum, Schwere, Beschreibung (erwartetes vs. tatsächliches Ergebnis), Titel, Status.",
                "hint": "Welche Attribute werden in einem Fehler ausgefüllt?",
            },
            {
                "id": "tfd-11",
                "text": "Es gibt einen definierten Workflow inkl. Eskalationsmechanismen für offene/kritische Defects.",
                "hint": None,
            },
            {
                "id": "tfd-12",
                "text": "Der Umgang mit Fehlernachtests (komplett/partiell) ist definiert.",
                "hint": "Was wird nach der Behebung eines Fehlers getestet? Gibt es Richtlinien zum Umfang des Nachtests?",
            },
            {
                "id": "tfd-13",
                "text": "Testergebnisse (Pass/Fail) werden pro Testfall dokumentiert und sind nachvollziehbar.",
                "hint": None,
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
            },
            {
                "id": "tum-2",
                "text": "Es gibt klar definierte Anforderungen an die Testumgebung.",
                "hint": "Wie viele User können gleichzeitig die Umgebung nutzen? Welche Verfügbarkeiten gibt es?",
            },
            {
                "id": "tum-3",
                "text": "Es gibt einen definierten Prozess für Bereitstellung, Konfiguration und Verwaltung von Testumgebungen, inkl. zugeordneter Verantwortlichkeiten (z.B. Umgebungsmanager).",
                "hint": "Wer ist für die Umgebung verantwortlich? Wer informiert über Downtimes und Testzeiten?",
            },
            {
                "id": "tum-4",
                "text": "Die Verfügbarkeit der Testumgebungen wird geplant und überwacht (Umgebungsmanagement).",
                "hint": "Steht die Umgebung während des Tests uneingeschränkt zur Verfügung?",
            },
            {
                "id": "tum-5",
                "text": "Es existiert ein Konzept für Testdatenmanagement (Erstellung, Anonymisierung, Aktualisierung).",
                "hint": "Sind Testdaten auf allen Umgebungen für den Test vorhanden? Sind diese vollständig nutzbar?",
            },
            {
                "id": "tum-6",
                "text": "Konflikte bei der gemeinsamen Nutzung von Testumgebungen durch mehrere Teams werden aktiv gemanagt.",
                "hint": None,
            },
            {
                "id": "tum-7",
                "text": "Änderungen der Testumgebung werden rechtzeitig an den Testmanager herangetragen und können bei Bedarf eingefroren werden (Change Management/Freeze).",
                "hint": "Gibt es ein Change Management für Änderungen? Kann ein Freeze der Umgebung eingefordert werden?",
            },
            {
                "id": "tum-8",
                "text": "Anforderungen an die Testumgebung werden frühzeitig spezifiziert und mit Architektur/Betrieb abgestimmt.",
                "hint": None,
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
            },
            {
                "id": "org-2",
                "text": "Es existiert eine zentrale Testfunktion oder ein Testkompetenzzentrum (Test Center of Excellence).",
                "hint": "Existiert eine Organisations- oder Projekteinheit, die für Testprodukte und Hilfestellungen verantwortlich ist?",
            },
            {
                "id": "org-3",
                "text": "Rollen wie Testmanager, Testanalyst und Testautomatisierer sind klar voneinander abgegrenzt, inklusive Namen.",
                "hint": "Gibt es eine Rollenübersicht (Tester, Testdesigner, Entwickler, Releasemanager, Umgebungsmanager, Projektleiter, Testmanager, Defectmanager)?",
            },
            {
                "id": "org-4",
                "text": "Die Unabhängigkeit der Testorganisation von der Entwicklung ist angemessen sichergestellt.",
                "hint": None,
            },
            {
                "id": "org-5",
                "text": "Es gibt eine organisationsweite Teststandardisierung (Vorlagen, Prozesse, Tools), die den Testern bekannt ist.",
                "hint": "Existiert eine Übersicht der Produkte und Dienstleistungen (z.B. Templates) der Abteilung?",
            },
            {
                "id": "org-6",
                "text": "Testressourcen werden sinnvoll über Projekte hinweg verteilt.",
                "hint": None,
            },
            {
                "id": "org-7",
                "text": "Geeignete Tools für Testmanagement, Testautomatisierung und Defect-Tracking werden eingesetzt und sind dem Testteam bekannt.",
                "hint": "Welche Testwerkzeuge werden genutzt? Sind diese zugänglich für das gesamte Team?",
            },
            {
                "id": "org-8",
                "text": "Die eingesetzten Tools sind integriert (z.B. Anbindung an CI/CD-Pipeline, ALM-Tools).",
                "hint": None,
            },
            {
                "id": "org-9",
                "text": "Es gibt eine strategische Auswahl und Bewertung von Testwerkzeugen (Tool-Strategie), bei der relevante Stakeholder (Einkauf, Projekt, Testteam) vom Nutzen überzeugt sind.",
                "hint": None,
            },
            {
                "id": "org-10",
                "text": "Es gibt Schulungen zur effektiven Nutzung der Testwerkzeuge.",
                "hint": None,
            },
            {
                "id": "org-11",
                "text": "Es existiert ein definiertes, organisationsweites Standard-Testprozessmodell, von dem Projekte ihre eigenen Prozesse ableiten.",
                "hint": None,
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
            },
            {
                "id": "sch-2",
                "text": "Es gibt ein Schulungs- und Weiterbildungskonzept für Testpersonal, das bei Bedarf genutzt werden kann.",
                "hint": "Gibt es Schulungen zu Testvorgaben? Ist eine Schulungsteilnahme bei Bedarf möglich?",
            },
            {
                "id": "sch-3",
                "text": "Wissen wird innerhalb des Testteams aktiv ausgetauscht (z.B. durch Reviews, Pairing, interne Schulungen).",
                "hint": None,
            },
            {
                "id": "sch-4",
                "text": "Karrierepfade für Testrollen sind definiert.",
                "hint": None,
            },
            {
                "id": "sch-5",
                "text": "Soft Skills (z.B. Kommunikation, kritisches Denken) werden bei der Personalentwicklung berücksichtigt.",
                "hint": None,
            },
            {
                "id": "sch-6",
                "text": "Die fachliche Weiterentwicklung der Tester wird regelmäßig evaluiert (z.B. in Mitarbeitergesprächen) in Bezug auf Test- und IT-Fähigkeiten.",
                "hint": None,
            },
            {
                "id": "sch-7",
                "text": "Der individuelle und organisationsweite Schulungsbedarf wird systematisch ermittelt und mit dem Testprozessmodell abgeglichen.",
                "hint": None,
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
            },
            {
                "id": "lc-2",
                "text": "Tester sind in Sprint-Planungen, Refinements und Reviews aktiv eingebunden.",
                "hint": None,
            },
            {
                "id": "lc-3",
                "text": "Testverantwortliche wirken bei der Definition von Akzeptanzkriterien mit.",
                "hint": None,
            },
            {
                "id": "lc-4",
                "text": "Es gibt eine definierte Verantwortlichkeit für Testaktivitäten über den gesamten Lebenszyklus (Shift-Left/Shift-Right).",
                "hint": None,
            },
            {
                "id": "lc-5",
                "text": "Entwickler sind aktiv in Testaktivitäten (z.B. Unit-/Komponententests, Reviews) eingebunden.",
                "hint": None,
            },
            {
                "id": "lc-6",
                "text": "Das Testteam wird frühzeitig in Anforderungs- und Architekturdiskussionen einbezogen und kennt die zuständigen Architekten und Entwickler.",
                "hint": "Gibt es Softwarearchitekten? Wenn ja, wer ist das? Sind die Entwickler bekannt?",
            },
            {
                "id": "lc-7",
                "text": "Es gibt regelmäßige Abstimmungsformate zwischen Test und Business/Fachbereich.",
                "hint": None,
            },
            {
                "id": "lc-8",
                "text": "Es gibt verschiedene definierte Testlevel/Teststufen, die im Projekt verfolgt werden (Unit-, Komponenten-, Integrations-, Regressionstests), deren Ziele dokumentiert sind und zur Teststrategie passen.",
                "hint": None,
            },
            {
                "id": "lc-9",
                "text": "Eine einheitliche Testmethodik (z.B. nach ISTQB-Standard) wird angewendet und vom Projekt- und Testteam unterstützt.",
                "hint": None,
            },
            {
                "id": "lc-10",
                "text": "Testtechniken (z.B. Äquivalenzklassenbildung, Grenzwertanalyse, Entscheidungstabellen) werden systematisch eingesetzt, ggf. unterstützt durch Checklisten oder formale Designtechniken.",
                "hint": None,
            },
            {
                "id": "lc-11",
                "text": "Das Vorgehen ist an die jeweilige Entwicklungsmethodik (Wasserfall, Agile, SAFe) angepasst und schriftlich festgehalten.",
                "hint": None,
            },
            {
                "id": "lc-12",
                "text": "Es gibt definierte Vorgehensweisen für explorative Tests.",
                "hint": None,
            },
            {
                "id": "lc-13",
                "text": "Testtechniken werden je nach Risiko und Testobjekt bewusst ausgewählt.",
                "hint": None,
            },
            {
                "id": "lc-14",
                "text": "Es existiert ein definiertes Vorgehen für Regressionstests.",
                "hint": None,
            },
            {
                "id": "lc-15",
                "text": "Es gibt eine einheitliche Terminologie/ein Glossar, das von allen Beteiligten verwendet wird.",
                "hint": None,
            },
            {
                "id": "lc-16",
                "text": "Testaktivitäten sind an definierten Meilensteinen des Entwicklungsprozesses verankert (z.B. Definition of Ready/Done).",
                "hint": None,
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
                "new": True,
            },
            {
                "id": "nf-2",
                "text": "Für nicht-funktionale Testarten existieren spezifische Teststrategien, Methoden und Werkzeuge.",
                "hint": None,
                "new": True,
            },
            {
                "id": "nf-3",
                "text": "Es gibt definierte Akzeptanzkriterien (z.B. Schwellenwerte) für nicht-funktionale Eigenschaften.",
                "hint": None,
                "new": True,
            },
            {
                "id": "nf-4",
                "text": "Nicht-funktionale Tests sind in den Testplanungs- und Reporting-Prozess integriert.",
                "hint": None,
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
            },
            {
                "id": "pr-2",
                "text": "Bei der Testfallerstellung werden Wiederverwendbarkeit und Wartbarkeit berücksichtigt.",
                "hint": None,
            },
            {
                "id": "pr-3",
                "text": "Es existiert ein definiertes, dokumentiertes Verfahren für Peer Reviews (z.B. von Anforderungen, Architektur, Code, Testbasis).",
                "hint": None,
                "new": True,
            },
            {
                "id": "pr-4",
                "text": "Für Reviews werden Checklisten oder Leitfäden genutzt, um Konsistenz sicherzustellen.",
                "hint": None,
                "new": True,
            },
            {
                "id": "pr-5",
                "text": "Ergebnisse aus Reviews werden erfasst, nachverfolgt und in Metriken berücksichtigt.",
                "hint": None,
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
            },
            {
                "id": "tme-2",
                "text": "Metriken werden genutzt, um Entscheidungen zu treffen (z.B. Release-Freigabe).",
                "hint": None,
            },
            {
                "id": "tme-3",
                "text": "Es gibt definierte Zielwerte/Benchmarks für relevante Metriken.",
                "hint": None,
            },
            {
                "id": "tme-4",
                "text": "Metriken werden regelmäßig analysiert, um Prozessverbesserungen abzuleiten.",
                "hint": None,
            },
            {
                "id": "tme-5",
                "text": "Es wird zwischen Prozess-, Produkt- und Projektmetriken unterschieden.",
                "hint": None,
            },
            {
                "id": "tme-6",
                "text": "Die erhobenen Metriken sind für alle Stakeholder nachvollziehbar und konsistent definiert.",
                "hint": None,
            },
            {
                "id": "tme-7",
                "text": "Trends (z.B. Defect-Trends, Fortschrittstrends) werden über Zeit dargestellt und ausgewertet.",
                "hint": None,
            },
            {
                "id": "tme-8",
                "text": "Der Reifegrad der Testautomatisierung wird regelmäßig bewertet (z.B. Automatisierungsgrad, Wartungsaufwand).",
                "hint": None,
            },
            {
                "id": "tme-9",
                "text": "Die benötigten Daten werden synchron ermittelt, zentral gespeichert und es gibt Prüfungen zur Validierung der genutzten Daten (Stichproben).",
                "hint": "Werden die zugrundeliegenden Daten zentral gespeichert und stichprobenartig auf Validität geprüft?",
            },
            {
                "id": "tme-10",
                "text": "Mindestens 7 der folgenden Metriken werden genutzt: Testüberdeckungsverhältnis, Anzahl Testfälle geplant/bereits erstellt, Testfortschritt (Ist/Plan), Testdurchführungsverhältnis, Fehlerschwere, Anzahl Produktionsfehler, verbrauchter Budgetanteil, Testphasen/verbrauchte Stunden, Leerlaufrate, Testendekriterien.",
                "hint": "Welche Metriken werden genutzt?",
            },
            {
                "id": "tme-11",
                "text": "Ein organisationsweites Metrikprogramm definiert verbindliche Kennzahlen, die projektübergreifend vergleichbar sind.",
                "hint": None,
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
                "new": True,
            },
            {
                "id": "pq-2",
                "text": "Qualitätsziele für das Produkt werden quantitativ definiert und im Projektverlauf gemessen.",
                "hint": None,
                "new": True,
            },
            {
                "id": "pq-3",
                "text": "Die tatsächliche Produktqualität wird mit den definierten Qualitätszielen verglichen und Abweichungen werden bewertet.",
                "hint": None,
                "new": True,
            },
            {
                "id": "pq-4",
                "text": "Defect-Daten werden ausgewertet, um Muster (z.B. fehleranfällige Module) zu identifizieren.",
                "hint": None,
            },
            {
                "id": "pq-5",
                "text": "Root-Cause-Analysen werden bei kritischen Defects durchgeführt.",
                "hint": None,
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
                "new": True,
            },
            {
                "id": "er-2",
                "text": "Review-Daten werden genutzt, um die Wirksamkeit von Reviews im Vergleich zu dynamischen Tests zu bewerten.",
                "hint": None,
                "new": True,
            },
            {
                "id": "er-3",
                "text": "Auf Basis von Review-Metriken werden gezielte Verbesserungen am Review-Prozess vorgenommen.",
                "hint": None,
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
                "new": True,
            },
            {
                "id": "fv-2",
                "text": "Es existiert ein definierter Prozess, um aus Fehlerursachen präventive Maßnahmen abzuleiten und deren Wirksamkeit zu verfolgen.",
                "hint": None,
                "new": True,
            },
            {
                "id": "fv-3",
                "text": "Lessons Learned aus abgeschlossenen Projekten werden systematisch in den Testprozess eingearbeitet.",
                "hint": None,
            },
            {
                "id": "fv-4",
                "text": "Erkenntnisse zur Fehlervermeidung werden organisationsweit kommuniziert und in Schulungen/Standards integriert.",
                "hint": None,
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
                "new": True,
            },
            {
                "id": "qk-2",
                "text": "Abweichungen vom erwarteten (statistisch normalen) Prozessverhalten werden erkannt und Ursachen gezielt untersucht.",
                "hint": None,
                "new": True,
            },
            {
                "id": "qk-3",
                "text": "Prognosen zu Qualität und Aufwand basieren auf historischen, statistisch abgesicherten Daten.",
                "hint": None,
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
            },
            {
                "id": "po-2",
                "text": "Der Testprozess wird kontinuierlich überwacht, bewertet und verbessert (z.B. Retrospektiven).",
                "hint": None,
            },
            {
                "id": "po-3",
                "text": "Es gibt definierte Prozesse für Change-Management innerhalb des Testprozesses.",
                "hint": None,
            },
            {
                "id": "po-4",
                "text": "Es existieren standardisierte Vorlagen und Checklisten für Testaktivitäten.",
                "hint": None,
            },
            {
                "id": "po-5",
                "text": "Die Einhaltung des definierten Testprozesses wird überprüft (Audits, Reviews).",
                "hint": None,
            },
            {
                "id": "po-6",
                "text": "Neue Tools/Technologien werden evaluiert und bei Bedarf eingeführt.",
                "hint": None,
            },
            {
                "id": "po-7",
                "text": "Testartefakte (Testfälle, Testdaten, Testskripte) werden versioniert und verwaltet, inkl. eines für das Testteam zugänglichen Versionsmanagements für Testobjekte/Anforderungen.",
                "hint": "Ist sofort klar, welche Fehler zu welcher Anforderungsversion gehören?",
            },
            {
                "id": "po-8",
                "text": "Es gibt ein zentrales Repository für Testware sowie ein beschriebenes, dem Team bekanntes Verfahren zur Verwaltung von Testware, Testbasis und Testobjekten.",
                "hint": None,
            },
            {
                "id": "po-9",
                "text": "Die Wiederverwendbarkeit von Testfällen wird aktiv gefördert (z.B. durch modulare Strukturierung).",
                "hint": None,
            },
            {
                "id": "po-10",
                "text": "Testfälle und Testdaten werden gepflegt und bei Anforderungsänderungen aktualisiert; Testfälle beziehen sich jeweils auf eine Version/Dokument der Testbasis.",
                "hint": None,
            },
            {
                "id": "po-11",
                "text": "Es existiert eine Rückverfolgbarkeit (Traceability) zwischen Anforderungen, Testfällen und Testergebnissen.",
                "hint": None,
            },
            {
                "id": "po-12",
                "text": "Veraltete oder redundante Testfälle werden regelmäßig identifiziert und bereinigt.",
                "hint": None,
            },
            {
                "id": "po-13",
                "text": "Testumgebungen können schnell zurückgesetzt/bereitgestellt werden (z.B. durch Automatisierung, Containerisierung).",
                "hint": None,
            },
            {
                "id": "po-14",
                "text": "Verbesserungsmaßnahmen am Testprozess werden anhand von Pilotprojekten getestet, bevor sie organisationsweit ausgerollt werden.",
                "hint": None,
                "new": True,
            },
            {
                "id": "po-15",
                "text": "Es gibt einen formalen Mechanismus, über den Mitarbeitende Verbesserungsvorschläge für den Testprozess einreichen können.",
                "hint": None,
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