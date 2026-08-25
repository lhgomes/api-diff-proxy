from app.config import load_settings


def test_environment_overrides_yaml(monkeypatch, tmp_path):
    config = tmp_path / "config.yaml"
    config.write_text("""primary: backend_a
backends:
  backend_a:
    url: https://yaml-a.example.com
  backend_b:
    url: https://yaml-b.example.com
""", encoding="utf-8")

    monkeypatch.setenv("CONFIG_FILE", str(config))
    monkeypatch.setenv("PRIMARY", "backend_b")
    monkeypatch.setenv("BACKEND_A_URL", "https://env-a.example.com")
    monkeypatch.setenv("BACKEND_B_URL", "https://env-b.example.com")

    settings = load_settings()
    assert settings.primary == "backend_b"
    assert settings.backend_a.url == "https://env-a.example.com"
    assert settings.backend_b.url == "https://env-b.example.com"
