import pytest

from app.config import load_settings


def test_invalid_timeout_fails_configuration(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")
    monkeypatch.setenv("TIMEOUT_SECONDS", "invalid")
    with pytest.raises(ValueError):
        load_settings()
