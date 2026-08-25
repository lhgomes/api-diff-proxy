from app.config import load_settings


def test_default_ignored_headers(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")
    settings = load_settings()
    assert "date" in settings.comparison.ignore_headers
    assert "server" in settings.comparison.ignore_headers
    assert "content-length" in settings.comparison.ignore_headers
