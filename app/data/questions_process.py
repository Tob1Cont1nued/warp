"""
WARP Tool - Fragenkatalog Deployment-Prozess

Erhebt den Prozess von der Anforderungserhebung bis zum Deployment auf Produktion,
inklusive Testen auf Testumgebungen, Versionsständen und Abhängigkeiten zwischen
Systemen, Umgebungen und Schnittstellen. Grundlage für den Prozesszwilling.

Erweitern: einfach neue Kategorien/Fragen anhängen.
"""

CATEGORIES = [
    # =========================================================================
    # PHASE 1: ANFORDERUNGSERHEBUNG
    # =========================================================================
    {
        "id": "proc-anforderung",
        "title": "Anforderungserhebung",
        "parent": "Prozessphasen",
        "description": "Wie entstehen Anforderungen, wer verantwortet sie und wie gelangen sie in die Entwicklung?",
        "questions": [
            {
                "id": "proc-anf-1",
                "text": "Wer stellt Anforderungen und wer verantwortet deren Priorisierung?",
                "hint": "Nennen Sie die Rollen (Fachbereich, Product Owner, Auftraggeber) und deren Entscheidungsbefugnis.",
            },
            {
                "id": "proc-anf-2",
                "text": "Wie werden Anforderungen dokumentiert und versioniert?",
                "hint": "Tool oder Ablage, z.B. Jira, Confluence, Word-Dokumente auf einem Laufwerk.",
            },
            {
                "id": "proc-anf-3",
                "text": "Welche Schnittstellen zu anderen Systemen werden in der Anforderungsphase berücksichtigt?",
                "hint": "Gibt es ein Schnittstellenverzeichnis oder werden Schnittstellen erst in der Entwicklung geklärt?",
            },
            {
                "id": "proc-anf-4",
                "text": "Welche Abhängigkeiten zu anderen Teams, Projekten oder Umgebungen sind bekannt?",
                "hint": "Z.B. Datenlieferung durch ein Datawarehouse, gemeinsam genutzte Testumgebung, zeitliche Abhängigkeiten.",
            },
            {
                "id": "proc-anf-5",
                "text": "Wie wird geprüft, ob eine Anforderung testbar formuliert ist?",
                "hint": "Gibt es Akzeptanzkriterien, und wer prüft sie vor Freigabe in die Entwicklung?",
            },
            {
                "id": "proc-anf-6",
                "text": "Wie werden Änderungen an bereits freigegebenen Anforderungen behandelt?",
                "hint": "Gibt es einen Change-Prozess, und wer genehmigt ihn?",
            },
        ],
    },

    # =========================================================================
    # PHASE 2: ENTWICKLUNG
    # =========================================================================
    {
        "id": "proc-entwicklung",
        "title": "Entwicklung",
        "parent": "Prozessphasen",
        "description": "Wie wird entwickelt, wie wird Code geprüft und wie entsteht ein auslieferbares Artefakt?",
        "questions": [
            {
                "id": "proc-ent-1",
                "text": "Wie ist die Versionsverwaltung organisiert (Branching-Modell)?",
                "hint": "Z.B. Git mit feature-/dev-/main-Branches, Trunk-based, Release-Branches.",
            },
            {
                "id": "proc-ent-2",
                "text": "Wie entsteht aus einem Commit ein auslieferbares Artefakt (Build)?",
                "hint": "Automatisierter Build in einer Pipeline oder manuell? Wer triggert ihn?",
            },
            {
                "id": "proc-ent-3",
                "text": "Wie werden Code-Änderungen geprüft, bevor sie zusammengeführt werden?",
                "hint": "Code-Review, Pflicht-Approvals, automatisierte Checks in der Pipeline.",
            },
            {
                "id": "proc-ent-4",
                "text": "Wie ist die Build-Nummer bzw. Version eines Artefakts aufgebaut?",
                "hint": "Semantische Versionierung, Datum, Build-ID? Ist sie in der Anwendung sichtbar?",
            },
            {
                "id": "proc-ent-5",
                "text": "Welche Schnittstellen werden in der Entwicklung gegen welche Umgebungen getestet?",
                "hint": "Gibt es Mocks, Stubs oder werden echte Gegenstücke auf einer Entwicklungsumgebung genutzt?",
            },
            {
                "id": "proc-ent-6",
                "text": "Welche Artefakte gehören zu einem Release (Code, Konfiguration, Datenbankskripte, Dokumentation)?",
                "hint": "Gibt es eine Liste, was bei einem Release mitgeliefert werden muss?",
            },
        ],
    },

    # =========================================================================
    # PHASE 3: TESTEN (inkl. Deployment auf Testumgebungen)
    # =========================================================================
    {
        "id": "proc-testen",
        "title": "Testen und Deployment auf Testumgebungen",
        "parent": "Prozessphasen",
        "description": (
            "Welche Testumgebungen gibt es, wie kommt eine Version dorthin und welche Versionen "
            "liegen dort aktuell bereit, besonders wenn Systeme von anderen Umgebungen und Schnittstellen abhängen?"
        ),
        "questions": [
            {
                "id": "proc-tst-1",
                "text": "Welche Testumgebungen gibt es, und welche Stufen decken sie ab?",
                "hint": "Z.B. Entwicklung, Systemtest, Integrationstest, Abnahme. Welche davon sind gemeinsam genutzt?",
            },
            {
                "id": "proc-tst-2",
                "text": "Wie wird eine Version auf eine Testumgebung deployt?",
                "hint": "Manuell, über eine Pipeline oder durch einen Betrieb? Welche Schritte gehören dazu?",
            },
            {
                "id": "proc-tst-3",
                "text": "Wer entscheidet, welche Version auf welcher Testumgebung liegt?",
                "hint": "Gibt es eine Zuständigkeit für die Belegung der Umgebungen, oder einen Buchungskalender?",
            },
            {
                "id": "proc-tst-4",
                "text": "Ist nachvollziehbar, welche Version zu welchem Zeitpunkt auf einer Testumgebung lag?",
                "hint": "Gibt es ein Protokoll oder eine Übersicht der Deployments, und wo wird sie geführt?",
            },
            {
                "id": "proc-tst-5",
                "text": "Welche Systeme oder Schnittstellen muss eine Testumgebung zwingend erreichen können?",
                "hint": "Z.B. Datawarehouse, Authentifizierung, Partnersysteme. Wer betreibt diese Gegenstücke?",
            },
            {
                "id": "proc-tst-6",
                "text": "Was passiert, wenn ein benötigtes System oder eine benötigte Umgebung nicht verfügbar ist?",
                "hint": "Gibt es Ausweichlösungen wie Simulatoren oder verschobene Testfenster? Wer entscheidet darüber?",
            },
            {
                "id": "proc-tst-7",
                "text": "Welche Versionen auf den Testumgebungen müssen zueinander passen, damit ein Test aussagekräftig ist?",
                "hint": "Z.B. eine Schnittstelle, deren Gegenstück auf einer anderen Umgebung in einer bestimmten Version laufen muss.",
            },
            {
                "id": "proc-tst-8",
                "text": "Welche Testschritte werden nach jedem Deployment auf einer Testumgebung durchgeführt?",
                "hint": "Smoke-Test, Konfigurationsprüfung, Datenabgleich, automatisierte Regressionstests?",
            },
            {
                "id": "proc-tst-9",
                "text": "Wie werden Testergebnisse dokumentiert und an wen werden sie kommuniziert?",
                "hint": "Testmanagement-Tool, Testbericht, Statusrunde? Wer trifft die Entscheidung über den Testabschluss?",
            },
            {
                "id": "proc-tst-10",
                "text": "Wer vertritt die Testverantwortung, wenn die zuständige Person ausfällt?",
                "hint": "Gibt es eine benannte Vertretung, und ist sie mit den Umgebungen und Zugängen vertraut?",
            },
        ],
    },

    # =========================================================================
    # PHASE 4: FREIGABE
    # =========================================================================
    {
        "id": "proc-freigabe",
        "title": "Freigabe",
        "parent": "Prozessphasen",
        "description": "Welche Kriterien und Entscheider gibt es, bevor eine Version für Produktion freigegeben wird?",
        "questions": [
            {
                "id": "proc-frg-1",
                "text": "Welche Kriterien müssen erfüllt sein, damit ein Release freigegeben wird?",
                "hint": "Z.B. Testabschluss, offene Fehler nach Schweregrad, Abnahme durch den Fachbereich.",
            },
            {
                "id": "proc-frg-2",
                "text": "Wer gibt ein Release frei, und gibt es eine Vertretung für diese Rolle?",
                "hint": "Nennen Sie die Rolle und die Vertretungsregelung.",
            },
            {
                "id": "proc-frg-3",
                "text": "Wie wird eine Freigabe dokumentiert?",
                "hint": "Freigabeformular, Ticket, E-Mail? Wo wird sie abgelegt?",
            },
            {
                "id": "proc-frg-4",
                "text": "Welche Abhängigkeiten zu anderen Releases oder Teams müssen vor der Freigabe geklärt sein?",
                "hint": "Z.B. ein Partnersystem muss parallel ausgeliefert werden, oder ein Datenmodell muss vorher live sein.",
            },
            {
                "id": "proc-frg-5",
                "text": "Was passiert, wenn eine Freigabe verweigert wird?",
                "hint": "Wer entscheidet über das weitere Vorgehen, und gibt es einen definierten Ablauf?",
            },
        ],
    },

    # =========================================================================
    # PHASE 5: DEPLOYMENT AUF PRODUKTION
    # =========================================================================
    {
        "id": "proc-deployment",
        "title": "Deployment auf Produktion",
        "parent": "Prozessphasen",
        "description": "Wie wird eine freigegebene Version auf Produktion gebracht und wie wird ein Fehlschlag behandelt?",
        "questions": [
            {
                "id": "proc-dep-1",
                "text": "Welche Schritte umfasst das Deployment auf Produktion, in welcher Reihenfolge?",
                "hint": "Z.B. Datenbankmigration, Anwendung ausrollen, Konfiguration anpassen, Smoke-Test.",
            },
            {
                "id": "proc-dep-2",
                "text": "Welche Umgebungen und Systeme müssen beim Produktions-Deployment in einem bestimmten Zustand sein?",
                "hint": "Z.B. Schnittstellenpartner im Wartungsmodus, Datawarehouse-Ladelauf beendet.",
            },
            {
                "id": "proc-dep-3",
                "text": "Wer führt das Deployment durch, und wer ist während des Deployments erreichbar?",
                "hint": "Namen bzw. Rollen, Bereitschaft, Eskalationsweg.",
            },
            {
                "id": "proc-dep-4",
                "text": "Wie wird geprüft, dass das Deployment auf Produktion erfolgreich war?",
                "hint": "Automatisierte Prüfungen, manuelle Checks, welche Ergebnisse gelten als Erfolg?",
            },
            {
                "id": "proc-dep-5",
                "text": "Gibt es einen Rollback-Plan, und wie lange dauert ein Rollback?",
                "hint": "Ist ein Rollback für Datenbankänderungen überhaupt möglich?",
            },
            {
                "id": "proc-dep-6",
                "text": "Wann finden Deployments auf Produktion statt, und gibt es Sperrzeiten?",
                "hint": "Z.B. Freeze vor Monatsende, feste Wartungsfenster.",
            },
        ],
    },
]


def question_count() -> int:
    return sum(len(c["questions"]) for c in CATEGORIES)
