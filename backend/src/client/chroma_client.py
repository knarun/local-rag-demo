"""
ChromaDB client wrapper.

Responsibilities:
- Initializes a persistent ChromaDB client at the configured CHROMA_PERSIST_PATH
- Creates or retrieves the default collection on startup (process-wide singleton)
- add()    : Store a list of chunks with their embeddings and chroma_ids
- query()  : Retrieve top-K most similar chunks for a given embedding vector
- delete() : Remove chunks by chroma_id as an idempotent batch operation
              (safe to call with already-deleted IDs — does not raise an error)

Note:
- Must be constructed once per process and reused across all requests
  to avoid reopening the persistent store and exhausting file handles
"""
