"""
Integration tests for DocumentRepo against an in-memory SQLite database.

Tests:
- Insert a Document and retrieve it by id
- Get a Document by filename (used for duplicate detection)
- List all Documents returns correct count and fields
- Delete a Document by id cascades to Chunk records
- Update sync_status from OK to DELETE_PENDING and back
- Querying a non-existent id returns None
"""
