"""
Ingest service — business logic for PDF document ingestion.

Responsibilities:
- Runs pre-checks in fixed order: file size → duplicate filename → PDF validity
- Extracts full text from the PDF via PDF_Client
- Splits text into token-aware chunks using configurable max size and overlap
- Generates an embedding for each chunk via Embedder_Client
- Stores chunks and embeddings in the VectorStore via Chroma_Client
- Records Document metadata in the SQL database via document_repo and chunk_repo
- Rolls back partially written VectorStore chunks if any pipeline step fails
- Invalidates the cached document list in Redis on successful ingestion
"""
