run:
	poetry run gunicorn --reload

format:
	black src
	poetry run ruff . --fix