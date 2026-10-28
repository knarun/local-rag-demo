"""
Integration tests for ConversationRepo against an in-memory SQLite database.

Tests:
- Insert a Conversation Turn and verify it is persisted with correct role and content
- Retrieve last N turns ordered by created_at ascending
- Returns empty list for a session with no turns
- Retrieving more turns than exist returns all available turns (no error)
- Turns from different sessions are not mixed
"""
