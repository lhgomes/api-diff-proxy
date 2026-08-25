from app.config import load_settings


def test_timeout_environment_setting(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")
    monkeypatch.setenv("TIMEOUT_SECONDS", "12.5")
    settings = load_settings()
    assert settings.timeout_seconds == 12.5
