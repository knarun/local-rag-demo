"""
HTTP-level tests for POST /chat.

Tests:
- Returns HTTP 200 with answer and new session_id when no session_id is provided
- Returns HTTP 200 with answer and same session_id on subsequent messages
- Returns HTTP 422 with EMPTY_MESSAGE when message is empty or whitespace-only
- Returns HTTP 422 with MESSAGE_TOO_LONG when message exceeds 2000 characters
- Returns HTTP 404 with SESSION_NOT_FOUND when session_id does not exist
- Returns HTTP 404 with NO_DOCUMENTS_INGESTED when VectorStore is empty
- Returns HTTP 503 with LLM_UNAVAILABLE when Ollama fails after all retries
- Does NOT persist the user message when the LLM call fails
- Does NOT use cache for LLM responses (Ollama is always called for each turn)
"""
