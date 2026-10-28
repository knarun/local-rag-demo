"""
Pytest shared fixtures.

Fixtures defined here are available to all tests under backend/tests/.

Fixtures:
- db_session     : Provides an in-memory SQLite session with all tables created,
                   rolled back after each test to ensure isolation
- mock_chroma    : MagicMock for Chroma_Client — stubs add(), query(), delete()
- mock_ollama    : MagicMock for Ollama_Client — stubs chat() and generate()
- mock_embedder  : MagicMock for Embedder_Client — stubs embed() and embed_batch()
- mock_cache     : MagicMock for Cache_Client — stubs get(), set(), delete(), build_key()
- mock_pdf       : MagicMock for PDF_Client — stubs validate() and extract()
- test_client    : FastAPI TestClient with all external clients overridden via DI
"""
