"""
HTTP-level tests for POST /ingest.

Tests:
- Returns HTTP 201 with document_id, filename, chunk_count on valid PDF upload
- Returns HTTP 413 when file exceeds MAX_UPLOAD_SIZE_MB
- Returns HTTP 409 when a document with the same filename already exists
- Returns HTTP 422 with INVALID_FILE_TYPE when file is not a valid PDF
- Returns HTTP 422 with EMPTY_DOCUMENT when PDF contains no extractable text
- Returns HTTP 503 with EMBEDDER_UNAVAILABLE when embedder fails
- Returns HTTP 503 with VECTOR_STORE_UNAVAILABLE when Chroma fails
"""
