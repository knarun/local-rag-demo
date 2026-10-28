"""
Pydantic models for the chat endpoint.

Models:
- ChatRequest    : Accepted by POST /chat
    - message    : str            — the user's message (1–2000 characters, non-whitespace-only)
    - session_id : str | None     — existing session UUID, or None to start a new session

- ChatResponse   : Returned by POST /chat on success (HTTP 200)
    - answer     : str  — the LLM-generated assistant response
    - session_id : str  — the session UUID (newly created or the one passed in the request)
"""
