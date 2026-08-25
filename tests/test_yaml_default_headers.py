from app.config import load_settings


def test_yaml_without_comparison_uses_default_ignored_headers(monkeypatch, tmp_path):
    config = tmp_path / "config.yaml"
    config.write_text("""backends:
  backend_a: {url: https://a.example.com}
  backend_b: {url: https://b.example.com}
""", encoding="utf-8")
    monkeypatch.setenv("CONFIG_FILE", str(config))
    monkeypatch.delenv("BACKEND_A_URL", raising=False)
    monkeypatch.delenv("BACKEND_B_URL", raising=False)
    assert load_settings().comparison.ignore_headers == ["date", "server", "content-length"]
