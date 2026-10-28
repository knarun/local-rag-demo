"""
One-shot query route handler.

Responsibilities:
- Defines POST /query endpoint
- Accepts a QueryRequest (question text)
- Delegates all processing to QueryService
- Returns QueryResponse (answer text, source chunk identifiers) with HTTP 200
- HTTP layer only — contains no business logic
"""
