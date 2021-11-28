# python-music-scraper
Python service for finding new music.

This consists a collection of web scrapers to find new music that is available to listen to on Spotify.

## Dependencies
- Spotify API which requires a Spotify Developer account.

## Usage
Create a `.env` file in the root directory with the following variables:
- `SPOTIFY_CLIENT_SECRET`
- `SPOTIFY_CLIENT_ID`

Then run the following:
- `make run` to run the scraper.
- `make test` to run the test suite.
- `make black` to apply automated code formatting.
- `make lint` to apply flake8 linting rules.

## To Do
- Publish songs to make them available for other services.
- Add Bandcamp album finder.
- Add RYM album finder.

## Area to Improve
- Improve the matching algorithm, e.g. introduce fuzzy matching on artist names.
