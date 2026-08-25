from app.config import load_settings


def test_log_level_is_normalized(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")
    monkeypatch.setenv("LOG_LEVEL", "debug")
    assert load_settings().log_level == "DEBUG"
