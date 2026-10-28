"""
Query service — business logic for one-shot question answering.

Responsibilities:
- Validates the question (non-empty, within 2000 character limit)
- Checks that the VectorStore contains at least one chunk before embedding
- Implements a three-level cache-first flow:
    1. Check cache for the question embedding; generate via Embedder_Client if missing
    2. Check cache for chunk retrieval results; query Chroma_Client if missing
    3. Check cache for the LLM response; call Ollama_Client if missing
- Stores each computed result in Redis with its configured TTL
- Retries Ollama calls up to the configured MAX_RETRY_ATTEMPTS on failure
- Returns the answer text and the source ChromaDB chunk identifiers
"""
