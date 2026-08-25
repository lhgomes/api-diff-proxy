.PHONY: install test run docker-build

install:
	pip install -r requirements-dev.txt

test:
	pytest -q

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload

docker-build:
	docker build -t api-diff-proxy .
