"""
Chunk repository — SQL query operations for the Chunk table.

Responsibilities:
- Bulk insert Chunk records (document_id, chunk_index, content, chroma_id)
- Get all Chunk records for a given document_id (used during document deletion)
- Delete all Chunk records for a given document_id
- All methods accept a SQLAlchemy Session and execute within the caller's transaction
"""
