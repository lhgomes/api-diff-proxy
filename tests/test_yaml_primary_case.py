from app.config import load_settings


def test_yaml_primary_is_case_insensitive(monkeypatch, tmp_path):
    config = tmp_path / "config.yaml"
    config.write_text("""primary: BACKEND_B
backends:
  backend_a: {url: https://a.example.com}
  backend_b: {url: https://b.example.com}
""", encoding="utf-8")
    monkeypatch.setenv("CONFIG_FILE", str(config))
    monkeypatch.delenv("PRIMARY", raising=False)
    monkeypatch.delenv("BACKEND_A_URL", raising=False)
    monkeypatch.delenv("BACKEND_B_URL", raising=False)
    assert load_settings().primary == "backend_b"
