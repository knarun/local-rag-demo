"""
Document repository — SQL query operations for the Document table.

Responsibilities:
- Insert a new Document record (filename, file_size, chunk_count, created_at)
- Get a Document by its integer primary key id
- Get a Document by its filename (used for duplicate detection during ingestion)
- List all Document records (used by DocumentService when cache is cold)
- Delete a Document record by id (cascades to Chunk records via FK constraint)
- Update the sync_status of a Document (OK → DELETE_PENDING and back)
- All methods accept a SQLAlchemy Session and execute within the caller's transaction
"""
