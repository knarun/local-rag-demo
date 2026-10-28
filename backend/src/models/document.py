"""
Pydantic models for the document management endpoints.

Models:
- DocumentOut   : Represents a single document in API responses
    - id          : int  — SQL primary key
    - filename    : str  — original PDF filename
    - chunk_count : int  — number of chunks stored in ChromaDB
    - sync_status : str  — 'OK' or 'DELETE_PENDING'
    - created_at  : datetime — UTC ingestion timestamp

- DocumentList  : Returned by GET /documents (HTTP 200)
    - documents   : list[DocumentOut]  — empty list when no documents exist (not an error)

- DeleteResponse : Returned by DELETE /documents/{id} (HTTP 200)
    - document_id : int  — the id of the successfully deleted document
"""
