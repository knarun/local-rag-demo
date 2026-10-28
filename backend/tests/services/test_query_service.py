"""
Unit tests for QueryService.

Tests:
- EMPTY_QUERY raised for empty or whitespace-only question
- QUERY_TOO_LONG raised when question exceeds 2000 characters
- NO_DOCUMENTS_INGESTED raised before any embedding work when VectorStore is empty
- Embedding fetched from cache when available (Embedder_Client not called)
- Embedding generated via Embedder_Client and stored in cache on cache miss
- EMBEDDER_UNAVAILABLE raised on embedder failure
- Chunk retrieval fetched from cache when available (Chroma_Client not called)
- Chunk retrieval executed via Chroma_Client and stored in cache on cache miss
- VECTOR_STORE_UNAVAILABLE raised on Chroma failure
- LLM response fetched from cache when available (Ollama_Client not called)
- LLM response generated via Ollama_Client and stored in cache on cache miss
- LLM_UNAVAILABLE raised after MAX_RETRY_ATTEMPTS failures
- Correct source chunk ids returned in QueryResponse
"""
