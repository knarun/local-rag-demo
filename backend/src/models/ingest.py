"""
Pydantic models for the ingest endpoint.

Models:
- IngestResponse : Returned by POST /ingest on success (HTTP 201)
    - document_id  : int   — the SQL primary key of the newly created Document
    - filename     : str   — the sanitized filename of the uploaded PDF
    - chunk_count  : int   — total number of chunks produced during ingestion
"""
