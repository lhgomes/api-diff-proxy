import pytest

from app.config import load_settings


def test_invalid_yaml_primary_is_rejected(monkeypatch, tmp_path):
    config = tmp_path / "config.yaml"
    config.write_text("""primary: other
backends:
  backend_a: {url: https://a.example.com}
  backend_b: {url: https://b.example.com}
""", encoding="utf-8")
    monkeypatch.setenv("CONFIG_FILE", str(config))
    monkeypatch.delenv("PRIMARY", raising=False)
    monkeypatch.delenv("BACKEND_A_URL", raising=False)
    monkeypatch.delenv("BACKEND_B_URL", raising=False)
    with pytest.raises(ValueError, match="PRIMARY"):
        load_settings()
