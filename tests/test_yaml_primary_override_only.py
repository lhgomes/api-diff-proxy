from app.config import load_settings


def test_environment_can_override_only_primary(monkeypatch, tmp_path):
    config = tmp_path / "config.yaml"
    config.write_text("""primary: backend_a
backends:
  backend_a: {url: https://a.example.com}
  backend_b: {url: https://b.example.com}
""", encoding="utf-8")
    monkeypatch.setenv("CONFIG_FILE", str(config))
    monkeypatch.setenv("PRIMARY", "backend_b")
    monkeypatch.delenv("BACKEND_A_URL", raising=False)
    monkeypatch.delenv("BACKEND_B_URL", raising=False)
    settings = load_settings()
    assert settings.primary == "backend_b"
    assert settings.backend_a.url == "https://a.example.com"
