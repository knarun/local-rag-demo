"""
Dependency injection wiring — single source of truth for all injectable components.

This module is the ONLY place where clients, repos, and services are constructed.
No route handler or service is allowed to instantiate its own dependencies directly.

------------------------------------------------------------
PROCESS-WIDE SINGLETONS (constructed once at startup)
------------------------------------------------------------
These are expensive to create and stateful/connection-holding, so they must be
shared across all requests rather than rebuilt per request:

- Settings          : Reads and validates all env vars once (config.py)
- SQL engine        : SQLAlchemy engine (one connection pool per process)
- SessionFactory    : SQLAlchemy sessionmaker bound to the engine
- CacheClient       : Redis connection (holds a persistent connection pool)
- ChromaClient      : ChromaDB persistent handle (holds open file/store)
- OllamaClient      : httpx.AsyncClient connection pool to Ollama server
- EmbedderClient    : Loaded sentence-transformers model (expensive to load)
- PDFClient         : Stateless, but constructed once for consistency

------------------------------------------------------------
REQUEST-SCOPED DEPENDENCIES (constructed per HTTP request)
------------------------------------------------------------
These are cheap to create and must be bound to the current request's DB session:

- get_db_session    : Yields a new SQLAlchemy Session, closes it after response
- get_document_repo : DocumentRepo bound to the current request's DB session
- get_chunk_repo    : ChunkRepo bound to the current request's DB session
- get_session_repo  : SessionRepo bound to the current request's DB session
- get_conversation_repo : ConversationRepo bound to the current request's DB session

------------------------------------------------------------
SERVICE INJECTORS (constructed per HTTP request from singletons + request repos)
------------------------------------------------------------
Each service receives only the clients and repos it actually needs:

- get_ingest_service    : IngestService(settings, pdf_client, embedder_client,
                          chroma_client, cache_client, document_repo, chunk_repo)

- get_query_service     : QueryService(settings, embedder_client, chroma_client,
                          ollama_client, cache_client)
                          NOTE: No repos — one-shot queries do not touch SQL state.

- get_chat_service      : ChatService(settings, embedder_client, chroma_client,
                          ollama_client, cache_client, session_repo, conversation_repo)
                          NOTE: Does NOT receive a cache dependency for LLM responses
                          (multi-turn responses must never be cached — see Req 3.10).

- get_document_service  : DocumentService(settings, chroma_client, cache_client,
                          document_repo, chunk_repo)

------------------------------------------------------------
USAGE IN ROUTE HANDLERS
------------------------------------------------------------
Route handlers declare services as FastAPI Depends parameters only.
They never import or call this module's internals directly:

    @router.post("/ingest")
    async def ingest(
        file: UploadFile,
        service: IngestService = Depends(get_ingest_service)
    ):
        return await service.ingest(file)
"""
