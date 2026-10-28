"""
Chat service — business logic for session-aware multi-turn conversation.

Responsibilities:
- Validates the incoming message (non-empty, within 2000 character limit)
- Checks that the VectorStore contains chunks before any session work begins
- Creates a new Session record in the SQL database when no session_id is provided
- Validates an existing session_id against the SQL database
- Retrieves the last N conversation turns (ordered ascending) from conversation_repo
- Embeds the current message (cache-first via Cache_Client / Embedder_Client)
- Retrieves top-K relevant chunks from Chroma (cache-first via Cache_Client / Chroma_Client)
- Constructs a prompt: retrieved chunks as context + conversation history + current message
- Calls Ollama_Client directly — LLM responses are NOT cached for multi-turn chat
- Persists both the user message and assistant response as Conversation Turns on success
- Does NOT persist the user message if the LLM call fails after all retries
"""
