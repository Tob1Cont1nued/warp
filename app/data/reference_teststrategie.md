# Testautomations-Strategie – SAP-GUI / Playwright
SAP-GUI-Anwendungen | Playwright | CI/CD | Jira/XRAY

## 1. Management Summary

Diese Testautomations-Strategie beschreibt den Aufbau, die Governance und den technischen Rahmen für das automatisierte Testen und die Sicherstellung der Qualität der gelieferten Inkremente im Kontext eines SAFe-geführten, regulierten Umfelds (MaRisk, BaFin, DORA). Test und Qualitätssicherung liegen dabei vollständig in der Verantwortung der Feature-Teams (Payments Solution AddOn, Process_AddOn, TRBK Solution_AddOn) – es gibt weder eine zentrale QS- noch eine zentrale Testautomatisierungsinstanz. Die Strategie definiert, welche Ebenen der ISTQB-Testpyramide wie automatisiert werden, wie Playwright als primäres UI-Testframework eingesetzt wird, wie die Ausführung über GitHub Actions in die CI/CD-Pipeline eingebettet wird und wie Testfälle, Testergebnisse und Defects konsistent in Jira/XRAY verwaltet werden.

Kernziele:
- Kontinuierliche Reduktion der manuellen Regressionsaufwände über aufeinanderfolgende PI-Zyklen hinweg
- Etablierung einer stabilen, wartbaren Testpyramide mit klarer Verantwortlichkeitsverteilung innerhalb der Feature-Teams
- Volle Integration der Automatisierung in die bestehende SAFe-Kadenz (Sprint, PI, Release Train)
- Nachvollziehbare, auditfeste Testdokumentation als Nachweis für interne Revision und aufsichtsrechtliche Prüfungen (MaRisk AT 7.2, DORA Art. 24-27)
- Deutliche Verkürzung der Feedback-Zyklen durch parallele, gestufte Pipeline-Ausführung (Smoke → Regression → Full E2E)

## 2. Ziele, Geltungsbereich und Rahmenbedingungen

### 2.1 Geltungsbereich

Begriffsklärung: „SAP-GUI" bezeichnet in diesem Dokument ausschließlich browserbasierte Web-Oberflächen – nicht den klassischen SAP-GUI-Windows-Client mit Transaktionscodes. Innerhalb des Scopes kommen dabei zwei technisch unterschiedliche Web-Technologien zum Einsatz: überwiegend SAP GUI for HTML (WebGUI/NWBC im HTML-Modus – dieselbe Dynpro-Architektur wie der Windows-Client, nur als HTML gerendert) sowie ergänzend, in Teilen, Fiori/SAPUI5-Apps. Playwright automatisiert Browser-Inhalte und ist damit für beide Technologien technisch grundsätzlich einsetzbar; die konkrete Automatisierungsstrategie (Selektoren, Wrapper-Bibliothek, API-Testebene) unterscheidet sich jedoch deutlich zwischen WebGUI und Fiori und wird getrennt behandelt (Kapitel 5.1–5.5 für Fiori, Kapitel 5.6 für WebGUI). Für den klassischen SAP-GUI-Windows-Client (nicht im Browser) wäre Playwright nicht geeignet – dieser ist nach aktuellem Stand nicht Teil des Scopes.

Die Strategie gilt für alle browserbasierten SAP-Oberflächen (SAP GUI for HTML/WebGUI als überwiegender Anteil, Fiori Elements und Freestyle SAPUI5 ergänzend) sowie angrenzende Non-SAP-Webanwendungen innerhalb der betroffenen Wertschöpfungskette. Sie umfasst funktionale UI-Tests, API-/Service-Tests auf OData/REST-Ebene (soweit vorhanden) sowie deren Einbettung in bestehende End-to-End-Geschäftsprozessketten.

Die Umsetzung erfolgt dezentral durch drei Feature-Teams, die jeweils die volle Verantwortung für Test und Qualitätssicherung ihrer gelieferten Inkremente tragen:

| Team | Fachlicher Schwerpunkt |
|---|---|
| Payments Solution AddOn | Zahlungsverkehr-Add-On |
| Process_AddOn | Fachliche Prozesse/Anforderungen |
| TRBK Solution_AddOn | SAP Transactional Banking (TRBK) Add-On |

### 2.2 Regulatorischer Rahmen

Da die Anwendungen in einem bankaufsichtlich relevanten Umfeld betrieben werden, gelten zusätzliche Anforderungen an Nachvollziehbarkeit, Nachweisbarkeit und Änderungskontrolle:
- MaRisk AT 7.2 (Technisch-organisatorische Ausstattung): Testfälle und -ergebnisse müssen versioniert, nachvollziehbar und auditierbar dokumentiert werden
- DORA (Digital Operational Resilience Act): Anforderungen an Testing von IKT-Systemen, inkl. Nachweis regelmäßiger Testdurchführung und Nachverfolgung von Schwachstellen
- BaFin-Prüfungspraxis: Testabdeckung und Freigabeentscheidungen müssen im Vier-Augen-Prinzip dokumentiert sein (Trennung Ersteller/Freigeber)

Konsequenz für die Strategie: jede automatisierte Testausführung erzeugt einen persistenten, versionierten Bericht (Allure/HTML-Report + XRAY Test Execution), der mindestens so lange aufbewahrt wird, wie es die interne Aufbewahrungsrichtlinie vorsieht.

### 2.3 Abgrenzung
- Diese Strategie ersetzt kein manuelles exploratives Testen für neue, noch nicht stabile GUI-Anwendungen
- Last- und Performance-Tests werden hier nur als Schnittstelle referenziert, nicht im Detail spezifiziert (separate Performance-Test-Strategie)
- Sicherheitstests (SAST/DAST) sind Bestandteil einer separaten Security-Testing-Guideline

### 2.4 Abgrenzung zur Bundesbank: Quality-Gate-Modell

Die Abgrenzung orientiert sich am projektweiten Quality-Gate-Modell (QG1–QG4), wie es bereits im Testdatenkonzept festgelegt ist. Diese Testautomations-Strategie deckt ausschließlich die Phase bis QG1 ab:

| Phase | Verantwortung | Teststufen |
|---|---|---|
| Bis QG1 | SAP Fioneer (Scope dieser Strategie) | Entwickler-/Komponententests, Integrationstests, Systemtests |
| Ab QG2 | adesso + Bundesbank | DaMIT, SIT, UAT, Rehearsal in BBk-Umgebungen |

Ab QG2 übernehmen adesso und die Bundesbank die weiteren Teststufen in eigener Verantwortung und mit eigenen Prozessen; Automatisierungsentscheidungen für DaMIT, SIT, UAT und Rehearsal liegen außerhalb des Scopes dieser Strategie.

#### 2.4.1 Was wird übergeben?

Übergeben wird nicht die Automatisierung selbst (die Playwright-Suiten laufen nicht unverändert in BBk-Umgebungen weiter), sondern:
- Testfall-Dokumentation aus Jira/XRAY (Vorbedingungen, Schritte, Erwartungsergebnisse) als Wiederverwendungsgrundlage für SIT/UAT
- Requirement Coverage Report (Kapitel 7.4) als Freigabenachweis, dass bis QG1 ausreichend getestet wurde
- Die Traceability-Kette Requirement → Test → Execution → Defect als Nachweis Richtung Bundesbank/Revision

Nicht übergeben werden dürfen Testdaten mit Bezug zur Bundesbank – die synthetischen Testdaten-Bausteine (Kapitel 4.5.1) sind ausschließlich für die Phase bis QG1 bestimmt, analog zur bereits im Testdatenkonzept festgelegten Regel, dass keine anonymisierten oder pseudonymisierten BBk-Daten verwendet werden.

#### 2.4.2 Was wird wann automatisiert?
- Bis QG1: Automatisierungstiefe gemäß Testpyramide (Kapitel 3) und Kritikalitätsklasse (Kapitel 3.4) – so weit wie in dieser Strategie beschrieben
- Ab QG2 (DaMIT/SIT/UAT/Rehearsal): außerhalb des Automatisierungsscopes dieser Strategie; ob und wie adesso/Bundesbank dort automatisieren, liegt in deren eigener Verantwortung

## 3. Teststrategie nach der ISTQB-Testpyramide

Die Automatisierungsstrategie folgt konsequent dem Pyramidenprinzip: viele schnelle, isolierte Tests unten, wenige, aber aussagekräftige End-to-End-Tests oben. Dies verhindert die in SAPUI5-/GUI-Projekten häufig anzutreffende „Eistüten"-Antipattern-Form (kaum Unit-Tests, dafür eine überladene, brüchige UI-Testschicht).

### 3.1 Ebenen und Zielverteilung

| Ebene | Zielanteil | Werkzeuge | Verantwortlich | Ausführungsfrequenz |
|---|---|---|---|---|
| Unit Tests (SAPUI5-Controller, CDS-Views, Backend-Logik/ABAP-Unit) | ≈ 65–70 % | QUnit / OPA5-Unit, ABAP Unit, JavaScript Jest (für Non-UI5-Module) | Feature-Teams | Bei jedem Commit / Transportfreigabe |
| Integrations-/Komponententests (OData-Services, API-Contracts, CDS-Konsumtion) | ≈ 15–20 % | Playwright API-Testing (requestFixture), Postman/Newman als Fallback, ABAP Integrationstest | Feature-Teams | Bei jedem Merge in Feature-Branch |
| UI-/E2E-Tests (generative GUI-Frameworks & Freestyle-Apps, Geschäftsprozessketten) | ≈ 10–15 % | Playwright (Cross-Browser), Page-Object-Modell | Feature-Teams | Nightly + vor Release |
| Manuelle / explorative Tests (Usability, Edge Cases, neue Features) | Ergänzend, nicht quantifiziert | Manuell, Jira/XRAY Test Execution | Feature-Teams / Fachbereich | Sprintweise |

### 3.2 Kosten-, Geschwindigkeits- und Komplexitätsprofil

Der zentrale wirtschaftliche Grund für die Pyramidenform liegt im deutlichen Kosten- und Geschwindigkeitsgefälle zwischen den Ebenen: Ein Unit-Test ist isoliert, läuft in Millisekunden und benötigt keine Testdaten-Bausteine oder UI-Interaktion – ein manueller Fachtest hingegen bindet Personentage, erfordert eine vollständige Systemumgebung und ist entsprechend teuer, langsam und komplex in der Vorbereitung. (Im Originaldokument veranschaulicht eine Pyramiden-Grafik dieses Gefälle schematisch entlang der Testebenen – Kosten je Testfall und Ausführungsdauer/Komplexität steigen von Unit-Tests über Integration/API und UI-/E2E-Tests bis zu manuellen/explorativen Tests.)

Für die Automatisierungsstrategie folgt daraus: Jede fachliche Prüfung, die auch auf Unit- oder Integrationsebene abgesichert werden kann, sollte dort verortet werden – nicht weil die oberen Ebenen weniger wertvoll wären, sondern weil dieselbe Absicherung dort um ein Vielfaches günstiger und schneller zu erreichen ist. Die knappe, teure Kapazität für manuelle Fachtests und E2E-Automatisierung wird dadurch gezielt auf die Fälle konzentriert, die sich nicht weiter unten abbilden lassen (Cross-App-Navigation, echte Geschäftsprozessketten, Usability).

### 3.3 Warum diese Verteilung im SAP-GUI-Kontext wichtig ist

Viele SAP-GUI-Oberflächen sind naturgemäß volatil: OData-Metadaten, Annotationen und generative GUI-Generierung ändern sich häufig, ohne dass sich die fachliche Logik ändert. Eine Testautomatisierungsstrategie, die zu stark auf UI-Ebene setzt, führt zu hoher Wartungslast und sogenannten „Flaky Tests". Deshalb gilt:
- Fachliche Validierungslogik wird so weit wie möglich auf CDS-View- und Backend-Ebene über ABAP Unit abgesichert
- Playwright-Tests validieren bevorzugt Geschäftsprozessketten (mehrere Apps/Schritte) statt einzelne Feldvalidierungen, die bereits durch Unit-Tests abgedeckt sind
- UI-Selektoren erfolgen ausschließlich über stabile Attribute (siehe Kapitel 5.4), nicht über generierte GUI-IDs

### 3.4 Testarten-Matrix nach Business-Kritikalität

| Kritikalitätsklasse | Beispiel-Prozesse | Automatisierungstiefe | Regressionsfrequenz |
|---|---|---|---|
| Klasse A – Kritisch (regulatorisch/finanziell) | Kreditvergabeprozess, Meldewesen-Reports, Zahlungsverkehr-Freigaben | Vollständige E2E-Automatisierung + Unit + Integration, Vier-Augen-Nachweis | Bei jedem Release + nightly |
| Klasse B – Wichtig (Kernprozesse) | Kundenstammdaten-Pflege, Dokumentenmanagement, Antragserfassung | E2E für Haupt-Happy-Path, Unit/Integration vollständig | Wöchentlich + vor Release |
| Klasse C – Unterstützend | Reporting-Dashboards, interne Verwaltungs-Apps | Smoke-Test E2E, Unit-Fokus | Vor Release |

## 4. Playwright-Testautomatisierungs-Framework

### 4.1 Warum Playwright für SAP-GUIs

Playwright wurde gegenüber Alternativen (wpi5/OPA5 End-to-End, Selenium, Cypress) aus folgenden Gründen als strategisches Werkzeug für die UI-Automatisierungsebene gewählt:
- Native Auto-Waiting: reduziert Flakiness bei asynchronem OData-Laden in generativen GUI-Frameworks deutlich gegenüber expliziten Sleep/Wait-Konstrukten
- Cross-Browser-Unterstützung (Chromium, Firefox, WebKit) in einer API – relevant, da einige Fachbereiche Edge/Chromium-basiert arbeiten, andere Safari (WebKit-Engine) auf iPad-Kiosk-Geräten
- Eingebautes Tracing, Video-Recording und Screenshot-on-Failure – zentral für Nachvollziehbarkeit im regulierten Kontext
- Parallelisierung nativ über Worker, deutlich schneller in der CI-Pipeline als sequentielle Selenium-Grids
- Request-Interception erlaubt gezieltes Mocken einzelner OData-Calls für Randfälle, ohne das gesamte Backend zu stubben
- Gute TypeScript-Unterstützung – ermöglicht typsichere Page Objects analog zur bestehenden Entwicklungspraxis

### 4.2 Architektur: Page-Object-Modell (POM) mit GUI-Erweiterung

Da Standard-POM auf klassischen Webseiten aufbaut, wird es um eine zusätzliche Abstraktionsschicht erweitert, die typische GUI-Elemente kapselt (Smart Table, Object Page, Value Help Dialog, Message Toast/Popover):

| Schicht | Inhalt | Beispiel |
|---|---|---|
| Test Specs (*.spec.ts) | Testfälle, fachliche Assertions, keine Selektoren | „Antrag anlegen und zur Freigabe senden" |
| Page Objects (*.page.ts) | App-spezifische Seiten/Views, kapseln GUI-Kontrollen | AntragErfassenPage, AntragFreigabePage |
| GUI Control Wrappers | Wiederverwendbare Wrapper für generische GUI-Kontrollen | SmartTable, ObjectPageWrapper, ValueHelpDialog, MessageToast |
| Fixtures / Test Setup | Playwright-Fixtures für Login (SAML/IAS), Testdaten-Setup, API-Vorbereitung | authenticatedPage-Fixture, testDataFixture |
| Utilities | OData-Helper, Datumsformatierung, Wartehilfen für UI5-Busy-Indicator | waitForUI5BusyIndicatorGone() |

#### 4.2.1 Beispielstruktur des Repositories

```
playwright-tests/
  tests/     → Spec-Dateien, gruppiert nach Fachdomäne (kredit/, zahlungsverkehr/, stammdaten/)
  pages/     → Page Objects je GUI-Anwendung
  fixtures/  → Playwright-Fixtures (Auth, Testdaten, API-Clients)
  controls/  → GUI-Control-Wrapper-Bibliothek (SmartTable, ObjectPage, ValueHelp …)
  utils/     → Hilfsfunktionen (Wartelogik, Datenaufbereitung, Reporting-Helper)
  config/    → playwright.config.ts, Umgebungs-Konfigurationen (DEV/QA/PreProd)
  reporters/ → Custom Reporter für XRAY-Anbindung
```

### 4.3 Selektorstrategie

Generative GUI-Frameworks generieren IDs dynamisch und nicht deterministisch über Deployments hinweg. Deshalb gilt als verbindlicher Standard:
- Priorität 1: data-testid-Attribute, die von den Feature-Teams gezielt in Custom-Controls/Fragmenten ergänzt werden
- Priorität 2: stabile ARIA-Rollen und zugängliche Namen (getByRole, getByLabel) – zusätzlicher Nutzen: verbessert gleichzeitig die Accessibility-Qualität der App
- Priorität 3: kontrollspezifische Bindungspfade (z. B. OData-Property-Namen) über Custom-Locator-Utilities
- Nicht zulässig: automatisch generierte UI5-IDs (z. B. __component0---idAntrag--...) oder rein positionsbasierte XPath-Selektoren

### 4.4 Umgang mit UI5-spezifischer Asynchronität

Ein zentraler Baustein der Framework-Stabilität ist eine gemeinsame Wartebibliothek, die den UI5-Busy-Indicator sowie ausstehende OData-Batch-Requests berücksichtigt, bevor eine Aktion ausgeführt wird. Dadurch wird die Notwendigkeit von statischen Wartezeiten vollständig eliminiert und die Flaky-Test-Rate signifikant gesenkt.

### 4.5 Testdatenmanagement

Das Testdatenmanagement folgt dem unternehmensweiten Testdatenkonzept und wird für die Playwright-Automatisierung konkretisiert. Leitprinzip ist ein Synthetic-First-/Baustein-Ansatz: Testdaten werden nicht als vorgelagerte, lose Datenbestände verstanden, sondern als wiederverwendbare, ausführbare Bausteine, die Bestandteil des jeweiligen Testfalls sind.

#### 4.5.1 Synthetic-First-Prinzip
- Es werden ausschließlich synthetische, template-basierte oder generatorbasiert erzeugte Testdaten verwendet – keine anonymisierten oder pseudonymisierten Produktions-/Kundendaten, auch nicht auszugsweise
- Dies gilt insbesondere für QA-/Integrationsumgebungen bis zur Freigabe für PreProd (vgl. Umgebungsstrategie, Kapitel 6.4) und erfüllt zugleich DSGVO- und bankaufsichtliche Anforderungen
- Für Massen-/Volumendaten (Performance-Vorbereitung, NFT-nahe Smoke-Checks) wird auf einen Mass-Data-Generator-Mechanismus zurückgegriffen, der aus einem kleinen, fachlich korrekten Referenzbestand realistische Volumina erzeugt

#### 4.5.2 Testdaten-Bausteine als Vorbedingung von Playwright-Tests

Analog zum Bausteinmodell des Testdatenkonzepts wird jede Precondition eines Playwright-Tests als ausführbarer, wiederverwendbarer Baustein modelliert statt als statischer Datenzustand:
- Ein Testdaten-Baustein ist eine parametrisierbare Setup-Funktion (z. B. createBusinessPartner(), createAccount(), createStandingOrder()), die über die OData-/API-Fixture (siehe Kapitel 4.5.4) ausgeführt wird – nicht über die UI
- Playwright-Tests referenzieren in ihrem Setup ausschließlich vorhandene Bausteine; das Anlegen oder Ändern von Testdaten ist damit selbst Teil des Testfalls und wird ebenso versioniert wie der eigentliche Testschritt
- Beispiel Klasse-A-Prozess „SEPA-Zahlungsausgang": Preconditions createBusinessPartner → createAccount (Quellkonto) → createAccount/Empfängerdaten → seedBalance, gefolgt vom eigentlichen Playwright-Testschritt (Zahlung erfassen/ausführen) und der Ergebniskontrolle (Buchung, Status, Logs)

#### 4.5.3 Bausteinkatalog und Reuse-First
- Vor der Implementierung eines neuen Bausteins ist verpflichtend zu prüfen, ob ein bestehender Baustein wiederverwendet oder durch Parametrisierung angepasst werden kann (Reuse-First-Prinzip) – analysiert wird pro Testfall, nicht vorab für alle Anforderungen
- Der Bausteinkatalog wird zentral gepflegt und in Jira/XRAY über die Precondition-Verknüpfung des jeweiligen Tests referenziert, sodass Testfall Owner bestehende Bausteine direkt im Testmanagement-Tool auffinden
- Fehlt ein passender Baustein, wird dies wie im Testdatenkonzept über einen Baustein Change Request (BCR) angefordert (Zielsystem, fachlicher Bedarf, erwartete Inputs/Outputs, Kritikalität) – entschieden wird bevorzugt für Wiederverwendung vor Erweiterung vor Neuerstellung; Einmal-Skripte sind die Ausnahme
- Jeder Baustein gilt erst als „Done", wenn Zweck, Parameter, Outputs, Wiederholbarkeit (Idempotenz) sowie Logging/Audit-Trail dokumentiert und durch eine Smoke-Validierung nachgewiesen sind

#### 4.5.4 Ausführung, Isolation und Reset-/Refresh-Strategie
- Bausteine werden über dedizierte API-Fixtures vor Testausführung ausgeführt (Given-Setup über OData/REST, nicht über die UI) und – soweit fachlich sinnvoll – nach Testende wieder bereinigt (Teardown)
- Namensräume, Nummernkreise und Idempotenzregeln je Baustein stellen sicher, dass parallele Pipeline-Worker/Shards (Kapitel 6.2) keine Datenkollisionen erzeugen
- Für Klasse-A-Prozesse existieren zusätzlich stabile, versionierte Referenz-Datensätze in einem dedizierten QA-Mandanten, die durch keinen automatisierten Lauf verändert werden dürfen; eine Reset-/Refresh-Strategie stellt die Wiederholbarkeit der Baseline Regression Suite (Kapitel 4.5.5) nach jedem Release sicher

#### 4.5.5 Baseline Regression Suite (Happy Flow)

Analog zum projektweiten Testdatenkonzept wird die Playwright-Vollregression (Stufe 5, Kapitel 6.1) um eine stabile Kernsuite ergänzt, die die zentralen Geschäftsprozessketten mit Bausteinen absichert, bevor Fehler-/Randfälle automatisiert werden. Fehler- und Sonderfälle werden bewusst erst als zweiter Schritt automatisiert, um zunächst eine belastbare Basis zu schaffen.

#### 4.5.6 Massendaten und Volumen-Testdaten (Schnittstelle zu Performance-Tests)
- Für Last-, Volumen- und Performance-Vorbereitung werden versionierte Volume Data Sets (klein/mittel/groß) über den Mass-Data-Generator-Mechanismus aufgebaut; die eigentliche Durchführung ist Gegenstand der separaten Performance-Test-Strategie
- Playwright-seitig wird nur ein schlanker Smoke-Check gegen ein solches Volumen-Set gefahren, um sicherzustellen, dass die GUI-Anwendungen bei realistischer Datenlast funktional stabil bleiben (z. B. Ladezeiten von Smart Tables, Paging-Verhalten)

#### 4.5.7 Governance

Rollen und Freigabeprozess für Testdaten-Bausteine folgen dem projektweiten Testdatenkonzept und sind auf die RACI-Matrix dieses Dokuments (Kapitel 8.1) abgebildet: Da keine zentrale Testautomatisierungsinstanz existiert, übernimmt jedes Feature-Team die Rolle des Baustein Maintainers für die von ihm verantworteten Bausteine (Implementierung, Wiederholbarkeit, Logging). Übergreifende Standards und der gemeinsame Bausteinkatalog werden durch den Testmanager als Test Data Owner koordiniert, gemeinsam mit dem Fachbereich als Domain Data Owner sowie den jeweils betroffenen Feature-Teams.

#### 4.5.8 Zeitbezogene Testdaten (Time Travel Testing)

Ein Teil der Geschäftsprozesse ist explizit datums-/zeitabhängig (Zinsberechnung, Monats-/Quartals-/Jahresabschluss, Vertrags- und Produktlaufzeiten, Ausführungsrhythmen von Daueraufträgen, regulatorische Meldestichtage). Ohne gezielte Zeitsimulation lassen sich solche Szenarien nur durch tatsächliches Warten auf den realen Kalendertag verifizieren – das ist für eine kontinuierliche Pipeline nicht praktikabel. Dieses Konzept unterscheidet daher zwei Ebenen, die beide an das bestehende Bausteinmodell andocken, statt ein separates Testdatenkonzept zu etablieren:
- Fachliche Stichtag-Parametrisierung: Testdaten-Bausteine (z. B. createStandingOrder(), createContract()) erhalten einen optionalen asOfDate-/Stichtag-Parameter
- Echte Zeitsimulation für Batch-/EOD-Prozesse: Zinsläufe, Abschlussverarbeitung und terminierte Hintergrundjobs benötigen eine dedizierte, isolierte Zeitverschiebung (separater Testmandant mit verschobenem Systemdatum, oder Virtual-Clock-Werkzeug)
- Isolationsgebot: Zeitverschobene Läufe finden ausschließlich in einem eigens dafür vorgesehenen Testmandanten statt, niemals im gemeinsam genutzten QA-/Integrationsmandanten
- Erweiterung der Volume Data Sets um eine zeitliche Achse (z. B. VDS „Monatsultimo", „Quartalsultimo")
- Versionierte Zeitpunkt-Snapshots für wiederkehrende Abschluss-Szenarien als eigene, restaurierbare Bausteine

## 5. SAP-GUI-spezifische Testaspekte

### 5.1 Generatives GUI-Framework vs. Freestyle SAPUI5

| Aspekt | Generatives GUI-Framework | Freestyle SAPUI5 |
|---|---|---|
| Testansatz | Fokus auf Konfigurations-/Annotationsvalidierung + Prozessfluss | Vollständige funktionale Testabdeckung inkl. Custom-Controller-Logik |
| Selektor-Risiko | Hoch bei generierten IDs → zwingend data-testid via Fragment-Erweiterung | Mittel, da Controller-Code steuerbar ist |
| Typische Fehlerquellen | Annotation-Änderungen, Value-Help-Konfiguration, Draft-Handling | Custom-Event-Handling, Fragmenteinbindung, manuelle Validierungen |
| Regressionsrisiko bei OData-Änderungen | Sehr hoch – jede Annotation-Änderung kann UI beeinflussen | Mittel |

### 5.2 GUI-Launchpad und Cross-App-Navigation

Da viele Geschäftsprozesse app-übergreifend über den GUI-Launchpad navigieren (Intent-based Navigation), werden E2E-Tests explizit so konzipiert, dass sie reale Navigationsketten abbilden statt jede App isoliert über eine direkte URL zu starten. Dies deckt Fehler in der Launchpad-Konfiguration (Semantic Objects, Navigation Targets, Rollen-Berechtigung im Katalog) ab, die isolierte App-Tests systematisch übersehen würden.

### 5.3 Authentifizierung in Testumgebungen
- SAML/SAP-IAS-basierte Anmeldung wird über eine wiederverwendbare Playwright-Fixture gelöst, die einen authentifizierten Storage-State (storageState) einmal pro Testlauf erzeugt und für alle Tests wiederverwendet – das spart signifikant Ausführungszeit gegenüber Login-per-Test
- Für Klasse-A-Prozesse mit rollenbasierter Freigabe (Vier-Augen-Prinzip) existieren separate technische Testnutzer je Rolle (Ersteller, Prüfer/Genehmiger), deren Berechtigungen genau den produktiven Rollenprofilen entsprechen

### 5.4 Umgang mit generierten IDs und Annotationsänderungen (Wartungsstrategie)
- Verbindliche Entwicklungsrichtlinie: jedes neue Custom-Fragment erhält data-testid-Attribute auf allen interaktiven Elementen (Pflicht im Definition of Done der Feature-Teams)
- Änderungen an CDS-Annotationen, die UI-relevante Strukturen betreffen, lösen automatisch eine Kennzeichnung der betroffenen Testfälle in Jira zur Re-Validierung aus (siehe Kapitel 7.4 Traceability)
- Quartalsweises „Selector Health Check": automatisiertes Skript prüft alle Page Objects auf Verwendung nicht zulässiger Selektortypen und erzeugt einen technischen Schuldenbericht

### 5.5 OData-/API-Ebene als eigenständige Testschicht

Soweit Fiori-Apps betroffen sind, die auf OData V2/V4-Services aufsetzen, wird die Service-Schicht getrennt von der UI getestet:
- Contract-Tests prüfen Metadaten-Konsistenz (Entity-Typen, Navigation-Properties) gegen ein versioniertes Referenzschema, um Breaking Changes frühzeitig zu erkennen
- Playwright APIRequestContext wird für funktionale Service-Tests genutzt (CRUD-Operationen, Draft-Handling, Aktionen/Functions Imports), unabhängig von der UI-Rendering-Zeit
- Diese Schicht liefert deutlich schnelleres Feedback (Sekunden statt Minuten) und deckt fachliche Logikfehler ab, bevor teure E2E-Läufe gestartet werden

Für SAP GUI for HTML (WebGUI) existiert diese Testschicht in der Regel nicht (siehe Kapitel 5.6) – hier fehlt der Fiori-typische OData-Layer, sodass Integrationstests dort primär auf Ebene der Dynpro-/RFC-Postbacks bzw. direkt gegen die ABAP-Backend-Logik erfolgen.

### 5.6 SAP GUI for HTML (WebGUI/NWBC): abweichende Testaspekte

Ein wesentlicher Teil des Scopes läuft über SAP GUI for HTML bzw. NWBC im HTML-Modus – technisch dieselbe Dynpro-Architektur wie der klassische SAP-GUI-Windows-Client, lediglich im Browser gerendert. Da diese Bildschirme SAP-generiert und nicht wie Fiori-Apps individuell entwickelt werden, gelten mehrere wichtige Abweichungen:
- Keine data-testid-Möglichkeit: Selektoren müssen sich auf die von SAP vergebenen Feld-/Element-IDs stützen, die über Support-Packages und Releases hinweg weniger stabil sein können als bei Fiori
- Keine Fiori-Elements-Wrapper-Bibliothek: für WebGUI ist eine eigene, schlankere Wrapper-Schicht für klassische Dynpro-Bedienelemente vorzusehen
- Keine OData-/API-Testebene: WebGUI-Bildschirme kommunizieren über klassische Dynpro-Postbacks; Integrationstests laufen näher an ABAP-Unit- bzw. Transport-Ebene
- Andere Navigationslogik: klassischer Transaktionscode-Wechsel und Dynpro-Screen-Sequenzen statt Fiori-Launchpad-Navigation
- Playwright bleibt technisch einsetzbar, da WebGUI im Browser läuft – der Automatisierungsaufwand pro Testfall ist jedoch tendenziell höher

## 6. CI/CD-Integration mit GitHub Actions

### 6.1 Pipeline-Philosophie: Shift-Left mit gestuften Qualitätstoren

Die Pipeline ist in aufeinander aufbauende Stufen gegliedert, sodass teure, langsame Tests erst ausgeführt werden, wenn günstigere, schnellere Prüfungen erfolgreich waren („Fail Fast"). Dies reduziert Wartezeiten für die Feature-Teams und Rechenkosten in der CI-Infrastruktur.

| Stufe | Trigger | Inhalt | Ziel-Laufzeit | Blockierend für |
|---|---|---|---|---|
| 1. Lint & Static Checks | Jeder Push / Pull Request | ESLint, TypeScript-Compile-Check, ABAP-Code-Inspector-Regeln | < 3 Min | Merge in Feature-Branch |
| 2. Unit Tests | Jeder Push / Pull Request | QUnit/OPA5-Unit, ABAP Unit, Jest | < 8 Min | Merge in Feature-Branch |
| 3. Integration/API-Tests | Merge in develop/Integrationsbranch | Playwright API-Tests gegen OData-Services (Testmandant) | < 12 Min | Deployment in QA-Umgebung |
| 4. Smoke E2E (Playwright) | Nach Deployment in QA-Umgebung | Kritischer Happy-Path je Klasse-A-Prozess | < 15 Min | Freigabe für weitere QA-Tests |
| 5. Vollregression E2E (Playwright) | Nightly + vor jedem Release-Kandidaten | Vollständige Testsuite aller Klassen A/B, Smoke für Klasse C | 45–90 Min (parallelisiert) | Release-Freigabe |
| 6. Reporting & XRAY-Sync | Nach jedem Pipeline-Lauf | Allure-/HTML-Report-Erzeugung, automatischer Import als XRAY Test Execution | < 5 Min | Nachweisdokumentation |

#### 6.1.1 Auslösemechanismen: Git-basiert vs. Transportbasiert (ABAP-Backend)

Die Trigger „Jeder Push / Pull Request", „Merge in Feature-Branch" gelten unmittelbar nur für den Anteil, der tatsächlich in Git verwaltet wird – also Frontend (Fiori/SAPUI5) und Playwright-Testsuiten. Für die ABAP-Backend-Entwicklung trifft dies nicht automatisch zu, sofern klassisch über das SAP-Transportwesen statt über gCTS gearbeitet wird. Für diesen Fall gilt ein separater, ABAP-nativer Auslösemechanismus:
- Unit-Tests (ABAP Unit): Auslöser ist die Transportfreigabe im Entwicklungssystem
- Integrations-/API-Tests gegen OData-Services: Auslöser ist der Transportimport in das Konsolidierungs-/Testsystem
- Beide Auslösewege münden unabhängig voneinander in dieselbe Jira/XRAY-Traceability

#### 6.1.2 Vorgeschlagener Auslösemechanismus für den Transport-Trigger

Da ein SAP-seitiger Push-Mechanismus zusätzliche ABAP-Eigenentwicklung erfordern würde und der Restriktion gegen ausgehende Kommunikation widerspricht, wird ein Pull-/Bridge-Ansatz vorgeschlagen, der ausschließlich lesende Standard-Schnittstellen nutzt:
- Polling-Baustein (systematisches Sicherheitsnetz): ein zeitgesteuerter Workflow fragt regelmäßig über eine lesende RFC-/OData-Standardschnittstelle ab, ob neue Transporte freigegeben/importiert wurden
- Jira-Bridge (schnellerer Pfad): eine Jira-Automation-Regel reagiert auf einen Statuswechsel und löst den passenden Workflow aus
- Empfohlene Kombination: Polling als durchgängiges Sicherheitsnetz, ergänzt um die Jira-Bridge als schnelleren Pfad

### 6.2 GitHub-Actions-Workflow-Aufbau (Beispiel)

Playwright-Spezifikationen liegen bewusst dezentral je Fiori-App/-Repository und nicht in einem zentralen Playwright-Testrepository, um keine zentrale Testautomatisierungsinstanz wieder einzuführen. Konsistenz zwischen den Repositories wird über gemeinsame, zentral gepflegte Bausteine sichergestellt:
- Zentrales Repository „testautomation-shared-workflows" enthält wiederverwendbare .github/workflows/*.yml-Bausteine (playwright-smoke.yml, playwright-regression.yml, xray-sync.yml); Pflege gemeinsam durch die drei Feature-Teams über reguläre Pull Requests
- App-Repositories referenzieren diese Bausteine via workflow_call, versioniert über Tags
- Matrix-Strategie für Cross-Browser-Ausführung (Chromium/WebKit) und Sharding zur Parallelisierung
- Self-hosted Runner in der internen Netzwerkzone, da die QA-/PreProd-SAP-Systeme nicht öffentlich erreichbar sind
- Secrets ausschließlich über GitHub Environments mit Required Reviewers für produktionsnahe Umgebungen
- Artefakte (Traces, Videos, Screenshots bei Fehlschlag) werden als Workflow-Artifacts mit definierter Aufbewahrungsfrist (mind. 90 Tage) gespeichert

### 6.3 Quality Gates und Merge-Regeln
- Branch-Protection auf main/develop: Stufe 1 und 2 müssen grün sein, sonst kein Merge möglich
- Required Status Checks zusätzlich für Integrationsbranches: Stufe 3 muss erfolgreich sein
- Release-Kandidaten benötigen zusätzlich eine grüne Vollregression sowie eine manuelle Freigabe vor Deployment in PreProd/Produktion – erfüllt das Vier-Augen-Prinzip auf technischer Ebene
- Bei Testfehlschlägen in Stufe 4/5 wird automatisch ein Jira-Bug mit vorbefülltem Kontext über die XRAY-API erzeugt

### 6.4 Umgebungsstrategie

| Umgebung | Zweck | Testtiefe | Datenbasis |
|---|---|---|---|
| DEV | Entwicklerlokal / Feature-Branch | Unit + gezielte Playwright-Einzeltests | Synthetische Minimal-Daten |
| QA/Integration | Kontinuierliche Integration aller Feature-Branches | Integration + Smoke E2E | Stabile synthetische Referenzdaten |
| PreProd/Staging | Release-Kandidaten-Validierung, produktionsnahe Konfiguration | Vollregression E2E | Anonymisierte, produktionsnahe Datenstruktur |
| Produktion | Nur Monitoring/Synthetic Checks nach Go-Live | Read-only Smoke-Checks (kein Datenschreibvorgang) | Produktivdaten (keine Testschreibungen) |

## 7. Testmanagement-Integration mit Jira und XRAY

Da bereits Jira, XRAY und Confluence als zentrale Werkzeuge etabliert sind, baut diese Strategie direkt darauf auf, statt ein Parallelsystem einzuführen.

### 7.1 Struktur in Jira/XRAY

| Jira/XRAY-Objekt | Zweck | Verknüpfung |
|---|---|---|
| Test (Issue-Typ „Test") | Einzelner Testfall (manuell oder automatisiert), inkl. Testschritten oder Cucumber-Gherkin-Referenz | Verlinkt mit User Story/Feature via „Tests"-Link |
| Test Set | Bündelung thematisch zusammengehöriger Tests | Zuordnung zu Epic/Fachdomäne |
| Precondition | Wiederverwendbare Vorbedingungen | Verlinkt mit mehreren Tests |
| Test Plan | Release- oder PI-bezogene Zusammenstellung aller relevanten Test Sets | Verlinkt mit Fix Version / PI |
| Test Execution | Konkreter Ausführungslauf (manuell oder automatisiert importiert) | Automatisch erzeugt aus GitHub-Actions-Pipeline-Lauf |
| Bug | Automatisch erzeugter Defect bei Testfehlschlag | Verlinkt mit Test und Test Execution, referenziert Trace-Artefakt |

### 7.2 Automatisierte Testfälle: Kennzeichnung und Pflege
- Jeder automatisierte Playwright-Test erhält im Testcode ein Tag mit der zugehörigen XRAY-Test-Key (z. B. @XRAY-T1234)
- Neue Testfälle werden zunächst in Jira/XRAY als Test-Issue angelegt (fachliche Spezifikation, Schritte, Erwartungsergebnis), bevor die technische Automatisierung erfolgt
- Der XRAY-Test-Typ wird auf „Automated" gesetzt, mit Verweis auf den Generic-Test-Definition-Eintrag

### 7.3 Automatischer Ergebnis-Import (XRAY-API)

Nach jedem Pipeline-Lauf übernimmt ein dedizierter Schritt in GitHub Actions:
- Import des JUnit-/Cucumber-Ergebnisformats aus Playwright direkt als neue Test Execution
- Verknüpfung der Execution mit dem auslösenden Commit/PR sowie dem Pipeline-Run-Link
- Automatische Erstellung eines Bug-Issues bei „Failed"-Status inkl. Screenshot, Video und Trace-Datei
- Bei wiederholtem Fehlschlag desselben Tests (Flaky-Verdacht) wird statt eines neuen Bugs ein Kommentar am bestehenden Bug ergänzt und das Test-Issue mit dem Label „flaky-review" versehen

### 7.4 Traceability und Impact-Analyse

Die durchgängige Verlinkung Requirement → Test → Execution → Defect ermöglicht eine vollständige Rückverfolgbarkeit:
- Requirement Coverage Report zeigt je User Story/Feature den Automatisierungsgrad und letzten Ausführungsstatus
- Bei Änderungen an CDS-Annotationen/OData-Services identifiziert ein Abgleichsskript betroffene Test-Issues und setzt das Label „re-validate"
- Traceability-Reports werden pro PI als Confluence-Seite exportiert und archiviert

### 7.5 Defect-Management-Prozess (Kurzfassung)

Automatisiert erzeugte Bugs durchlaufen denselben Workflow wie manuell gefundene Defects (Triage → Priorisierung → Bearbeitung → Verifikation durch erneuten Pipeline-Lauf → Schließung), mit dem Unterschied, dass die Verifikation durch einen erneuten automatisierten Testlauf statt manueller Nachtestung erfolgt.

## 8. Rollen, Verantwortlichkeiten und Governance

### 8.1 RACI-Übersicht

Da es keine zentrale QS- oder Testautomatisierungsinstanz gibt, führt die RACI-Matrix „Entwicklungsteam" und „Testautomatisierungsteam" in einer gemeinsamen Spalte „Feature-Team" zusammen:

| Aktivität | Feature-Team | Testmanager | Fachbereich/Product Owner |
|---|---|---|---|
| Unit-Tests schreiben & pflegen | R/A | I | I |
| Playwright-E2E-Tests erstellen | R/A | C | C |
| Fachliche Testfallspezifikation (Jira/XRAY) | C | A | R |
| CI/CD-Pipeline-Wartung | R (gemeinsam, alle drei Feature-Teams) | A | I |
| Testdatenmanagement | R | A | C |
| Freigabe Release-Kandidat (Vier-Augen) | I | R | A |
| Traceability-/Coverage-Reporting | R | A | I |
| Flaky-Test-Triage | R/A | I | I |

R = Responsible, A = Accountable, C = Consulted, I = Informed

### 8.2 Testverantwortung in den Feature-Teams

Es gibt bewusst kein hybrides Modell mit zentralem Testautomatisierungsteam: Test und Qualitätssicherung der gelieferten Inkremente liegen vollständig in der Verantwortung der drei Feature-Teams. Jedes Team durchläuft die gesamte Testpyramide für den eigenen Verantwortungsbereich (Shift-Left-Prinzip, kurze Feedback-Zyklen, volle Ende-zu-Ende-Verantwortung für die eigene Lieferqualität). Ein teamübergreifendes Gremium existiert nicht; Abstimmung erfolgt bilateral bzw. über den Testmanager als übergreifende Rolle für Standardsetzung und Konfliktlösung.

### 8.3 Definition of Done – Ergänzungen
- Jede neue User Story mit UI-Anteil enthält verpflichtend data-testid-Attribute auf allen neuen interaktiven Elementen
- Jede User Story der Kritikalitätsklasse A/B ist erst „Done", wenn der zugehörige Playwright-Test in der Pipeline grün läuft (nicht nur im PR-Review verifiziert)
- Kein Merge in den Release-Branch ohne aktualisierte XRAY-Test-Verknüpfung

## 9. Metriken, Reporting und kontinuierliche Verbesserung

### 9.1 Kern-KPIs

| KPI | Definition | Zielwert | Berichtsfrequenz |
|---|---|---|---|
| Automatisierungsgrad | Anteil automatisiert ausgeführter Testfälle an Gesamttestfällen je Kritikalitätsklasse | ≥ 90 % Klasse A, ≥ 70 % Klasse B | Pro PI |
| Pipeline-Erfolgsquote | Anteil grüner Vollregressionsläufe ohne manuelles Eingreifen | ≥ 95 % | Wöchentlich |
| Flaky-Test-Rate | Anteil Tests mit inkonsistentem Ergebnis bei identischem Code-Stand | < 3 % | Monatlich |
| Mean Time to Detect (MTTD) | Zeit zwischen Codeänderung und automatisierter Fehlererkennung | < 24 Stunden für Klasse A | Monatlich |
| Testlaufzeit Vollregression | Gesamtdauer der Stufe-5-Pipeline | < 90 Minuten | Pro Lauf |
| Requirement Coverage | Anteil Requirements mit mindestens einem verlinkten, aktuellen Test | 100 % Klasse A/B | Pro PI |

### 9.2 Reporting-Kadenz im SAFe-Kontext
- Sprint Review: Kurzstatus Automatisierungsfortschritt neuer Stories als Teil des Team-Demo-Berichts
- PI-Planning-Vorbereitung: Coverage- und Flaky-Report je Feature-Team als Grundlage für die dortige Kapazitätsplanung
- Inspect & Adapt (I&A): Auswertung der KPI-Trends über das PI hinweg, Ableitung konkreter Verbesserungsmaßnahmen

### 9.3 Kontinuierliche Verbesserung
- Quartalsweiser „Test Health Check": Analyse von Ausführungszeiten, Flaky-Tests und technischer Schuld im Testcode
- Retrospektive Auswertung produktionsnaher Incidents: Prüfung, ob ein zusätzlicher automatisierter Testfall das Auftreten hätte verhindern können

## 10. Risiken und Mitigationsmaßnahmen

| Risiko | Auswirkung | Mitigationsmaßnahme |
|---|---|---|
| Hohe Flaky-Test-Rate durch UI5-Asynchronität | Vertrauensverlust in Automatisierung, manuelle Nachprüfung nötig | Gemeinsame Wartebibliothek, verpflichtende Selektorstrategie, quartalsweiser Health Check |
| Breaking Changes durch OData-/Annotationsänderungen | Massenhafte Testfehlschläge nach Updates generativer GUI-Frameworks | Contract-Tests auf Metadatenebene, automatische Kennzeichnung betroffener Tests |
| Fachbereich priorisiert Automatisierung zu niedrig gegenüber neuen Features | Wachsende Testschuld, sinkender Automatisierungsgrad | Verpflichtende DoD-Kriterien, KPI-Reporting in PI-Planning sichtbar machen |
| Abhängigkeit von Self-hosted Runnern (Netzwerkzugriff auf SAP-Systeme) | Pipeline-Ausfälle bei Runner-/Netzwerkproblemen | Redundante Runner-Pools, Monitoring/Alerting auf Runner-Verfügbarkeit |
| Unzureichende Testdatentrennung zwischen parallelen Pipeline-Läufen | Nicht-deterministische Testergebnisse durch Datenkollisionen | Isolierte Testdaten je Worker/Shard, API-basiertes Setup/Teardown |
| Regulatorische Nachweispflicht wird durch reine Automatisierung nicht ausreichend erfüllt | Beanstandungen in Revision/Aufsichtsprüfung | Verpflichtende XRAY-Traceability, Aufbewahrungsfristen für Artefakte |
| Fehlende zentrale Instanz führt zu inkonsistenten Standards zwischen den drei Feature-Teams | Divergierende Frameworks, doppelte Bausteine, uneinheitliche Testqualität | Gemeinsames Repository mit Pull-Request-Review durch alle beteiligten Teams, Testmanager als Eskalationsinstanz |
| WebGUI-Bildschirme bieten keine anpassbaren Selektor-Attribute | Höherer Wartungsaufwand und potenziell instabilere Selektoren bei Support-Package-Updates | Eigene WebGUI-Selektorstrategie auf Basis stabiler SAP-Feld-IDs, Klärung der Selektorstabilität vor finaler Freigabe |

## 11. Einführungs-Roadmap

| Phase | Zeitraum | Schwerpunkt |
|---|---|---|
| Phase 1 – Fundament | PI n (Monat 1–2) | Gemeinsames Playwright-Framework-Grundgerüst und GUI-Control-Wrapper-Bibliothek abgestimmt zwischen den Feature-Teams, GitHub-Actions-Basis-Pipeline, Pilot in einem Feature-Team an einer Klasse-A-App |
| Phase 2 – Skalierung | PI n (Monat 2–3) | Ausrollen auf alle drei Feature-Teams für Klasse-A-/B-Prozesse, XRAY-Ergebnis-Import produktiv, Definition-of-Done-Anpassung |
| Phase 3 – Stabilisierung | PI n+1 (Monat 1–2) | Flaky-Test-Reduktion, Selector Health Checks etablieren, Traceability-Reporting automatisieren |
| Phase 4 – Optimierung | Laufend ab PI n+1 | KPI-getriebene kontinuierliche Verbesserung, Erweiterung auf Klasse-C-Prozesse, wiederverwendbare Workflow-Bausteine für neue App-Teams |

## 12. Anhang

### 12.1 Glossar
- SAP-GUI (in diesem Dokument) – bezeichnet die browserbasierten Web-Oberflächen; ausdrücklich NICHT der klassische SAP-GUI-Windows-Client mit Transaktionscodes
- SAP GUI for HTML (WebGUI) – im Browser gerenderte Variante der klassischen Dynpro-Oberfläche
- Dynpro – SAPs klassisches Bildschirm-/Interaktionsmodell für Transaktionen
- OPA5 – One Page Acceptance Test, SAPUI5-eigenes Testframework für UI-Interaktionstests
- Generatives GUI-Framework – Metadaten-/Annotation-getriebenes Framework zur Generierung von GUI-Anwendungen ohne manuelles UI-Coding
- CDS-View – Core Data Services View, Datenmodellierungsschicht in SAP S/4HANA
- Flaky Test – Testfall mit inkonsistentem Ergebnis bei unverändertem Code- und Datenstand
- Storage State – von Playwright gespeicherter Session-/Cookie-Zustand zur Wiederverwendung einer Anmeldung über mehrere Tests hinweg
- Feature-Team – eines der für Test und Qualität eigenverantwortlichen Teams; es gibt keine zentrale QS- oder Testautomatisierungsinstanz
