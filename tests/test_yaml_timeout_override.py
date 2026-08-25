from app.config import load_settings


def test_timeout_environment_overrides_yaml(monkeypatch, tmp_path):
    config = tmp_path / "config.yaml"
    config.write_text("""backends:
  backend_a: {url: https://a.example.com}
  backend_b: {url: https://b.example.com}
proxy:
  timeout_seconds: 60
""", encoding="utf-8")
    monkeypatch.setenv("CONFIG_FILE", str(config))
    monkeypatch.setenv("TIMEOUT_SECONDS", "5")
    monkeypatch.delenv("BACKEND_A_URL", raising=False)
    monkeypatch.delenv("BACKEND_B_URL", raising=False)
    assert load_settings().timeout_seconds == 5
