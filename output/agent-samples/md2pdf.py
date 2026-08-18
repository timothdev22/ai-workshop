"""Markdown -> PDF. A plain function. No LLM, no API key, no network.

    python md2pdf.py reports/what-is-rag.md

This is the counterexample to the agent: the task is fully specified, so it needs
zero judgment and therefore zero intelligence. Adding a model here would buy
nothing and cost money.
"""

import sys
from pathlib import Path

import markdown
from fpdf import FPDF

REPORTS = Path(__file__).parent / "reports"


def md_to_pdf(md_path: str | Path) -> Path:
    """Convert a Markdown file to a PDF beside it. Returns the PDF path."""
    md_path = Path(md_path).resolve()
    # Guardrail: only ever read and write inside reports/.
    if not md_path.is_relative_to(REPORTS.resolve()):
        raise ValueError(f"refusing to touch a path outside {REPORTS}: {md_path}")

    html = markdown.markdown(md_path.read_text(encoding="utf-8"),
                             extensions=["tables", "fenced_code"])
    # fpdf2's built-in fonts are latin-1 only; drop what they cannot encode.
    # For full Unicode, add a TTF: pdf.add_font("dejavu", fname="DejaVuSans.ttf").
    html = html.encode("latin-1", "replace").decode("latin-1")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", size=11)
    pdf.write_html(html)

    out = md_path.with_suffix(".pdf")
    pdf.output(str(out))
    return out


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python md2pdf.py <path-to-markdown>")
    print(md_to_pdf(sys.argv[1]))
