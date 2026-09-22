"""ChromaDB vector store wrapper.

Owner: Adeel (backs the Report Agent's RAG step, agents/report.py).

Holds the CVE/OWASP reference material ingested by
rag/ingest_cve_owasp.py, queried by the Report Agent to ground its
generated fix suggestions (docs/ARCHITECTURE.md "5. Report Agent").
"""

from __future__ import annotations

# TODO: import chromadb


def get_collection():
    """Return the ChromaDB collection holding CVE/OWASP reference
    material.

    TODO
    """
    raise NotImplementedError


def query(text: str, *, n_results: int = 5):
    """Return the `n_results` most relevant reference chunks for `text`.

    TODO
    """
    raise NotImplementedError
