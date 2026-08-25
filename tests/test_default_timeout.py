from app.config import load_settings


def test_default_timeout_is_thirty_seconds(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.delenv("TIMEOUT_SECONDS", raising=False)
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")
    assert load_settings().timeout_seconds == 30.0
