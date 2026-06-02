"""
WARP Tool - Fragenkatalog Daten

Beispieldaten basierend auf dem Wavestone Figma-Designs.
Kategorien orientieren sich an Testmanagement-Reifegradanalyse.

Erweitern: einfach neue Kategorien/Fragen anhaengen.
"""

CATEGORIES = [
    {
        "id": "stakeholder",
        "title": "Stakeholderbeziehung",
        "description": (
            "Bewertet die Qualitaet der Kommunikation und Zusammenarbeit "
            "zwischen Test-Team und Projekt-Stakeholdern."
        ),
        "questions": [
            {
                "id": "stk-1",
                "text": "Stakeholder werden regelmaessig ueber den Teststatus informiert.",
                "hint": "Wie haeufig finden Status-Updates statt?",
            },
            {
                "id": "stk-2",
                "text": "Es gibt einen definierten Eskalationsweg fuer kritische Testbefunde.",
                "hint": "Wer wird bei Blocker-Bugs informiert?",
            },
            {
                "id": "stk-3",
                "text": "Anforderungen werden vor Testbeginn mit dem Fachbereich abgestimmt.",
                "hint": None,
            },
            {
                "id": "stk-4",
                "text": "Testergebnisse werden in einem fuer Stakeholder verstaendlichen Format aufbereitet.",
                "hint": "z.B. Reports, Dashboards, Reifegradberichte",
            },
        ],
    },
    {
        "id": "testmanagement",
        "title": "Testmanagement",
        "description": (
            "Bewertet Strukturen, Prozesse und Werkzeuge zur Steuerung "
            "der Testaktivitaeten ueber den gesamten Lebenszyklus."
        ),
        "questions": [
            {
                "id": "tm-1",
                "text": "Es gibt ein dokumentiertes Testkonzept fuer das Projekt.",
                "hint": "Strategie, Scope, Methodik, Werkzeuge",
            },
            {
                "id": "tm-2",
                "text": "Testfaelle werden zentral verwaltet und sind versioniert.",
                "hint": None,
            },
            {
                "id": "tm-3",
                "text": "Die Testabdeckung wird gemessen und ausgewertet.",
                "hint": "Anforderungs- und Code-Coverage",
            },
            {
                "id": "tm-4",
                "text": "Es existiert ein definierter Prozess fuer das Fehlermanagement.",
                "hint": "Erfassung, Triage, Tracking, Schliessung",
            },
            {
                "id": "tm-5",
                "text": "Testressourcen (Personen, Umgebungen) werden geplant.",
                "hint": None,
            },
        ],
    },
    {
        "id": "testware",
        "title": "Testwaremanagement",
        "description": (
            "Es sorgt dafuer, dass die einzelnen Testprodukte zueinander "
            "und zu den zugehoerigen Entwurfsdokumenten passen."
        ),
        "questions": [
            {
                "id": "tw-1",
                "text": (
                    "Es gibt ein fuer das Testteam zugaengliches Versionsmanagement "
                    "fuer die Testobjekte/Anforderungen."
                ),
                "hint": "Versionsnummer und Name nachvollziehbar",
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
                "text": "Die Testfaelle beziehen sich jeweils auf eine Version/Dokument der Testbasis.",
                "hint": None,
            },
            {
                "id": "tw-4",
                "text": "Testfaelle und Anforderungen sind miteinander verknuepft.",
                "hint": "Ist der Weg von Anforderung zu Testfall zu Fehler nachvollziehbar?",
            },
        ],
    },
    {
        "id": "testkompetenz",
        "title": "Testkompetenz",
        "description": (
            "Bewertet das Wissen, die Erfahrung und die Weiterbildung "
            "der am Testprozess beteiligten Personen."
        ),
        "questions": [
            {
                "id": "tk-1",
                "text": "Tester verfuegen ueber eine fachliche und/oder technische Test-Ausbildung.",
                "hint": "z.B. ISTQB-Zertifizierung",
            },
            {
                "id": "tk-2",
                "text": "Testverantwortliche kennen die fachlichen Anforderungen detailliert.",
                "hint": None,
            },
            {
                "id": "tk-3",
                "text": "Es gibt regelmaessige Weiterbildungsmoeglichkeiten fuer das Testteam.",
                "hint": None,
            },
            {
                "id": "tk-4",
                "text": "Wissen wird im Team systematisch dokumentiert und geteilt.",
                "hint": "Wiki, Pairing, Reviews",
            },
        ],
    },
    {
        "id": "fehlermanagement",
        "title": "Fehlermanagement",
        "description": (
            "Erfassung, Bewertung und Nachverfolgung von Fehlern "
            "ueber den gesamten Lebenszyklus."
        ),
        "questions": [
            {
                "id": "fm-1",
                "text": "Es gibt ein Fehlermanagement inkl. Fehlerlebenszyklus, das dem Team bekannt ist.",
                "hint": None,
            },
            {
                "id": "fm-2",
                "text": "Regelmaessige Fehlerbesprechungen unterstuetzen das Fehlermanagement.",
                "hint": "z.B. Bug Triage Meetings",
            },
            {
                "id": "fm-3",
                "text": (
                    "Verantwortliche Personen im Fehlerprozess sind definiert "
                    "(Tester / Entwickler / Umgebungsmanager / Testmanager)."
                ),
                "hint": None,
            },
            {
                "id": "fm-4",
                "text": "Genutzte Fehlermanagementwerkzeuge sind fuer verantwortliche Personen nutzbar.",
                "hint": None,
            },
            {
                "id": "fm-5",
                "text": "Der Umgang mit Fehlernachtests (komplett/partiell) ist definiert.",
                "hint": None,
            },
            {
                "id": "fm-6",
                "text": (
                    "Die Mindestattribute jedes Fehlers sind: Ersteller / Tester / ID / "
                    "Datum / Schwere / Beschreibung / Titel / Status."
                ),
                "hint": "Erwartetes vs. tatsaechliches Ergebnis",
            },
        ],
    },
    {
        "id": "testautomatisierung",
        "title": "Testautomatisierung",
        "description": (
            "Reifegrad und Skalierung der automatisierten Testverfahren "
            "auf Unit-, Integrations- und End-to-End-Ebene."
        ),
        "questions": [
            {
                "id": "ta-1",
                "text": "Es gibt eine dokumentierte Strategie fuer die Testautomatisierung.",
                "hint": None,
            },
            {
                "id": "ta-2",
                "text": "Automatisierte Tests laufen in der CI/CD-Pipeline.",
                "hint": None,
            },
            {
                "id": "ta-3",
                "text": "Die Wartung der automatisierten Tests ist klar verantwortet.",
                "hint": None,
            },
            {
                "id": "ta-4",
                "text": "Der Anteil automatisierter Tests an Regressionstests wird gemessen.",
                "hint": None,
            },
        ],
    },
]


# Antwort-Optionen mit linearer Wertung wie vom Nutzer definiert
ANSWER_OPTIONS = [
    {"id": "voll",   "label": "Trifft voll zu",  "score": 100},
    {"id": "zu",     "label": "Trifft zu",       "score":  66},
    {"id": "kaum",   "label": "Trifft kaum zu",  "score":  33},
    {"id": "nicht",  "label": "Trifft nicht zu", "score":   0},
]


def total_question_count() -> int:
    return sum(len(c["questions"]) for c in CATEGORIES)
