from typing import Iterator, List
import structlog

from music_scraper.clients import SpotifyClient
from music_scraper.clients.exceptions import SpotifyRecordNotFound
from music_scraper.album_finders import AlbumFinderBase
from music_scraper.models import Album, Song


_LOGGER = structlog.get_logger(__name__)


class AlbumProcessor:
    def __init__(
        self,
        album_finders: List[AlbumFinderBase],
        spotify_client: SpotifyClient,
    ):
        self._album_finders = album_finders
        self._spotify_client = spotify_client

    def _find_albums(self) -> Iterator[Album]:
        _LOGGER.info("Starting to scrape websites for new albums...")
        for album_finder in self._album_finders:
            _LOGGER.info(f"Starting to scrape {album_finder.get_url()}...")
            for album in album_finder.get_albums():
                yield album
            _LOGGER.info("Finished scraping" f" {album_finder.get_url()} for new albums.")
        _LOGGER.info("Finished scraping websites for now...")

    def _get_songs_from_album(self, album: Album) -> Iterator[Song]:
        try:
            for song in self._spotify_client.get_songs_from_album(album):
                yield song
        except SpotifyRecordNotFound as err:
            _LOGGER.warning(str(err))

    def main(self):
        for album in self._find_albums():
            for song in self._get_songs_from_album(album):
                _LOGGER.info(f"Found song: {str(song)}")
        _LOGGER.info("Task complete.")
