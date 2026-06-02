"""
WARP Tool - Flask Application

Routes:
  GET  /              - Fragenkatalog (Single Page)
  POST /report        - PDF Generierung (HTML -> PDF via WeasyPrint)
  POST /report/html   - HTML-Vorschau des Reports (zum Debuggen)

Stateless: alle Antworten werden im Form-POST uebergeben,
nichts wird serverseitig gespeichert.
"""

from __future__ import annotations

import io
import datetime as dt
from collections import OrderedDict
from typing import Any, Dict, List

from flask import Flask, render_template, request, send_file, abort

from app.data.questions import CATEGORIES, ANSWER_OPTIONS, total_question_count


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")

    score_lookup = {opt["id"]: opt["score"] for opt in ANSWER_OPTIONS}
    label_lookup = {opt["id"]: opt["label"] for opt in ANSWER_OPTIONS}

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _collect_answers(form) -> Dict[str, str]:
        """Liest answer-* Felder aus dem Formular."""
        out: Dict[str, str] = {}
        for key, value in form.items():
            if key.startswith("answer-") and value:
                qid = key[len("answer-"):]
                if value in score_lookup:
                    out[qid] = value
        return out

    def _collect_notes(form) -> Dict[str, str]:
        out: Dict[str, str] = {}
        for key, value in form.items():
            if key.startswith("note-"):
                qid = key[len("note-"):]
                if value.strip():
                    out[qid] = value.strip()
        return out

    def _build_report_context(form) -> Dict[str, Any]:
        """Baut alle Daten fuer das Report-Template."""

        answers = _collect_answers(form)
        notes = _collect_notes(form)
        project_name = form.get("project_name", "").strip() or "Unbenannte Analyse"
        project_owner = form.get("project_owner", "").strip()
        project_date = form.get("project_date", "").strip() or dt.date.today().strftime("%d.%m.%Y")

        categories: List[Dict[str, Any]] = []
        all_scores: List[float] = []

        for cat in CATEGORIES:
            cat_scores: List[float] = []
            cat_questions: List[Dict[str, Any]] = []
            answered = 0
            distribution: "OrderedDict[str, int]" = OrderedDict(
                (opt["id"], 0) for opt in ANSWER_OPTIONS
            )

            for q in cat["questions"]:
                aid = answers.get(q["id"])
                if aid:
                    answered += 1
                    distribution[aid] += 1
                    score = score_lookup[aid]
                    cat_scores.append(score)
                    all_scores.append(score)

                cat_questions.append({
                    "id": q["id"],
                    "text": q["text"],
                    "hint": q.get("hint"),
                    "answer_id": aid,
                    "answer_label": label_lookup.get(aid),
                    "score": score_lookup.get(aid),
                    "note": notes.get(q["id"], ""),
                })

            cat_avg = sum(cat_scores) / len(cat_scores) if cat_scores else 0
            categories.append({
                "id": cat["id"],
                "title": cat["title"],
                "description": cat["description"],
                "questions": cat_questions,
                "answered": answered,
                "total": len(cat["questions"]),
                "score": round(cat_avg, 1),
                "distribution": [
                    {
                        "id": opt["id"],
                        "label": opt["label"],
                        "count": distribution[opt["id"]],
                    }
                    for opt in ANSWER_OPTIONS
                ],
            })

        overall = round(sum(all_scores) / len(all_scores), 1) if all_scores else 0
        answered_count = sum(c["answered"] for c in categories)

        # Reifegrad-Stufe ableiten
        if overall >= 80:
            maturity_label = "Optimiert"
            maturity_index = 5
        elif overall >= 60:
            maturity_label = "Etabliert"
            maturity_index = 4
        elif overall >= 40:
            maturity_label = "Definiert"
            maturity_index = 3
        elif overall >= 20:
            maturity_label = "Wiederholbar"
            maturity_index = 2
        else:
            maturity_label = "Initial"
            maturity_index = 1

        return {
            "project_name": project_name,
            "project_owner": project_owner,
            "project_date": project_date,
            "generated_at": dt.datetime.now().strftime("%d.%m.%Y, %H:%M"),
            "categories": categories,
            "overall_score": overall,
            "answered_count": answered_count,
            "total_count": total_question_count(),
            "maturity_label": maturity_label,
            "maturity_index": maturity_index,
            "answer_options": ANSWER_OPTIONS,
        }

    # ------------------------------------------------------------------
    # Routes
    # ------------------------------------------------------------------

    @app.route("/")
    def index():
        return render_template(
            "index.html",
            categories=CATEGORIES,
            answer_options=ANSWER_OPTIONS,
            total_questions=total_question_count(),
            today=dt.date.today().strftime("%Y-%m-%d"),
        )

    @app.route("/report/html", methods=["POST"])
    def report_html():
        """HTML-Vorschau (gleiches Template wie PDF, ohne PDF-Konvertierung)."""
        ctx = _build_report_context(request.form)
        return render_template("report.html", **ctx)

    @app.route("/report", methods=["POST"])
    def report_pdf():
        """PDF-Generierung via WeasyPrint."""
        try:
            from weasyprint import HTML, CSS  # type: ignore
        except ImportError:
            abort(500, description=(
                "WeasyPrint ist nicht installiert. Bitte `pip install -r requirements.txt` ausfuehren."
            ))

        ctx = _build_report_context(request.form)
        html = render_template("report.html", **ctx)

        pdf_bytes = HTML(
            string=html,
            base_url=request.host_url,
        ).write_pdf()

        filename = f"WARP_Report_{ctx['project_name'].replace(' ', '_')}_{dt.date.today().isoformat()}.pdf"
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=filename,
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
