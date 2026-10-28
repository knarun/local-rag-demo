"""
Document management route handler.

Responsibilities:
- Defines GET /documents endpoint — returns list of all ingested documents
- Defines DELETE /documents/{id} endpoint — removes a document and its chunks
- Delegates all processing to DocumentService
- HTTP layer only — contains no business logic
"""
