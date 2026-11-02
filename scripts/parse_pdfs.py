"""Converte i PDF in data/ in Markdown (cv.pdf -> cv.md, linkedin.pdf -> linkedin.md).

Dopo l'esecuzione rivedi i .md a mano: l'estrazione dai PDF non è mai perfetta.

Richiede il gruppo di dipendenze opzionale "parse" (PyMuPDF, AGPL):
    uv run --group parse python scripts/parse_pdfs.py
"""
from pathlib import Path

import pymupdf.layout  # noqa: F401 (va importato prima di pymupdf4llm per attivare l'analisi del layout)
import pymupdf4llm

DATA = Path(__file__).resolve().parent.parent / "data"

for pdf in sorted(DATA.glob("*.pdf")):
    out = pdf.with_suffix(".md")
    out.write_text(pymupdf4llm.to_markdown(str(pdf)), encoding="utf-8")
    print(f"{pdf.name} -> {out.name}")
