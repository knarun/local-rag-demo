"""
HTTP-level tests for POST /query.

Tests:
- Returns HTTP 200 with answer and source chunk ids on valid question
- Returns HTTP 422 with EMPTY_QUERY when question is empty or whitespace-only
- Returns HTTP 422 with QUERY_TOO_LONG when question exceeds 2000 characters
- Returns HTTP 404 with NO_DOCUMENTS_INGESTED when VectorStore is empty
- Returns HTTP 503 with EMBEDDER_UNAVAILABLE when embedder fails
- Returns HTTP 503 with VECTOR_STORE_UNAVAILABLE when Chroma fails
- Returns HTTP 503 with LLM_UNAVAILABLE when Ollama fails after all retries
- Returns cached response on repeated identical question (no Ollama call)
"""
