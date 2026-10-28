"""
Application configuration.

Responsibilities:
- Defines the Settings class using pydantic-settings
- Reads all environment variables from the .env file and the process environment
- Environment variables take precedence over .env file values
- Exposes all tunable parameters: Ollama URL/model, embedding model, ChromaDB path,
  Redis URL, database URL, chunk size/overlap, top-K, chat history depth,
  cache TTLs, max upload size, log level, and max retry attempts
- Raises a startup error if any required setting (OLLAMA_BASE_URL, OLLAMA_MODEL,
  DATABASE_URL) is missing
- Applies default values for all optional settings
- Derives and exposes the cache_namespace from EMBEDDING_MODEL + OLLAMA_MODEL
  for use by the Cache_Client
"""
