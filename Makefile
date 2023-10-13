run:
	poetry run python src/dragon-analyzer/main.py

format:
	black src
	poetry run ruff . --fix