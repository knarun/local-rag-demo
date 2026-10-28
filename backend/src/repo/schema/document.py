"""
SQLAlchemy ORM definition for the Document table.

Columns:
- id          : Integer, primary key, auto-increment
- filename    : String(255), unique, not null — original PDF filename
- file_size   : Integer, not null — file size in bytes
- chunk_count : Integer, not null, >= 0 — number of chunks produced during ingestion
- sync_status : Enum('OK', 'DELETE_PENDING'), not null, default 'OK'
                Set to DELETE_PENDING when a partial VectorStore deletion is detected
- created_at  : DateTime, not null, default current UTC timestamp

Relationships:
- One Document has many Chunks (cascade delete on document removal)
"""
