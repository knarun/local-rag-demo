"""
Ingest route handler.

Responsibilities:
- Defines POST /ingest endpoint
- Accepts a multipart PDF file upload via UploadFile
- Delegates all processing to IngestService
- Returns IngestResponse (document_id, filename, chunk_count) with HTTP 201 on success
- HTTP layer only — contains no business logic
"""
