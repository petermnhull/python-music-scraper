#!make

run:
	pipenv run python3 -m music_scraper

test:
	pipenv run coverage run --source music_scraper/ -m pytest

build:
	docker-compose build scraper

rund: build
	docker-compose up scraper

coverage: test
	pipenv run coverage report

black:
	pipenv run black . --line-length=100

lint:
	pipenv run flake8 . --max-line-length=100
