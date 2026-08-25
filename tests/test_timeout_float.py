from app.config import load_settings


def test_fractional_timeout(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")
    monkeypatch.setenv("TIMEOUT_SECONDS", "0.5")
    assert load_settings().timeout_seconds == 0.5
