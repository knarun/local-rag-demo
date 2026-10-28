"""
SQLAlchemy ORM definition for the Chunk table.

Columns:
- id          : Integer, primary key, auto-increment
- document_id : Integer, foreign key to document.id, not null
                Cascade deletes when the parent Document is removed
- chunk_index : Integer, not null, >= 0 — positional index of this chunk within the document
- content     : Text, not null — raw text content of the chunk
- chroma_id   : String(255), not null — the ID used to identify this chunk in ChromaDB

Relationships:
- Many Chunks belong to one Document
"""
