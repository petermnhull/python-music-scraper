from typing import Iterator, Union
from bs4 import BeautifulSoup
from datetime import datetime as dt

from music_scraper.clients import HTTPClient
from music_scraper.album_finders.album_finder_base import AlbumFinderBase
from music_scraper.models import Album


class AlbumFinderAOTY(AlbumFinderBase):
    def __init__(self, http_client: HTTPClient):
        self._url = "https://www.albumoftheyear.org/releases"
        self._http_client = http_client

    def get_url(self) -> str:
        return self._url

    @staticmethod
    def _get_element_from_album(album: BeautifulSoup, element: str) -> Union[str, None]:
        value = album.find("div", {"class": element})
        if value is None:
            return ""
        return value.get_text()

    @staticmethod
    def _create_album(title: str, artist: str) -> Album:
        album = Album(
            title=title,
            artists=[artist],
            release_type="album",
            found_at=dt.utcnow(),
        )
        return album

    def _create_album_from_soup(self, album_soup: BeautifulSoup) -> Album:
        title = self._get_element_from_album(album_soup, "albumTitle")
        artist = self._get_element_from_album(album_soup, "artistTitle")
        return self._create_album(title, artist)

    def get_albums(self) -> Iterator[Album]:
        response = self._http_client.do_get(self._url)
        soup = BeautifulSoup(response.text, "html.parser")
        albums_soup = soup.findAll("div", {"class": "albumBlock"})
        for album_soup in albums_soup:
            album = self._create_album_from_soup(album_soup)
            yield album
