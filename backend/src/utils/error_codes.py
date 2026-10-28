"""
Application-level error code enumeration.

Defines all error code strings returned in the 'error_code' field of error responses.

Error codes:
- INVALID_FILE_TYPE       : Uploaded file is not a valid PDF
- FILE_TOO_LARGE          : Uploaded file exceeds MAX_UPLOAD_SIZE_MB
- EMPTY_DOCUMENT          : PDF contains no extractable text
- DOCUMENT_ALREADY_EXISTS : A document with the same filename has already been ingested
- DOCUMENT_NOT_FOUND      : No document found for the given id
- EMPTY_QUERY             : Question text is empty or whitespace-only
- QUERY_TOO_LONG          : Question text exceeds 2000 characters
- EMPTY_MESSAGE           : Chat message text is empty or whitespace-only
- MESSAGE_TOO_LONG        : Chat message text exceeds 2000 characters
- SESSION_NOT_FOUND       : No session found for the given session_id
- NO_DOCUMENTS_INGESTED   : VectorStore contains no chunks to query
- EMBEDDER_UNAVAILABLE    : Embedder_Client failed to generate an embedding
- VECTOR_STORE_UNAVAILABLE: Chroma_Client operation failed
- LLM_UNAVAILABLE         : Ollama_Client failed after all retries
- VALIDATION_ERROR        : Request body failed Pydantic schema validation
- INTERNAL_SERVER_ERROR   : Unhandled exception caught by global exception handler
"""
