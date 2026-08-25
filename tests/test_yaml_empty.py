import pytest

from app.config import load_settings


def test_empty_yaml_still_requires_backend_urls(monkeypatch, tmp_path):
    config = tmp_path / "config.yaml"
    config.write_text("", encoding="utf-8")
    monkeypatch.setenv("CONFIG_FILE", str(config))
    monkeypatch.delenv("BACKEND_A_URL", raising=False)
    monkeypatch.delenv("BACKEND_B_URL", raising=False)
    with pytest.raises(ValueError):
        load_settings()
