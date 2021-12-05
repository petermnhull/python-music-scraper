from typing import Iterator, List
from bs4 import BeautifulSoup
from datetime import datetime

from music_scraper.models import Album
from music_scraper.album_finders.album_finder_base import AlbumFinderBase
from music_scraper.clients import WebDriver


BANDCAMP_URL_TEMPLATE = "?g={}&s=new&p={}&gn=0&f=all&w={}"


class AlbumFinderBandcamp(AlbumFinderBase):
    def __init__(self, web_driver: WebDriver, pages: List[int]):
        self._url = "https://bandcamp.com/"
        self._web_driver = web_driver
        self._pages = pages

    def get_url(self) -> str:
        return self._url

    def _create_album_from_soup(self, album_soup: BeautifulSoup) -> Album:
        title = album_soup.find("a", attrs={"item-title"}).get_text()
        artist = album_soup.find("a", attrs={"item-artist"}).get_text()
        return Album(title, [artist], "album", datetime.utcnow())

    def _find_albums_in_soup(self, soup: BeautifulSoup) -> Iterator[Album]:
        album_soups = soup.findAll("div", attrs={"class": "col col-3-12 discover-item"})
        for album_soup in album_soups:
            album = self._create_album_from_soup(album_soup)
            if album.title != "" and len(album.artists) > 0:
                yield album

    def _process_response(self, page_html: str) -> Iterator[Album]:
        soup = BeautifulSoup(page_html, "html.parser")
        return self._find_albums_in_soup(soup)

    def _get_albums_from_url(self, url: str) -> Iterator[Album]:
        page_html = self._web_driver.get_page_html(url)
        return self._process_response(page_html)

    def _get_page_url(self, page: int) -> str:
        return self._url + BANDCAMP_URL_TEMPLATE.format("all", page, -1)

    def get_albums(self) -> Iterator[Album]:
        for i in self._pages:
            url = self._get_page_url(i)
            for album in self._get_albums_from_url(url):
                yield album
