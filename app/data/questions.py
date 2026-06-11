"""
WARP Tool - Fragenkatalog Daten

Basierend auf dem Wavestone / Q_PERIOR TPI-Next-Reifegrad Quick-Check.
Kategorien orientieren sich an Testmanagement-Reifegradanalyse (Stufe "Kontrolliert").

Struktur:
  - 3 Hauptbereiche: Stakeholderbeziehung, Testmanagement, Testkompetenz
  - 19 Unterkategorien, ~83 Fragen insgesamt

Erweitern: einfach neue Kategorien/Fragen anhängen.
"""

CATEGORIES = [
    # =========================================================================
    # HAUPTBEREICH 1: STAKEHOLDERBEZIEHUNG
    # =========================================================================
    {
        "id": "engagement",
        "title": "Engagement der Stakeholder",
        "parent": "Stakeholderbeziehung",
        "description": (
            "Das Engagement der Stakeholder ist maßgebend für eine effiziente "
            "Kommunikation und gute Zusammenarbeit."
        ),
        "questions": [
            {
                "id": "eng-1",
                "text": "Der Anforderungsmanager/Fachbereich zuständig für die Anforderungen ist bekannt.",
                "hint": "Wissen Sie wer für welche Anforderung fachlich zuständig ist?",
            },
            {
                "id": "eng-2",
                "text": "Die Tester kennen den Auftraggeber.",
                "hint": "Wer ist ihr Auftraggeber?",
            },
            {
                "id": "eng-3",
                "text": "Der Auftraggeber hat das Budget bewilligt und dieses kann mit ihm verhandelt werden.",
                "hint": "Kann die Dauer des Tests mit dem Auftraggeber verhandelt werden?",
            },
            {
                "id": "eng-4",
                "text": "Die Testressourcen werden von den Stakeholdern zur Verfügung gestellt.",
                "hint": "Werden Tester aus den Fachbereichen nach Anfrage zur Verfügung gestellt?",
            },
            {
                "id": "eng-5",
                "text": "Der Auftraggeber hat eine dokumentierte Produktrisikoanalyse erstellt.",
                "hint": "Gibt es eine Risikoanalyse für die Software?",
            },
            {
                "id": "eng-6",
                "text": "Fachabteilungen, die mit dem Produkt arbeiten, sind bekannt.",
                "hint": "Welche Abteilungen arbeiten alles mit der Software?",
            },
            {
                "id": "eng-7",
                "text": "Die Releaseprozesse und Ansprechpartner sind bekannt.",
                "hint": "Wer ist Hauptansprechpartner im Releasemanagement? Gibt es Freigabeszenarien?",
            },
            {
                "id": "eng-8",
                "text": "Die Entwickler sind bekannt.",
                "hint": None,
            },
            {
                "id": "eng-9",
                "text": "Die Softwarearchitekten sind bekannt.",
                "hint": "Gibt es Softwarearchitekten? Wenn ja, wer ist das?",
            },
        ],
    },
    {
        "id": "beteiligung",
        "title": "Grad der Beteiligung",
        "parent": "Stakeholderbeziehung",
        "description": (
            "Ein hoher Grad der Beteiligung des Testteams im Projekt und Entwicklungsprozess "
            "hilft dabei, die meisten Testaktivitäten fern vom kritischen Pfad durchzuführen."
        ),
        "questions": [
            {
                "id": "bet-1",
                "text": "Der Umfang, der Testauftrag und das Vorgehen sind mit dem Auftraggeber vereinbart.",
                "hint": "Kennt der Auftraggeber die geschätzte Dauer des Tests und hat den Inhalten zugestimmt?",
            },
            {
                "id": "bet-2",
                "text": (
                    "Eine Person des Testteams wird in die Projektplanung einbezogen, "
                    "sodass Abhängigkeiten zwischen dem Testprozess und anderen Prozessen "
                    "berücksichtigt werden können."
                ),
                "hint": (
                    "Ist jemand aus dem Testteam von Anfang an im Projekt dabei? "
                    "Bekommt er mit, wenn Anforderungen definiert und Entwicklungsobjekte testbereit sind?"
                ),
            },
            {
                "id": "bet-3",
                "text": "Ein Tester wird bei der Analyse, Bewertung und dem Management von Projektrisiken einbezogen.",
                "hint": None,
            },
            {
                "id": "bet-4",
                "text": "Die Testplanung erfolgt gleichzeitig mit der Projektplanung.",
                "hint": "Wer erstellt die Projektplanung? Wann erfolgt die Testplanung?",
            },
            {
                "id": "bet-5",
                "text": "Nur die Testdurchführung befindet sich auf dem kritischen Projektpfad.",
                "hint": "Wann wird mit der Testvorbereitung gestartet? Wann endet sie?",
            },
        ],
    },
    {
        "id": "teststrategie",
        "title": "Teststrategie",
        "parent": "Stakeholderbeziehung",
        "description": (
            "Die Strategie sorgt für ein stimmiges Verhältnis von "
            "Aufwand/Ressourcen zu dem vorhandenen Risiko."
        ),
        "questions": [
            {
                "id": "ts-1",
                "text": "Produktrisiken, die den Go-live beeinträchtigen könnten, sind analysiert.",
                "hint": "Gibt es spezielle Testfälle für den Go-live zur Überpruefung der wichtigsten Funktionalitäten?",
            },
            {
                "id": "ts-2",
                "text": "Produktrisiken sind in die Priorisierung der Testfälle einbezogen.",
                "hint": "Gibt es eine Priorisierung der Testfälle? Wie wurde diese vorgenommen?",
            },
            {
                "id": "ts-3",
                "text": "Der finale Testaufwand/Ressourcen sind nach einer Risikoanalyse bestimmt worden.",
                "hint": "Ist der Zusammenhang zwischen Risiko und Aufwand betrachtet worden?",
            },
            {
                "id": "ts-4",
                "text": "Besonders risikobehaftete Softwarekomponenten oder Prozesse werden zuerst getestet.",
                "hint": "Werden risikoreiche Softwarekomponenten zuerst getestet? Gibt es eine Übersicht?",
            },
            {
                "id": "ts-5",
                "text": (
                    "Risiken werden bei verschiedenen Teststufen, Testarten sowie der "
                    "Testabdeckung und Testintensität berücksichtigt."
                ),
                "hint": "Erfolgt ein Test in verschiedenen Teststufen (Entwicklertests, Systemtest, Abnahmetests)?",
            },
            {
                "id": "ts-6",
                "text": "Fehlernachtests und Regressionstests werden durchgeführt.",
                "hint": "Gibt es eine Empfehlung vom Entwickler, wie viel nach der Fehlerbehebung getestet wird?",
            },
        ],
    },
    {
        "id": "testorganisation",
        "title": "Testorganisation",
        "parent": "Stakeholderbeziehung",
        "description": (
            "Die Testorganisation ist Wissensträger und sorgt dafür, dass Testressourcen, "
            "Testprodukte (Prozesse, Werkzeuge, Templates, Richtlinien) und "
            "Testdienstleistungen (Trainings) vorhanden sind."
        ),
        "questions": [
            {
                "id": "to-1",
                "text": (
                    "Es gibt eine Organisations- oder Projekteinheit, die für "
                    "Testprodukte und Hilfestellungen verantwortlich ist."
                ),
                "hint": "Existiert eine solche Einheit?",
            },
            {
                "id": "to-2",
                "text": "Es gibt eine Übersicht der Produkte und Dienstleistungen, die den Testern bekannt ist.",
                "hint": "Existiert eine Übersicht der Produkte und Dienstleistungen (z.B. Templates) der Abteilung?",
            },
            {
                "id": "to-3",
                "text": (
                    "Es gibt klar definierte Verantwortlichkeiten und eine Rollenübersicht "
                    "(Tester, Testdesigner, Entwickler, Releasemanager, Umgebungsmanager, "
                    "Projektleiter, Testmanager, Defectmanager inkl. Namen)."
                ),
                "hint": "Gibt es klar definierte Verantwortlichkeiten? Kennen Sie Ihre Rolle und Aufgaben?",
            },
        ],
    },
    {
        "id": "kommunikation",
        "title": "Kommunikation",
        "parent": "Stakeholderbeziehung",
        "description": (
            "Gezielte und transparente Informationsweitergabe fördert ein gemeinsames "
            "Verständnis und abgestimmte Erwartungshaltungen aller im Test beteiligten Personen."
        ),
        "questions": [
            {
                "id": "kom-1",
                "text": "Die Teammitglieder werden über Entscheidungen im Projekt informiert.",
                "hint": "Wie erhalten Sie Informationen zu Entscheidungen im Projekt?",
            },
            {
                "id": "kom-2",
                "text": "Alle Teammitglieder kennen den Status und die Phase, in der sich das Projekt befindet.",
                "hint": "In welcher Projektphase befindet sich das Projekt aktuell?",
            },
            {
                "id": "kom-3",
                "text": "Entscheidungen, Handlungen und Ergebnisse des Testteams können zurückverfolgt werden.",
                "hint": "Wie werden Entscheidungen vom Testteam festgehalten?",
            },
            {
                "id": "kom-4",
                "text": (
                    "Es gibt regelmäßigen Austausch zwischen Testteam und Stakeholdern über "
                    "Projekt- und Testfortschritt, Qualität des Produktes und Risiken."
                ),
                "hint": "Gibt es ein Statusmeeting über den Testfortschritt und Fehler?",
            },
            {
                "id": "kom-5",
                "text": "Das Testteam gibt vorausschauend Hinweise auf Verzögerungen/Probleme an die Stakeholder.",
                "hint": "Ist im Status eine Risikoabfrage vorhanden? Wie werden Probleme im Test adressiert?",
            },
            {
                "id": "kom-6",
                "text": "Das Testteam fragt aktiv nach für den Test relevanten Informationen bei den Stakeholdern nach.",
                "hint": "Fragen Sie regelmäßig nach veränderten/aktualisierten Anforderungen oder neuen Entwicklungen?",
            },
        ],
    },
    {
        "id": "berichterstattung",
        "title": "Berichterstattung",
        "parent": "Stakeholderbeziehung",
        "description": (
            "Gibt dem Auftraggeber/Stakeholder konkrete Informationen über "
            "Produktqualität/Risiken, sodass Entscheidungen getroffen werden können."
        ),
        "questions": [
            {
                "id": "ber-1",
                "text": (
                    "Es gibt regelmäßige schriftliche Berichte über den Testfortschritt (IST/PLAN) "
                    "in Bezug auf Zeit, Budget, Testfällen und Fehlern."
                ),
                "hint": "Gibt es Testberichte zum Fortschritt gegliedert nach Zeit/Budget/Testfällen und Fehlern?",
            },
            {
                "id": "ber-2",
                "text": "Die Berichte enthalten Ergebnisse und Risiken.",
                "hint": "Enthalten die Berichte Ergebnisse und Risiken?",
            },
            {
                "id": "ber-3",
                "text": "Die Stakeholder sind zufrieden mit dem Inhalt, der Qualität und der Häufigkeit der Berichte.",
                "hint": "Sind Sie zufrieden mit dem Inhalt, der Qualität und der Häufigkeit der Berichte?",
            },
            {
                "id": "ber-4",
                "text": "Produktrisiken und Projektrisiken sind in die Berichte einbezogen.",
                "hint": None,
            },
            {
                "id": "ber-5",
                "text": "Es gibt Trendanalysen über Fehler/Testfälle.",
                "hint": None,
            },
            {
                "id": "ber-6",
                "text": "Die Berichte enthalten Empfehlungen für Entscheidungen.",
                "hint": None,
            },
        ],
    },

    # =========================================================================
    # HAUPTBEREICH 2: TESTMANAGEMENT
    # =========================================================================
    {
        "id": "testprozessmanagement",
        "title": "Testprozessmanagement",
        "parent": "Testmanagement",
        "description": (
            "Sorgt dafür, dass der Testauftrag innerhalb von vorher abgestimmten "
            "Kosten, Zeit und Ergebnis optimiert wird."
        ),
        "questions": [
            {
                "id": "tpm-1",
                "text": (
                    "Es gibt einen Testplan, der zeitlich festlegt, wer was wann macht. "
                    "Dieser umfasst alle Phasen des Testprozesses."
                ),
                "hint": (
                    "Gibt es einen zeitlichen Plan, wann welche Teststufe durchlaufen wird? "
                    "Sind Ressourcen und Abwesenheiten berücksichtigt?"
                ),
            },
            {
                "id": "tpm-2",
                "text": (
                    "Der Testplan beinhaltet den Testauftrag, den Zeitraum, "
                    "die zeitliche Ressourcenplanung sowie Rollen und Verantwortlichkeiten."
                ),
                "hint": "Sind Ihnen die Testzeitraeume bekannt?",
            },
            {
                "id": "tpm-3",
                "text": "Die Erwartungen des Auftraggebers zu Umfang, Kosten und Qualität des Testens sind klar.",
                "hint": None,
            },
            {
                "id": "tpm-4",
                "text": "Ein Bericht gibt den Fortschritt des Testplans und geeignete Maßnahmen wieder.",
                "hint": None,
            },
            {
                "id": "tpm-5",
                "text": "Der Testplan ist mit den Stakeholdern (inkl. Auftraggeber) abgestimmt.",
                "hint": None,
            },
        ],
    },
    {
        "id": "kostenschätzung",
        "title": "Kostenschätzung und Planung",
        "parent": "Testmanagement",
        "description": (
            "Passende Schätztechniken ermöglichen eine realistische und "
            "zuverlässige Einschätzung der Kosten und Planung des Testvorgehens."
        ),
        "questions": [
            {
                "id": "kp-1",
                "text": "Es existiert eine Schätzung der benötigten Ressourcen pro Testaktivitaet.",
                "hint": None,
            },
            {
                "id": "kp-2",
                "text": "Es gibt ein zugewiesenes Budget für jede Phase des Testprozesses.",
                "hint": None,
            },
            {
                "id": "kp-3",
                "text": "Der Auftraggeber wird aktiv in die Schätzungen einbezogen.",
                "hint": None,
            },
            {
                "id": "kp-4",
                "text": (
                    "Die Dauer der einzelnen Testaktivitäten, die benötigten Ressourcen "
                    "und die zu erwartenden Ergebnisse sind bekannt."
                ),
                "hint": None,
            },
            {
                "id": "kp-5",
                "text": "Die Testplanung berücksichtigt Abhängigkeiten zwischen einzelnen Phasen oder Aktivitäten.",
                "hint": "Werden Abhängigkeiten zwischen Aktivitäten in der Testplanung berücksichtigt?",
            },
        ],
    },
    {
        "id": "metriken",
        "title": "Metriken",
        "parent": "Testmanagement",
        "description": (
            "Durch Metriken ist eine objektive Messung des Fortschritts, "
            "der Fehler und des Prozesses möglich."
        ),
        "questions": [
            {
                "id": "met-1",
                "text": "Es werden Metriken verwendet, die das Testprojekt bewerten und monitoren.",
                "hint": "Gibt es Metriken, die das Testobjekt bewerten?",
            },
            {
                "id": "met-2",
                "text": (
                    "Die benötigten Daten werden synchron ermittelt und "
                    "alle Metriken werden zentral gespeichert."
                ),
                "hint": "Werden die zugrundeliegenden Daten der Metriken synchron ermittelt und zentral gespeichert?",
            },
            {
                "id": "met-3",
                "text": "Es gibt Pruefungen zur Validierung der genutzten Daten (Stichproben).",
                "hint": "Werden die genutzten Metriken stichprobenartig geprueft, ob die Daten valide sind?",
            },
            {
                "id": "met-4",
                "text": (
                    "Mindestens 7 der folgenden Metriken werden genutzt: Testüberdeckungsverhaeltnis, "
                    "Anzahl Testfälle geplant/bereits erstellt, Testfortschritt (Ist/Plan), "
                    "Testdurchführungsverhaeltnis, Fehlerschwere, Anzahl Produktionsfehler, "
                    "verbrauchter Budgetanteil, Testphasen/verbrauchte Stunden, Leerlaufrate, Testendekriterien."
                ),
                "hint": "Welche Metriken werden genutzt?",
            },
        ],
    },
    {
        "id": "fehlermanagement",
        "title": "Fehlermanagement",
        "parent": "Testmanagement",
        "description": (
            "Das Fehlermanagement verfolgt Fehler und überwacht deren Status einzeln und "
            "als Gesamtheit. Zusaetzlich analysiert es die Ursachen und gibt Handlungsempfehlungen."
        ),
        "questions": [
            {
                "id": "fm-1",
                "text": "Es gibt ein Fehlermanagement inkl. Fehlerlebenszyklus, das dem Test- und Entwicklerteam bekannt ist.",
                "hint": "Wie sind die Phasen des Fehlerlebenszyklus? Wer entscheidet, ob ein Fehler geschlossen wird?",
            },
            {
                "id": "fm-2",
                "text": "Regelmäßige Fehlerbesprechungen unterstuetzen das Fehlermanagement.",
                "hint": "Gibt es regelmäßige Termine, um über bestimmte Fehler oder Fehleranfälligkeiten zu sprechen?",
            },
            {
                "id": "fm-3",
                "text": (
                    "Verantwortliche Personen im Fehlerprozess sind definiert "
                    "(Tester, Entwickler, Umgebungsmanager, Testmanager)."
                ),
                "hint": "Wer ist alles im Fehlerprozess involviert und was sind seine Aufgaben?",
            },
            {
                "id": "fm-4",
                "text": "Genutzte Fehlermanagementwerkzeuge sind für verantwortliche Personen nutzbar.",
                "hint": "Sind die Fehler für alle einsehbar? Sind Schweredefinitionen transparent und bekannt?",
            },
            {
                "id": "fm-5",
                "text": "Der Umgang mit Fehlernachtests (komplett/partiell) ist definiert.",
                "hint": "Was wird nach der Behebung eines Fehlers getestet? Gibt es Richtlinien zum Umfang des Nachtests?",
            },
            {
                "id": "fm-6",
                "text": (
                    "Die Mindestattribute jedes Fehlers sind: Ersteller/Tester, ID, Datum, Schwere, "
                    "Beschreibung (erwartetes vs. tatsaechliches Ergebnis), Titel, Status."
                ),
                "hint": "Welche Attribute werden in einem Fehler ausgefuellt?",
            },
        ],
    },
    {
        "id": "testwaremanagement",
        "title": "Testwaremanagement",
        "parent": "Testmanagement",
        "description": (
            "Sorgt dafür, dass die einzelnen Testprodukte zueinander "
            "und zu den zugehörigen Entwurfsdokumenten passen."
        ),
        "questions": [
            {
                "id": "tw-1",
                "text": (
                    "Es gibt ein für das Testteam zugaengliches Versionsmanagement "
                    "für die Testobjekte/Anforderungen (Versionsnummer und Name)."
                ),
                "hint": "Ist sofort klar, welche Fehler zu welcher Anforderungsversion gehören?",
            },
            {
                "id": "tw-2",
                "text": (
                    "Es gibt ein beschriebenes Verfahren, mit dem Testware, Testbasis "
                    "und Testobjekte verwaltet werden. Dieses ist dem Team bekannt."
                ),
                "hint": None,
            },
            {
                "id": "tw-3",
                "text": "Die Testfälle beziehen sich jeweils auf eine Version/Dokument der Testbasis.",
                "hint": None,
            },
            {
                "id": "tw-4",
                "text": "Testfälle und Anforderungen sind miteinander verknuepft.",
                "hint": "Ist der Weg von Anforderung zu Testfall zu Fehler nachvollziehbar?",
            },
        ],
    },

    # =========================================================================
    # HAUPTBEREICH 3: TESTKOMPETENZ
    # =========================================================================
    {
        "id": "methodisches_vorgehen",
        "title": "Methodisches Vorgehen",
        "parent": "Testkompetenz",
        "description": (
            "Eine Testmethode navigiert das Testvorgehen und hilft, mit Zielen und "
            "Vorbedingungen ein ausgewogenes Verhältnis zwischen Ergebnistypen, "
            "Risiken, Zeit und Kosten sicherzustellen."
        ),
        "questions": [
            {
                "id": "mv-1",
                "text": (
                    "Es gibt verschiedene definierte Testlevel/Teststufen, die im Projekt "
                    "verfolgt werden (Unit Tests, Komponententests, Integrationstests, Regressionstests)."
                ),
                "hint": None,
            },
            {
                "id": "mv-2",
                "text": "Die Ziele der Testlevel/Teststufen sind dokumentiert und passen zur Teststrategie.",
                "hint": None,
            },
            {
                "id": "mv-3",
                "text": (
                    "Die einzelnen Testlevel/Teststufen sind abgestimmt auf das Projektvorgehen/"
                    "die Entwicklung und sind schriftlich festgehalten."
                ),
                "hint": "Sind die Umgebungen passend für den jeweiligen Test?",
            },
            {
                "id": "mv-4",
                "text": "Das Projekt- und Testteam unterstuetzt die gewählten Testmethoden.",
                "hint": None,
            },
        ],
    },
    {
        "id": "professionalität",
        "title": "Professionalität der Tester",
        "parent": "Testkompetenz",
        "description": (
            "Beschreibt die richtige Mischung aus unterschiedlichen Fähigkeiten und Fachwissen, "
            "um die Tests mit dem erforderlichen Know-how zu unterstuetzen."
        ),
        "questions": [
            {
                "id": "pro-1",
                "text": (
                    "Die Tester planen ihre Testaktivitäten im Austausch mit den Kollegen, "
                    "fuehren diese eigenständig durch und geben proaktiv Feedback."
                ),
                "hint": "Wie planen Sie Ihre Testaktivitäten? Was passiert, wenn Sie krank werden oder Urlaub planen?",
            },
            {
                "id": "pro-2",
                "text": (
                    "Die Tester erhalten dedizierte Testschulungen oder haben bereits "
                    "ausreichende Erfahrungen bei der strukturierten Testdurchführung."
                ),
                "hint": "Gibt es Schulungen zu Testvorgaben? Ist eine Schulungsteilnahme bei Bedarf möglich?",
            },
            {
                "id": "pro-3",
                "text": "Die Testmethode ist den Testern bekannt und wird eingesetzt.",
                "hint": None,
            },
            {
                "id": "pro-4",
                "text": "Das Testteam hat Zugang zu benoetgtem Fachwissen und technischem Wissen.",
                "hint": None,
            },
            {
                "id": "pro-5",
                "text": "Die Tester sind zertifiziert nach ISTQB Foundation Level.",
                "hint": None,
            },
            {
                "id": "pro-6",
                "text": (
                    "Es gibt regelmäßige Leistungsbeurteilungen der Tester "
                    "in Bezug auf ihre Test- und IT-Fähigkeiten."
                ),
                "hint": None,
            },
        ],
    },
    {
        "id": "testfalldesign",
        "title": "Testfalldesign",
        "parent": "Testkompetenz",
        "description": "Setzt die Teststrategie ein, um die Fehlersuche zu optimieren.",
        "questions": [
            {
                "id": "tfd-1",
                "text": "Testfälle sind personenunabhängig wiederholbar (aehnlicher Wissensstand der Tester vorausgesetzt).",
                "hint": None,
            },
            {
                "id": "tfd-2",
                "text": "Es werden zunaechst logische Testfälle beschrieben, die dann konkretisiert werden.",
                "hint": None,
            },
            {
                "id": "tfd-3",
                "text": (
                    "Jeder Testfall enthaelt: Ausgangssituation, Beschreibung der Aktionen "
                    "und das erwartete Ergebnis."
                ),
                "hint": None,
            },
            {
                "id": "tfd-4",
                "text": "Das zugehoerige Testobjekt (=Teil der Testbasis, das getestet wird) ist im Testfall genannt.",
                "hint": None,
            },
            {
                "id": "tfd-5",
                "text": "Checklisten oder formale Designtechniken werden zur Testfallerstellung eingesetzt.",
                "hint": None,
            },
        ],
    },
    {
        "id": "testwerkzeuge",
        "title": "Testwerkzeuge",
        "parent": "Testkompetenz",
        "description": (
            "Testwerkzeuge beschleunigen/ermöglichen die Testaktivitäten, "
            "indem sie dem Testteam Arbeit abnehmen."
        ),
        "questions": [
            {
                "id": "twz-1",
                "text": (
                    "Testwerkzeuge, die für die Testaktivitäten benötigt werden, "
                    "sind zugaenglich für das Testteam "
                    "(z.B. Planungswerkzeuge, Stubs, Steuerungswerkzeuge, Testdurchführungswerkzeuge)."
                ),
                "hint": "Welche Testwerkzeuge werden genutzt? Sind diese zugaenglich für das gesamte Team?",
            },
            {
                "id": "twz-2",
                "text": "Das Testteam kennt die eingesetzten Werkzeuge.",
                "hint": None,
            },
            {
                "id": "twz-3",
                "text": (
                    "Die beteiligten Stakeholder des Werkzeuges (Einkauf, Projekt, Testteam) "
                    "sind überzeugt vom Nutzen des Werkzeuges."
                ),
                "hint": None,
            },
        ],
    },
    {
        "id": "testumgebung",
        "title": "Testumgebung",
        "parent": "Testkompetenz",
        "description": (
            "Die Testumgebung sollte auf die Ziele der einzelnen Teststufen angepasst sein "
            "und die jeweils benötigten Funktionalitäten bieten."
        ),
        "questions": [
            {
                "id": "tum-1",
                "text": "Es gibt klar definierte Anforderungen an die Testumgebung.",
                "hint": "Wie viele User können gleichzeitig die Umgebung nutzen? Welche Verfügbarkeiten gibt es?",
            },
            {
                "id": "tum-2",
                "text": (
                    "Aufgaben und Verantwortlichkeiten zur Umgebung sind mit den "
                    "zuständigen Parteien (z.B. Umgebungsmanager) definiert und abgestimmt."
                ),
                "hint": "Wer ist für die Umgebung verantwortlich? Wer informiert über Downtimes und Testzeiten?",
            },
            {
                "id": "tum-3",
                "text": "Die Umgebung steht in den definierten Testzeitraeumen ohne Unterbrechung zur Verfügung.",
                "hint": "Steht die Umgebung waehrend des Tests uneingeschraenkt zur Verfügung?",
            },
            {
                "id": "tum-4",
                "text": "Aenderungen der Testumgebung werden rechtzeitig an den Testmanager herangetragen.",
                "hint": "Gibt es ein Change Management für Aenderungen? Wie viel Vorlaufzeit gibt es bei Aenderungen?",
            },
            {
                "id": "tum-5",
                "text": "Der Testmanager kann einen Freeze der Umgebung gemeinsam mit dem Projektleiter anfordern.",
                "hint": "Kann ein Freeze der Umgebung eingefordert werden?",
            },
            {
                "id": "tum-6",
                "text": "Testdaten werden berücksichtigt.",
                "hint": "Sind Testdaten auf allen Umgebungen für den Test vorhanden? Sind diese vollständig nutzbar?",
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


def total_question_count() -> int:
    return sum(len(c["questions"]) for c in CATEGORIES)


def categories_by_parent() -> dict:
    """Gibt ein Dict zurück: {parent_name: [category, ...]}"""
    result: dict = {}
    for cat in CATEGORIES:
        parent = cat.get("parent", "Sonstige")
        result.setdefault(parent, []).append(cat)
    return result