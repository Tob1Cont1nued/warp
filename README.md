# WARP Tool — Funktionaler Fragenkatalog

Reifegrad-Analyse-Tool für Wavestone WARP. **Mobile-first**, stateless: Fragen beantworten → PDF mit Statistiken herunterladen.

## Stack

- **Python 3.10+** mit Flask
- **WeasyPrint** für die HTML→PDF-Konvertierung
- Reines Server-Side-Templating (Jinja) + CSS — kein JS-Framework
- Layout: Mobile-First mit Breakpoints bei 720 px (Tablet) und 1024 px (Desktop)

## Lokal starten

```bash
python3 -m venv .venv
source .venv/bin/activate            # macOS / Linux
# .venv\Scripts\activate             # Windows

pip install -r requirements.txt
python run.py
# → http://127.0.0.1:5000/
```

> **WeasyPrint** braucht auf macOS `brew install pango libffi`,
> auf Ubuntu/Debian `sudo apt install libpango-1.0-0 libpangoft2-1.0-0`.

## Per Docker starten (empfohlen für Server)

```bash
docker build -t warp-tool .
docker run -p 8080:8080 warp-tool
# → http://127.0.0.1:8080/
```

Das Image enthält alle WeasyPrint-System-Libraries und Gunicorn als Production-Server.

---

## GitLab-Deployment

> **Wichtig:** GitLab **Pages** ist nur für statische Sites — eine Flask-App
> mit serverseitiger PDF-Generierung kann dort **nicht** betrieben werden.
> Stattdessen liefere ich eine vollständige CI/CD-Pipeline (`.gitlab-ci.yml`),
> die ein Docker-Image baut, in die GitLab Container Registry pusht und
> per SSH auf einen Server deployt.

### Out-of-the-box-Setup

1. **Repository in GitLab anlegen** und diesen Code hochladen.
2. In den Repo-**Settings → CI/CD → Variables** drei Variablen eintragen:

   | Name | Inhalt | Schutz |
   |---|---|---|
   | `SSH_PRIVATE_KEY` | privater SSH-Key (gesamter Key inkl. Header/Footer) | Protected, Masked |
   | `SSH_HOST` | IP / Domain des Zielservers | Protected |
   | `SSH_USER` | User auf dem Zielserver (z.B. `deploy`) | Protected |

3. Auf dem Zielserver muss **Docker** installiert sein:
   ```bash
   curl -fsSL https://get.docker.com | sh
   usermod -aG docker $USER
   ```
4. Push auf `main`/`master` → Pipeline:
   - **build**: baut Image, pusht in `registry.gitlab.com/<group>/<project>:latest`
   - **deploy:ssh**: manueller Klick → Server pullt Image, startet Container auf Port 8080

### Alternativen

- **Kein eigener Server?** Den `deploy:ssh`-Job entfernen und das Image z.B. auf
  Render, Railway, Fly.io oder einem Kubernetes-Cluster (Auto Deploy) deployen.
  Das Image folgt der `PORT`-ENV-Konvention der meisten PaaS-Anbieter.
- **Nur Image bauen** und manuell `docker run` ausführen — die `build`-Stage
  reicht dafür schon aus.

---

## Bedienung

1. Projektname, Verantwortliche/n und Datum eintragen.
2. Pro Frage eine der vier Bewertungen wählen:
   - **Trifft voll zu** — 100 %
   - **Trifft zu** — 66 %
   - **Trifft kaum zu** — 33 %
   - **Trifft nicht zu** — 0 %
3. Optional Notizen pro Frage.
4. **PDF herunterladen** klickt → Report wird generiert und als Download geliefert.

## Mobile-Ansicht

- **< 720 px** (Phone): Sidebar als Off-Canvas-Drawer (Burger-Icon oben links),
  Fragen als gestapelte Karten statt Tabelle, große Hit-Targets (44 px),
  16-px-Inputs (kein iOS-Zoom-Bug).
- **720 – 1023 px** (Tablet): 3-Spalten-Projektgrid, Buttons nebeneinander,
  Fragen weiterhin als Karten.
- **≥ 1024 px** (Desktop): Permanente Sidebar, Fragen als Tabelle (wie Figma).

## Fragenkatalog erweitern

Alle Fragen liegen in **`app/data/questions.py`**. Neue Kategorie:

```python
{
    "id": "neue-kat",
    "title": "Neue Kategorie",
    "description": "...",
    "questions": [
        {"id": "nk-1", "text": "Frage", "hint": "optionaler Hilfstext"},
    ],
}
```

`id`-Werte müssen eindeutig sein (über alle Kategorien hinweg).

## Projektstruktur

```
.
├── run.py                       # Local entry point
├── requirements.txt
├── Dockerfile                   # Container-Build (Gunicorn + WeasyPrint deps)
├── .gitlab-ci.yml               # GitLab CI/CD pipeline
└── app/
    ├── __init__.py              # Flask App + Routes
    ├── data/questions.py        # Fragenkatalog
    ├── static/
    │   ├── css/app.css          # Mobile-first Styling
    │   └── img/warp-logo-*.svg
    └── templates/
        ├── index.html           # Fragenkatalog
        └── report.html          # PDF / HTML Report
```

## PDF-Inhalt

- **Cover-Seite** mit Wavestone-Branding (Magenta-Akzent), Projektname, Datum.
- **Executive Summary** mit Gesamtscore, Reifegrad-Stufe (Initial → Optimiert),
  Balkendiagramm pro Kategorie.
- **Detailauswertung** pro Kategorie: Antwort-Verteilungs-Bar + alle Fragen
  mit Bewertung, Score und Notizen.
- Footer mit Seitenzahl auf jeder Seite.
