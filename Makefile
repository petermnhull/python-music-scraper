#!make

run:
	pipenv run python3 -m music_scraper

test:
	pipenv run pytest

black:
	pipenv run black . --line-length=100

lint:
	pipenv run flake8 . --max-line-length=100
