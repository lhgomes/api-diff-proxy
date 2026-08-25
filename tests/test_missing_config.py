import pytest

from app.config import load_settings


def test_backend_urls_are_required(monkeypatch):
    monkeypatch.delenv("CONFIG_FILE", raising=False)
    monkeypatch.delenv("BACKEND_A_URL", raising=False)
    monkeypatch.delenv("BACKEND_B_URL", raising=False)
    monkeypatch.setenv("PRIMARY", "backend_a")

    with pytest.raises(ValueError, match="BACKEND_A_URL and BACKEND_B_URL are required"):
        load_settings()
