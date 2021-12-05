# python-music-scraper
Python service for finding new music.

This consists a collection of web scrapers to find new music that is available to listen to on Spotify.

I started this project to automate my habit of scrolling through Bandcamp for finding releases that don't show up on Spotify's front page.

## Dependencies
- Spotify API which requires a Spotify Developer account.
- Chrome Driver
- Docker with Docker Compose.

## Usage
Create a `.env` file in the root directory with the following variables:

|Variable                  |Detail                                                  |
|--------------------------|--------------------------------------------------------|
|`SPOTIFY_CLIENT_ID`       |Spotify Client ID                                       |
|`SPOTIFY_CLIENT_SECRET`   |Spotify Client Secret                                   |
|`CHROME_DRIVER_PATH`      |Relative path to Chrome driver for Selenium             |
|`BANDCAMP_SCRAPER_ENABLED`|Feature flag for Bandcamp scraper (true/false)          |
|`AOTY_SCRAPER_ENABLED`    |Feature flag for albumoftheyear.org scraper (true/false)|

Then run the following:
- `make run` to run the scraper.
- `make test` to run the test suite.
- `make coverage` to run the test suite with a coverage report.
- `make black` to apply automated code formatting.
- `make lint` to apply flake8 linting rules.
- `make build` to build the Docker image for the scraper.
- `make rund` to build and run the scrapers in Docker.

### Notes
- This has been developed and tested on Ubuntu 20.04.
- If you have issues with installing a Chrome Driver or with local Python dependencies, running the app in Docker should work out of the box.

## To Do & Ideas for Improvement
- Publish songs to make them available for other services to consume from.
- Add RYM album finder.
- Improve the matching algorithm, e.g. introduce fuzzy matching on artist names.

