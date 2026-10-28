"""
Sentence-transformers embedding client wrapper.

Responsibilities:
- Loads the configured EMBEDDING_MODEL from sentence-transformers exactly once at startup
- embed(text: str) -> list[float]  : Returns the embedding vector for a single text string
- embed_batch(texts: list[str])    : Returns a list of embedding vectors for bulk ingestion
- Used by Ingest_Service (batch) and Query_Service / Chat_Service (single)

Note:
- Must be constructed once per process (process-wide singleton) because model loading
  is expensive (~seconds) and the loaded model is stateless and thread-safe for inference
"""
