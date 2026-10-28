"""
Pydantic models for the one-shot query endpoint.

Models:
- QueryRequest  : Accepted by POST /query
    - question  : str — the user's question (1–2000 characters, non-whitespace-only)

- QueryResponse : Returned by POST /query on success (HTTP 200)
    - answer    : str        — the LLM-generated answer text
    - sources   : list[str]  — list of ChromaDB chunk IDs used as context
"""
