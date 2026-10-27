.PHONY: install dev run test lint seed docker docker-run

install:
	python -m pip install -r requirements.txt

dev:
	python -m pip install -r requirements-dev.txt

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest -q --cov=app --cov-report=term-missing

lint:
	ruff check .

seed:
	python scripts/seed_sample_docs.py

docker:
	docker build -t agent-trust-control-plane:local .

docker-run: docker
	docker run --rm -p 8000:8000 agent-trust-control-plane:local
