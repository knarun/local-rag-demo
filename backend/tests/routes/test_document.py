"""
HTTP-level tests for GET /documents and DELETE /documents/{id}.

Tests:
- GET returns HTTP 200 with an empty list when no documents are ingested
- GET returns HTTP 200 with a list of DocumentOut objects including sync_status
- GET returns cached result on second call (no DB query)
- DELETE returns HTTP 200 with deleted document_id on success
- DELETE returns HTTP 404 with DOCUMENT_NOT_FOUND for unknown id
- DELETE returns HTTP 503 with VECTOR_STORE_UNAVAILABLE when Chroma fails before any removal
- DELETE marks document as DELETE_PENDING and returns 503 on partial Chroma failure
- GET excludes DELETE_PENDING documents from query results
"""
