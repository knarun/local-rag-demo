"""
Unit tests for ChatService.

Tests:
- New session created and persisted when no session_id provided
- SESSION_NOT_FOUND raised for unknown session_id
- NO_DOCUMENTS_INGESTED raised before session lookup when VectorStore is empty
- EMPTY_MESSAGE and MESSAGE_TOO_LONG raised on invalid message input
- Embedding fetched from cache when available (Embedder_Client not called)
- Embedding generated and cached when cache is cold
- EMBEDDER_UNAVAILABLE raised without persisting user message on embedder failure
- Chunk retrieval fetched from cache when available (Chroma_Client not called)
- VECTOR_STORE_UNAVAILABLE raised without persisting user message on Chroma failure
- Prompt constructed with correct order: chunks → history (last N) → current message
- Ollama_Client.chat always called (LLM responses never served from cache)
- User message and assistant response both persisted on success
- User message NOT persisted when Ollama fails after all retries
"""
