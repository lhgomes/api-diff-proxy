from app.config import load_settings


def test_yaml_timeout(monkeypatch, tmp_path):
    config = tmp_path / "config.yaml"
    config.write_text("""backends:
  backend_a: {url: https://a.example.com}
  backend_b: {url: https://b.example.com}
proxy:
  timeout_seconds: 45
""", encoding="utf-8")
    monkeypatch.setenv("CONFIG_FILE", str(config))
    monkeypatch.delenv("TIMEOUT_SECONDS", raising=False)
    monkeypatch.delenv("BACKEND_A_URL", raising=False)
    monkeypatch.delenv("BACKEND_B_URL", raising=False)
    assert load_settings().timeout_seconds == 45.0
