"""Report Agent.

Owner: Adeel.

For each triaged finding, retrieves relevant CVE/OWASP reference material
from ChromaDB (see rag/chroma_store.py) and drafts a plain-language report
with a specific suggested fix per item, not a raw tool log
(docs/ARCHITECTURE.md "5. Report Agent"). RAG grounding here is the
mitigation against confident-but-wrong report text.
"""

from __future__ import annotations

# TODO: from autoredblue.rag import chroma_store
# TODO: from autoredblue.llm import ollama_client, parsing


def generate_report(state):
    """Turn `triaged_findings` into a plain-language report with
    RAG-grounded fix suggestions.

    TODO
    """
    raise NotImplementedError
