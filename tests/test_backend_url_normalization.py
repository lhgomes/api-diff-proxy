from app.config import load_settings


def test_backend_trailing_slash_is_removed(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com///")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com/")
    settings = load_settings()
    assert settings.backend_a.url == "https://a.example.com"
    assert settings.backend_b.url == "https://b.example.com"
