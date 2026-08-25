import pytest

from app.config import load_settings


def test_missing_config_file_fails_clearly(monkeypatch):
    monkeypatch.setenv("CONFIG_FILE", "/does/not/exist/config.yaml")
    with pytest.raises(FileNotFoundError):
        load_settings()
