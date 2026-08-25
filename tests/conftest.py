import os

# app.main loads runtime settings during module import. Provide harmless defaults
# for tests that import proxy helpers directly.
os.environ.setdefault("PRIMARY", "backend_a")
os.environ.setdefault("BACKEND_A_URL", "https://a.example.com")
os.environ.setdefault("BACKEND_B_URL", "https://b.example.com")
