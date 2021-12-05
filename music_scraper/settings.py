import os


class SpotifyConfig:
    CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
    CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")


class ScraperConfig:
    CHROME_DRIVER_PATH = os.environ.get("CHROME_DRIVER_PATH")

    ALBUM_FINDER_BANDCAMP_ENABLED = (
        os.environ.get("BANDCAMP_SCRAPER_ENABLED", "False").lower() == "true"
    )
    BANDCAMP_PAGES = [0]

    ALBUM_FINDER_AOTY_ENABLED = os.environ.get("AOTY_SCRAPER_ENABLED", "True").lower() == "true"
