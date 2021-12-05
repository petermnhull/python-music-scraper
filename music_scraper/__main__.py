import structlog
from typing import List

from music_scraper.clients import HTTPClient, SpotifyClient
from music_scraper.settings import SpotifyConfig, ScraperConfig
from music_scraper.factories import WebDriverFactory
from music_scraper.album_finders import AlbumFinderBandcamp, AlbumFinderAOTY
from music_scraper.album_processor import AlbumProcessor

_LOGGER = structlog.get_logger(__name__)


def _build_album_finder_bandcamp(
    chrome_driver_path: str, bandcamp_pages: List[int]
) -> AlbumFinderBandcamp:
    factory = WebDriverFactory(chrome_driver_path)
    return AlbumFinderBandcamp(factory, bandcamp_pages)


def _build_album_finder_aoty(http_client: HTTPClient) -> AlbumFinderAOTY:
    return AlbumFinderAOTY(http_client)


def _build_album_processor(
    spotify_client_id: str,
    spotify_client_secret: str,
    chrome_driver_path: str,
    aoty_enabled: bool,
    bandcamp_enabled: bool,
    bandcamp_pages: List[int],
) -> AlbumProcessor:
    http_client = HTTPClient()
    _LOGGER.info("Creating Spotify Client...")
    spotify_client = SpotifyClient(http_client, spotify_client_id, spotify_client_secret)
    album_finders = []
    if aoty_enabled:
        _LOGGER.info("Creating AOTY scraper...")
        album_finders.append(_build_album_finder_aoty(http_client))
    if bandcamp_enabled:
        _LOGGER.info(f"Creating Bandcamp scraper (pages {bandcamp_pages})...")
        album_finders.append(_build_album_finder_bandcamp(chrome_driver_path, bandcamp_pages))
    return AlbumProcessor(album_finders, spotify_client)


if __name__ == "__main__":
    app = _build_album_processor(
        SpotifyConfig.CLIENT_ID,
        SpotifyConfig.CLIENT_SECRET,
        ScraperConfig.CHROME_DRIVER_PATH,
        ScraperConfig.ALBUM_FINDER_AOTY_ENABLED,
        ScraperConfig.ALBUM_FINDER_BANDCAMP_ENABLED,
        ScraperConfig.BANDCAMP_PAGES,
    )
    app.main()
