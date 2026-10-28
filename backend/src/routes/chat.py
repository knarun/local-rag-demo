"""
Session-aware chat route handler.

Responsibilities:
- Defines POST /chat endpoint
- Accepts a ChatRequest (message text, optional session_id)
- Delegates all processing to ChatService
- Returns ChatResponse (LLM response text, session_id) with HTTP 200
- HTTP layer only — contains no business logic
"""
