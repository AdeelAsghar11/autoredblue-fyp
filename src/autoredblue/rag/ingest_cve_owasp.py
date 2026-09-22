"""One-off ingestion script: CVE/OWASP reference material -> ChromaDB.

Owner: Adeel.

Populates the collection that rag/chroma_store.py queries at report time.
Not part of the live pipeline: run manually / as setup, not per-audit.
"""

from __future__ import annotations

# TODO: from autoredblue.rag import chroma_store


def main():
    """Ingest CVE/OWASP source material into the ChromaDB collection.

    TODO
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
