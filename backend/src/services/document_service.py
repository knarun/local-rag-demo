"""
Document service — business logic for document listing and deletion.

Responsibilities:
- List: checks Redis cache first; falls back to document_repo query and caches the result
- Returns an empty list (not an error) when no documents exist
- Delete: verifies the document exists in SQL before touching the VectorStore
- Removes all associated chunk embeddings from Chroma_Client as an idempotent batch call
- Handles partial VectorStore deletion failures by marking the document as DELETE_PENDING
  and logging the unconfirmed chroma_ids — safe to retry because the batch delete is idempotent
- Deletes the Document and Chunk SQL records only after full VectorStore removal is confirmed
- Invalidates the cached document list in Redis after successful deletion
"""
