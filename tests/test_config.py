import pytest

from app.config import load_settings


def test_environment_only_configuration(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("PRIMARY", "backend_b")
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com/")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com/")

    settings = load_settings()

    assert settings.primary == "backend_b"
    assert settings.backend_a.url == "https://a.example.com"
    assert settings.backend_b.url == "https://b.example.com"


def test_invalid_primary(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.setenv("PRIMARY", "invalid")
    monkeypatch.setenv("BACKEND_A_URL", "https://a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://b.example.com")

    with pytest.raises(ValueError, match="PRIMARY"):
        load_settings()
