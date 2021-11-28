from typing import Iterator, Union
import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt

from music_scraper.clients import HTTPClient
from music_scraper.album_finders.album_finder_base import AlbumFinderBase
from music_scraper.album_finders.exceptions import (
    AlbumFinderPageNotFound,
    AlbumFinderUnhandledResponseError,
)
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

    def _create_album_from_soup(self, album_soup: BeautifulSoup) -> Album:
        title = self._get_element_from_album(album_soup, "albumTitle")
        artist = self._get_element_from_album(album_soup, "artistTitle")
        return Album(title, [artist], "album", dt.utcnow())

    def _find_albums_in_soup(self, soup: BeautifulSoup) -> Iterator[Album]:
        for album_soup in soup.findAll("div", {"class": "albumBlock"}):
            yield self._create_album_from_soup(album_soup)

    def _process_response(self, response: requests.Response) -> Iterator[Album]:
        soup = BeautifulSoup(response.text, "html.parser")
        return self._find_albums_in_soup(soup)

    def _raise_for_error(self, response: requests.Response) -> None:
        if response.status_code == 200:
            return
        if response.status_code == 404:
            raise AlbumFinderPageNotFound(f"page not found: {self.get_url()}")
        raise AlbumFinderUnhandledResponseError(f"unhandled error ({response.status_code})")

    def get_albums(self) -> Iterator[Album]:
        response = self._http_client.do_get(self._url)
        self._raise_for_error(response)
        return self._process_response(response)
