from app.config import load_settings


def test_minimum_configuration_is_two_backend_urls(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.delenv("PRIMARY", raising=False)
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")
    settings = load_settings()
    assert settings.primary == "backend_a"
