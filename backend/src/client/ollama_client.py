"""
Ollama HTTP client wrapper.

Responsibilities:
- Wraps the ollama Python SDK for communication with the local Ollama server
- chat()     : Send a list of messages (role + content) and return the assistant response text
               Used by Chat_Service for multi-turn conversation
- generate() : Send a single prompt and return the generated response text
               Used by Query_Service for one-shot question answering
- Both methods apply tenacity retry logic up to MAX_RETRY_ATTEMPTS on failure
- Raises a specific exception (LLM_UNAVAILABLE) after all retries are exhausted

Note:
- Must be constructed once per process (process-wide singleton) because it holds
  a persistent httpx.AsyncClient connection pool
"""
