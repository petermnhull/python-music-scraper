import structlog
from selenium import webdriver

from music_scraper.album_processor import AlbumProcessor
from music_scraper.album_finders import (
    AlbumFinderAOTY,
    AlbumFinderBandcamp,
)
from music_scraper.clients import HTTPClient, WebDriver, SpotifyClient
from music_scraper.settings import SpotifyConfig, ScraperConfig

_LOGGER = structlog.get_logger(__name__)


def _build_selenium_driver(chrome_driver_path: str) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("--no-sandbox")
    selenium_driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)
    return selenium_driver


def _build_album_processor() -> AlbumProcessor:
    http_client = HTTPClient()

    _LOGGER.info("Intialising Spotify Client...")
    spotify_client = SpotifyClient(
        http_client,
        SpotifyConfig.CLIENT_ID,
        SpotifyConfig.CLIENT_SECRET,
    )

    album_finders = []
    if ScraperConfig.ALBUM_FINDER_AOTY_ENABLED:
        _LOGGER.info("Creating AOTY scraper...")
        album_finder_aoty = AlbumFinderAOTY(http_client)
        album_finders.append(album_finder_aoty)
    if ScraperConfig.ALBUM_FINDER_BANDCAMP_ENABLED:
        _LOGGER.info("Creating Bandcamp scraper...")
        selenium_driver = _build_selenium_driver(ScraperConfig.CHROME_DRIVER_PATH)
        web_driver = WebDriver(selenium_driver)
        album_finder_bandcamp = AlbumFinderBandcamp(web_driver, ScraperConfig.BANDCAMP_PAGES)
        album_finders.append(album_finder_bandcamp)

    app = AlbumProcessor(album_finders, spotify_client)
    return app


if __name__ == "__main__":
    app = _build_album_processor()
    app.main()
