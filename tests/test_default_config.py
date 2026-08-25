from app.config import load_settings


def test_defaults(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.delenv("PRIMARY", raising=False)
    monkeypatch.delenv("TIMEOUT_SECONDS", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")
    settings = load_settings()
    assert settings.primary == "backend_a"
    assert settings.timeout_seconds == 30
    assert settings.log_level == "INFO"
