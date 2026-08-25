from app.config import load_settings


def test_environment_can_override_one_backend(monkeypatch, tmp_path):
    config = tmp_path / "config.yaml"
    config.write_text("""backends:
  backend_a: {url: https://yaml-a.example.com}
  backend_b: {url: https://yaml-b.example.com}
""", encoding="utf-8")
    monkeypatch.setenv("CONFIG_FILE", str(config))
    monkeypatch.setenv("BACKEND_A_URL", "https://env-a.example.com")
    monkeypatch.delenv("BACKEND_B_URL", raising=False)
    settings = load_settings()
    assert settings.backend_a.url == "https://env-a.example.com"
    assert settings.backend_b.url == "https://yaml-b.example.com"
