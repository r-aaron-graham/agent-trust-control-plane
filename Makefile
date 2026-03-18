.PHONY: install run test seed

install:
	python -m pip install -r requirements.txt

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest -q

seed:
	python scripts/seed_sample_docs.py
