"""
Unit tests for IngestService.

Tests:
- Pre-checks run in order: file size → duplicate → PDF validity (short-circuits on first fail)
- Correct chunks produced for given chunk size and overlap settings
- Embedder_Client.embed_batch called once with all chunk texts
- Chroma_Client.add called with correct chunk ids and embeddings
- Document and Chunk records inserted in SQL database on success
- Rollback: all Chroma chunks deleted when SQL insert fails after VectorStore writes
- Cache document list invalidated on successful ingestion
- FILE_TOO_LARGE, DOCUMENT_ALREADY_EXISTS, INVALID_FILE_TYPE, EMPTY_DOCUMENT
  all raised before any extraction or embedding work begins
"""
