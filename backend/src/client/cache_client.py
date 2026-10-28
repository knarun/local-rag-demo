"""
Redis cache client wrapper.

Responsibilities:
- Connects to Redis at the configured REDIS_URL on startup (process-wide singleton)
- Derives and stores the cache_namespace from EMBEDDING_MODEL + OLLAMA_MODEL at construction time
- get(key)           : Returns the deserialized (JSON → Python object) cached value, or None if missing/expired
- set(key, value, ttl) : Serializes value to JSON and stores it in Redis with the given TTL
- delete(key)        : Removes a specific cache entry (used for document list invalidation)
- build_key(cache_type, *inputs) : Constructs a namespaced key:
                                   {cache_namespace}:{cache_type}:{sha256(deterministic_inputs)}
- Gracefully degrades: logs a WARNING and returns None/no-ops if Redis is unavailable,
  never raising an exception to the caller
- Logs a WARNING and skips the write if JSON serialization fails
"""
