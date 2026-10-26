.PHONY: dev test lint build up down

dev:
	PYTHONPATH=src /Users/precisiontech/xxGEMEENTExx/.venv/bin/streamlit run src/main.py

test:
	pytest tests/

lint:
	black --check src/
	flake8 src/

up:
	docker-compose up -d

down:
	docker-compose down
