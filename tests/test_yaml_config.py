from app.config import load_settings


def test_yaml_configuration(monkeypatch, tmp_path):
    config = tmp_path / "config.yaml"
    config.write_text("""primary: backend_b
backends:
  backend_a:
    url: https://a.example.com
  backend_b:
    url: https://b.example.com
proxy:
  timeout_seconds: 15
comparison:
  ignore_json_paths:
    - $.requestId
""", encoding="utf-8")

    monkeypatch.setenv("CONFIG_FILE", str(config))
    monkeypatch.delenv("PRIMARY", raising=False)
    monkeypatch.delenv("BACKEND_A_URL", raising=False)
    monkeypatch.delenv("BACKEND_B_URL", raising=False)
    monkeypatch.delenv("TIMEOUT_SECONDS", raising=False)

    settings = load_settings()
    assert settings.primary == "backend_b"
    assert settings.timeout_seconds == 15
    assert settings.comparison.ignore_json_paths == ["$.requestId"]
