# Requirements Document

## Introduction

This document specifies the requirements for a local Retrieval-Augmented Generation (RAG) chatbot application. The system allows users to upload PDF documents, which are processed and stored in a local vector database. Users can then query the system in a one-shot mode or engage in a multi-turn session-aware conversation. All inference runs locally via Ollama, eliminating data-privacy concerns associated with cloud LLM providers. Redis caching reduces latency for repeated queries, and structured logging with global error handling ensures operational visibility.

> **Revision note:** This revision resolves eight issues found in review: (1) a missing `session` table causing a persistence/lookup contradiction in Chat_Service, (2) inconsistent ordering of the empty-vector-store check between Query_Service and Chat_Service, (3) missing failure-handling criteria for Chat_Service's Embedder/VectorStore calls, (4) an unstated LLM-response-caching policy for Chat_Service, (5) unspecified relative ordering of ingestion pre-checks, (6) an unimplementable cache key (raw embedding vector) for retrieval results, (7) no repair path for partial VectorStore deletion failures, and (8) cache keys not versioned against model/config changes.

---

## Glossary

- **System**: The local RAG chatbot application (FastAPI backend + React frontend).
- **Document**: A PDF file uploaded by the user and tracked in the SQL database.
- **Chunk**: A text segment extracted from a Document after splitting; the unit stored in ChromaDB.
- **Embedding**: A fixed-length vector representation of a Chunk or query, produced by the Embedder.
- **Embedder**: The sentence-transformers model (e.g., `all-MiniLM-L6-v2`) used to generate Embeddings.
- **VectorStore**: ChromaDB running locally with persistent storage.
- **LLM**: The Ollama-hosted language model (e.g., `llama3`) used to generate answers.
- **Session**: A conversation identified by a unique `session_id`, tracked as its own record in the SQL database, whose associated messages are persisted as Conversation Turns.
- **Conversation Turn**: A single logged message (`user` or `assistant`) belonging to a Session.
- **Cache**: Redis instance used to store computed Embeddings, LLM responses, chunk retrieval results, and document lists with TTL-based expiry.
- **Ingest_Service**: The backend service responsible for PDF extraction, chunking, embedding, and storage.
- **Query_Service**: The backend service responsible for one-shot question answering.
- **Chat_Service**: The backend service responsible for session-aware multi-turn conversation.
- **Document_Service**: The backend service responsible for listing and deleting Documents.
- **Cache_Client**: The Redis client wrapper used by all services for cache reads and writes.
- **Ollama_Client**: The HTTP client wrapper for communicating with the local Ollama server.
- **Chroma_Client**: The ChromaDB client wrapper for vector similarity search.
- **Embedder_Client**: The sentence-transformers wrapper for producing Embeddings.
- **PDF_Client**: The pypdf/pdfplumber wrapper for extracting raw text from PDF files.
- **Repo**: A repository module that executes SQL operations via SQLAlchemy.
- **N**: A configurable integer (1–50) representing the number of recent conversation turns retrieved from history for LLM context.
- **TTL**: Time-to-live (0–86400 seconds), the duration after which a Cache entry expires.
- **Cache Namespace**: A version tag, derived from `EMBEDDING_MODEL` and `OLLAMA_MODEL`, prefixed onto all cache keys so that changing a model does not serve stale results computed under a different model.

---

## Requirements

### Requirement 1: PDF Document Ingestion

**User Story:** As a user, I want to upload a PDF document so that its content becomes searchable through the chatbot.

#### Acceptance Criteria

1. WHEN a user submits a file via the ingest endpoint, THE Ingest_Service SHALL run pre-checks in the following fixed order, short-circuiting on the first failure, before any extraction begins: (a) file size check, (b) duplicate filename check, (c) PDF validity check. This order runs the cheapest checks (size from the upload's declared content length, then a DB lookup) before the most expensive check (parsing the file), so that oversized or duplicate files are rejected without ever being parsed.
2. IF the uploaded file exceeds the configurable maximum file size, THEN THE Ingest_Service SHALL return an error response with error code `FILE_TOO_LARGE` and HTTP status 413.
3. IF a Document with the same filename already exists in the SQL database, THEN THE Ingest_Service SHALL return an error response with error code `DOCUMENT_ALREADY_EXISTS` and HTTP status 409.
4. IF the uploaded file is not a valid PDF (parseable by PDF_Client with at least one page), THEN THE Ingest_Service SHALL return an error response with error code `INVALID_FILE_TYPE` and HTTP status 422.
5. WHEN the file passes all pre-checks, THE Ingest_Service SHALL extract the full text from the PDF using the PDF_Client.
6. IF the PDF text extraction yields no text, THEN THE Ingest_Service SHALL return an error response with error code `EMPTY_DOCUMENT` and HTTP status 422.
7. WHEN the text has been extracted, THE Ingest_Service SHALL split the text into Chunks using a token-aware text splitter, respecting a configurable maximum chunk size (1–2048 tokens) and configurable chunk overlap (0–512 tokens, must be less than maximum chunk size).
8. WHEN Chunks have been produced, THE Ingest_Service SHALL generate an Embedding for each Chunk using the Embedder_Client.
9. WHEN Embeddings have been generated, THE Ingest_Service SHALL store each Chunk and its Embedding in the VectorStore via the Chroma_Client.
10. WHEN all Chunks are stored in the VectorStore, THE Ingest_Service SHALL record the Document metadata (filename, file size in bytes, chunk count, ingestion timestamp) in the SQL database via the document Repo.
11. WHEN ingestion completes successfully, THE System SHALL return a response containing the Document identifier, filename, and total chunk count with HTTP status 201.
12. IF any pipeline step fails after VectorStore writes have begun, THEN THE Ingest_Service SHALL remove all partially written Chunks from the VectorStore before returning an error response.
13. WHEN a Document is successfully ingested, THE Cache_Client SHALL invalidate the cached document list entry so that subsequent list requests reflect the new Document.

---

### Requirement 2: One-Shot Query

**User Story:** As a user, I want to ask a question about my uploaded documents and receive a direct answer without maintaining a conversation session.

#### Acceptance Criteria

1. IF the question text is empty, contains only whitespace, or exceeds 2000 characters, THEN THE Query_Service SHALL return an error response with error code `EMPTY_QUERY` or `QUERY_TOO_LONG` respectively and HTTP status 422.
2. IF the VectorStore contains no Chunks, THEN THE Query_Service SHALL return an error response with error code `NO_DOCUMENTS_INGESTED` and HTTP status 404, before any Embedding work begins.
3. WHEN a user submits a valid question to the query endpoint, THE Query_Service SHALL check the Cache for a previously computed Embedding keyed by `{cache_namespace}:embedding:{sha256(question_text)}`.
4. WHEN no cached Embedding exists, THE Query_Service SHALL generate an Embedding for the question using the Embedder_Client and store it in the Cache with the configured embedding TTL.
5. IF the Embedder_Client fails, THEN THE Query_Service SHALL return an error response with error code `EMBEDDER_UNAVAILABLE` and HTTP status 503.
6. WHEN the question Embedding is available, THE Query_Service SHALL check the Cache for a previously retrieved chunk result set keyed by `{cache_namespace}:retrieval:{sha256(embedding_vector_bytes)}`, where the Embedding vector is deterministically serialized (fixed float precision, fixed byte order) before hashing.
7. WHEN no cached chunk result set exists, THE Query_Service SHALL retrieve the top-K most similar Chunks from the VectorStore using the Chroma_Client and store the result set in the Cache with the configured retrieval TTL.
8. IF the Chroma_Client fails, THEN THE Query_Service SHALL return an error response with error code `VECTOR_STORE_UNAVAILABLE` and HTTP status 503.
9. WHEN the relevant Chunks are available, THE Query_Service SHALL check the Cache for a previously generated LLM response keyed by `{cache_namespace}:llm:{sha256(question_text + sorted(chunk_ids))}`.
10. WHEN no cached LLM response exists, THE Query_Service SHALL send the question and retrieved Chunks as context to the LLM via the Ollama_Client and store the response in the Cache with the configured LLM response TTL.
11. IF the Ollama_Client request fails, THEN THE Query_Service SHALL retry the request up to the configured maximum retry attempts before returning an error response with error code `LLM_UNAVAILABLE` and HTTP status 503.
12. WHEN the LLM response is available, THE System SHALL return the answer text and the list of source Chunk identifiers (ChromaDB chunk IDs) used as context with HTTP status 200.

---

### Requirement 3: Session-Aware Chat

**User Story:** As a user, I want to have a multi-turn conversation with the chatbot, where the system remembers previous exchanges within my session, so that I can ask follow-up questions naturally.

#### Acceptance Criteria

1. IF the message text is empty or contains only whitespace, THEN THE Chat_Service SHALL return an error response with error code `EMPTY_MESSAGE` and HTTP status 422.
2. IF the VectorStore contains no Chunks, THEN THE Chat_Service SHALL return an error response with error code `NO_DOCUMENTS_INGESTED` and HTTP status 404, before any Session lookup/creation or Embedding work begins.
3. WHEN a user sends a message to the chat endpoint without a `session_id`, THE Chat_Service SHALL create a new Session record (UUID primary key, `created_at` timestamp) via the session Repo and persist it to the SQL database **immediately**, independent of whether the subsequent LLM call succeeds, and return the generated `session_id` in the response.
4. IF the provided `session_id` does not correspond to any existing Session record in the SQL database, THEN THE Chat_Service SHALL return an error response with error code `SESSION_NOT_FOUND` and HTTP status 404.
5. WHEN a valid `session_id` is provided (newly created or pre-existing), THE Chat_Service SHALL retrieve the last N Conversation Turns for that session from the SQL database via the conversation Repo, ordered by creation timestamp ascending. A newly created Session with zero Conversation Turns SHALL be treated as valid, yielding an empty history rather than an error.
6. WHEN the current message is available, THE Chat_Service SHALL check the Cache for a previously computed Embedding keyed by `{cache_namespace}:embedding:{sha256(message_text)}`; if absent, generate one via the Embedder_Client and store it with the configured embedding TTL.
7. IF the Embedder_Client fails, THEN THE Chat_Service SHALL return an error response with error code `EMBEDDER_UNAVAILABLE` and HTTP status 503 without persisting the user message for that turn.
8. WHEN the message Embedding is available, THE Chat_Service SHALL check the Cache for a previously retrieved chunk result set keyed by `{cache_namespace}:retrieval:{sha256(embedding_vector_bytes)}` (same deterministic serialization as Requirement 2.6); if absent, retrieve the top-K most similar Chunks from the VectorStore via the Chroma_Client and store the result with the configured retrieval TTL.
9. IF the Chroma_Client fails, THEN THE Chat_Service SHALL return an error response with error code `VECTOR_STORE_UNAVAILABLE` and HTTP status 503 without persisting the user message for that turn.
10. WHEN the retrieved Chunks are available, THE Chat_Service SHALL construct a prompt containing the retrieved Chunks as context, the last N conversation turns (each with role and content), and the current user message, then send it to the LLM via the Ollama_Client. LLM responses in Chat_Service SHALL NOT be served from or written to the Cache, because response correctness here depends on the full conversation history rather than the message text alone, making a cache hit unsafe across sessions or turns.
11. IF the Ollama_Client request fails after all configured retries, THEN THE Chat_Service SHALL return an error response with error code `LLM_UNAVAILABLE` and HTTP status 503 without persisting the user message for that turn.
12. WHEN the LLM response is received, THE Chat_Service SHALL persist both the user message (role: `user`) and the LLM response (role: `assistant`) as new Conversation Turns in the SQL database via the conversation Repo, linked to the Session.
13. WHEN all persistence operations are complete, THE System SHALL return the LLM response text and the `session_id` to the user with HTTP status 200.
14. WHILE a Session exists, THE Chat_Service SHALL maintain the full Conversation Turn history in the SQL database regardless of the Cache state.

---

### Requirement 4: Document Management

**User Story:** As a user, I want to list all ingested documents and delete documents I no longer need, so that I can manage the knowledge base of the chatbot.

#### Acceptance Criteria

1. WHEN a user requests the document list endpoint, THE Document_Service SHALL check the Cache for a previously stored document list under key `{cache_namespace}:documents:list`.
2. WHEN no cached document list exists, THE Document_Service SHALL query the SQL database via the document Repo for all Document records and store the result in the Cache with the configured document list TTL.
3. WHEN the document list is retrieved (from Cache or DB), THE System SHALL return the list with HTTP status 200; IF no Documents exist, THE System SHALL return an empty list (not an error).
4. WHEN a user requests deletion of a Document by its identifier, THE Document_Service SHALL first verify the identifier exists in the SQL database via the document Repo; IF not found, return error code `DOCUMENT_NOT_FOUND` and HTTP status 404.
5. WHEN the Document exists, THE Document_Service SHALL remove all associated Chunks and Embeddings from the VectorStore via the Chroma_Client, issuing the delete as a single idempotent batch call keyed by `chroma_id`.
6. IF the Chroma_Client deletion fails before any Chunks are removed, THEN THE Document_Service SHALL return an error response with error code `VECTOR_STORE_UNAVAILABLE` and HTTP status 503 without deleting SQL records, preserving data integrity.
7. IF the Chroma_Client deletion fails partway through (some Chunks removed, some not), THEN THE Document_Service SHALL: (a) log the affected `document_id` and the set of `chroma_id`s not confirmed deleted at ERROR level, (b) mark the Document record with a `sync_status` of `DELETE_PENDING` rather than deleting it, and (c) return an error response with error code `VECTOR_STORE_UNAVAILABLE` and HTTP status 503. A Document in `DELETE_PENDING` status SHALL be excluded from query/chat retrieval results (Requirements 2 and 3) even though its SQL record still exists, and SHALL be retried by re-invoking this deletion step — safe because the batch delete by `chroma_id` is idempotent for already-removed IDs.
8. WHEN the VectorStore entries are fully removed (directly, or via a successful retry of a `DELETE_PENDING` Document), THE Document_Service SHALL delete the Document record and all associated Chunk records from the SQL database via the document Repo and chunk Repo.
9. WHEN the SQL records are deleted, THE Cache_Client SHALL invalidate the cached document list entry so that subsequent list requests reflect the deletion.
10. WHEN all deletion steps are complete, THE System SHALL return a success response confirming the deleted document identifier with HTTP status 200.

---

### Requirement 5: Redis Caching

**User Story:** As a developer, I want all expensive computation results to be cached in Redis, so that repeated requests receive faster responses and the system reduces load on the LLM and Embedder.

#### Acceptance Criteria

1. THE Cache_Client SHALL store query Embeddings, chunk retrieval results, one-shot LLM responses (Requirement 2 only — see Requirement 3.10 for why Chat_Service LLM responses are excluded), and document lists, each with its own TTL (0–86400 seconds) configurable per data type via application settings.
2. WHEN a cache key is present and has not expired, THE Cache_Client SHALL return the cached value without re-executing the underlying computation.
3. WHEN a cache key is absent or has expired, THE Cache_Client SHALL allow the calling service to execute the computation and then write the result to the Cache under a key constructed as `{cache_namespace}:{cache_type_prefix}:{deterministic_hash_of_inputs}`, where `deterministic_hash_of_inputs` is a SHA-256 hash of the relevant, deterministically-serialized inputs (see Requirements 2.3, 2.6, 2.9, 3.6, 3.8 for the exact inputs hashed per cache type).
4. THE Cache_Client SHALL derive `cache_namespace` from the currently configured `EMBEDDING_MODEL` and `OLLAMA_MODEL` settings (e.g., a short hash of their concatenation), so that changing either model at startup begins writing to a disjoint set of cache keys rather than serving stale results computed under a different model. Namespace derivation SHALL happen once at startup and SHALL NOT require manual cache flushing on a model change.
5. WHEN a Document is ingested or deleted, THE Cache_Client SHALL invalidate the document list Cache entry (key: `{cache_namespace}:documents:list`).
6. THE Cache_Client SHALL serialize all cached values to JSON before storage and deserialize from JSON on retrieval.
7. IF the Redis connection is unavailable, THEN THE Cache_Client SHALL log a WARNING using the Logger and allow the calling service to proceed without caching, without raising an exception to the caller.
8. IF JSON serialization of a value fails, THEN THE Cache_Client SHALL log a WARNING and skip the cache write without raising an exception to the caller.

---

### Requirement 6: Database Initialization and Schema

**User Story:** As a developer, I want the SQL database schema to be created automatically on application startup, so that no manual migration steps are required to run the application locally.

#### Acceptance Criteria

1. WHEN the application starts, THE migration module SHALL call `Base.metadata.create_all(bind=engine)` to create all ORM-defined tables that do not already exist.
2. WHEN the application starts and the tables already exist, THE System SHALL skip table creation without raising an error.
3. THE document table SHALL define: `id` (integer primary key, auto-increment), `filename` (string, max 255 characters, unique, not null), `file_size` (integer, bytes, not null), `chunk_count` (integer, not null, >= 0), `sync_status` (enum: `OK` or `DELETE_PENDING`, not null, default `OK`), `created_at` (datetime, not null, default to current UTC timestamp).
4. THE chunk table SHALL define: `id` (integer primary key, auto-increment), `document_id` (integer, foreign key to document.id, not null), `chunk_index` (integer, not null, >= 0), `content` (text, not null), `chroma_id` (string, max 255 characters, not null); deleting a Document SHALL cascade-delete all associated Chunk records.
5. THE session table SHALL define: `id` (string, 36 characters, primary key — the UUID `session_id`), `created_at` (datetime, not null, default to current UTC timestamp). A Session record SHALL exist as soon as it is created (Requirement 3.3), independent of whether it has any associated Conversation Turns.
6. THE conversation table SHALL define: `id` (integer primary key, auto-increment), `session_id` (string, max 36 characters, foreign key to session.id, not null, indexed), `role` (enum: `user` or `assistant`, not null), `content` (text, not null), `created_at` (datetime, not null, default to current UTC timestamp); deleting a Session SHALL cascade-delete all associated conversation records.

---

### Requirement 7: Structured Logging and Global Error Handling

**User Story:** As a developer, I want all application events and errors to be logged in a structured format and all unhandled exceptions to return consistent error responses, so that I can diagnose issues efficiently.

#### Acceptance Criteria

1. THE System SHALL use the Loguru Logger for all log output, configured at the log level defined in application settings (default: INFO).
2. WHEN any HTTP request is received, THE System SHALL log the HTTP method, path, and a unique per-request UUID (assigned on arrival) at INFO level.
3. WHEN any HTTP response is sent, THE System SHALL log the HTTP status code, elapsed time in milliseconds, and the same per-request UUID at INFO level.
4. WHEN a handled application error occurs, THE System SHALL log the error code, message, request path, and per-request UUID at ERROR level before returning the error response.
5. WHEN an unhandled exception propagates to the global exception handler, THE System SHALL log the full stack trace at CRITICAL level and return a JSON error response with error code `INTERNAL_SERVER_ERROR` and HTTP status 500.
6. THE error response JSON body SHALL contain: `error_code` (string), `message` (string), and `details` (optional object, may be null).
7. IF a request body fails Pydantic validation, THEN THE System SHALL log the validation failure at WARNING level and return a JSON error response with error code `VALIDATION_ERROR`, HTTP status 422, and `details` populated with per-field validation errors.

---

### Requirement 8: Application Configuration

**User Story:** As a developer, I want all tunable parameters to be configurable via environment variables, so that I can adjust the application's behavior without changing source code.

#### Acceptance Criteria

1. THE System SHALL read configuration values using `pydantic-settings`, with environment variables taking precedence over values defined in the `.env` file.
2. THE configuration SHALL expose the following settings with valid ranges where applicable:
   - `OLLAMA_BASE_URL` (string, required): base URL of the local Ollama server.
   - `OLLAMA_MODEL` (string, required): name of the Ollama model to use.
   - `EMBEDDING_MODEL` (string, optional, default: `all-MiniLM-L6-v2`): sentence-transformers model name.
   - `CHROMA_PERSIST_PATH` (string, optional, default: `./chroma_db`): ChromaDB persistence directory.
   - `REDIS_URL` (string, optional, default: `redis://localhost:6379`): Redis connection URL.
   - `DATABASE_URL` (string, required): SQLAlchemy database connection string.
   - `MAX_CHUNK_SIZE` (integer, 1–2048, optional, default: 512): maximum tokens per chunk.
   - `CHUNK_OVERLAP` (integer, 0–512, optional, default: 50): token overlap between chunks; must be less than `MAX_CHUNK_SIZE`.
   - `TOP_K` (integer, 1–100, optional, default: 5): number of chunks retrieved per query.
   - `CHAT_HISTORY_DEPTH` (integer, 1–50, optional, default: 10): number of conversation turns passed to LLM.
   - `CACHE_TTL_EMBEDDING` (integer, 0–86400, optional, default: 3600): TTL in seconds for cached embeddings.
   - `CACHE_TTL_LLM_RESPONSE` (integer, 0–86400, optional, default: 1800): TTL in seconds for cached one-shot LLM responses (Requirement 2 only).
   - `CACHE_TTL_RETRIEVAL` (integer, 0–86400, optional, default: 900): TTL in seconds for cached chunk retrieval results.
   - `CACHE_TTL_DOCUMENT_LIST` (integer, 0–86400, optional, default: 300): TTL in seconds for the cached document list.
   - `MAX_UPLOAD_SIZE_MB` (integer, optional, default: 50): maximum allowed PDF upload size in megabytes.
   - `LOG_LEVEL` (string, optional, default: `INFO`): Loguru log level.
3. WHEN the application starts and a required configuration value (`OLLAMA_BASE_URL`, `OLLAMA_MODEL`, `DATABASE_URL`) is absent, THE System SHALL halt startup and raise a configuration error identifying the missing setting name.
4. WHEN the application starts with all required settings present, THE System SHALL apply default values for all absent optional settings without raising an error.
5. WHEN the application starts, THE System SHALL derive `cache_namespace` (Requirement 5.4) from the resolved `EMBEDDING_MODEL` and `OLLAMA_MODEL` values, after defaults have been applied.

---

### Requirement 9: Dependency Injection

**User Story:** As a developer, I want all external clients, repositories, and services to be wired together through a single, explicit dependency-injection layer, so that services stay testable, connections are reused correctly, and no component constructs its own dependencies.

#### Acceptance Criteria

1. THE System SHALL define a single dependency-injection module responsible for constructing and wiring: Settings, the SQL engine and session factory, all External Clients (Cache_Client, Chroma_Client, Ollama_Client, Embedder_Client, PDF_Client), all Repos (document, chunk, session, conversation), and all Services (Ingest_Service, Query_Service, Chat_Service, Document_Service). No route handler or service SHALL construct a client or Repo directly.
2. THE Settings object SHALL be constructed exactly once per application process (process-wide singleton) and reused by every component that depends on it, so that Requirement 8's startup validation (8.3) runs exactly once.
3. THE SQL engine and session factory SHALL each be constructed exactly once per application process. A new SQLAlchemy Session SHALL be created per incoming HTTP request and closed when the request completes, regardless of whether the request succeeded or raised an error.
4. THE following External Clients SHALL be constructed exactly once per application process and reused across all requests, because each holds a persistent connection, connection pool, or loaded model: Cache_Client (Redis connection), Chroma_Client (persistent VectorStore handle), Ollama_Client (HTTP client), and Embedder_Client (loaded sentence-transformers model). Constructing a fresh instance of any of these per request SHALL be considered a violation of this requirement, as it would reload models or exhaust connections under load.
5. EACH Repo instance SHALL be constructed per HTTP request and bound to that request's SQL session (Requirement 9.3), so that all repository operations within a single request participate in the same transaction.
6. EACH Service instance (Ingest_Service, Query_Service, Chat_Service, Document_Service) SHALL be constructed per HTTP request from: the process-wide Settings, the process-wide External Clients relevant to that service, and the request-scoped Repos relevant to that service. Chat_Service SHALL receive the session and conversation Repos; Ingest_Service SHALL receive the document and chunk Repos; Document_Service SHALL receive the document and chunk Repos; Query_Service SHALL receive no Repo, since one-shot queries do not read or write SQL state.
7. THE Cache_Client SHALL be constructed with the `cache_namespace` value derived at startup (Requirement 5.4, Requirement 8.5) already applied, so that every cache key it produces is namespaced without requiring each caller to pass the namespace explicitly.
8. Chat_Service's construction SHALL NOT include any LLM-response cache dependency, consistent with Requirement 3.10's prohibition on caching multi-turn LLM responses.
9. THE dependency-injection module SHALL expose each Service as an injectable unit that route handlers declare as a parameter, rather than importing or instantiating the dependency-injection module's internals directly, so that route handlers remain unaware of how a Service's dependencies are constructed.
