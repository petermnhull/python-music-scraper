from typing import Iterator, List
from bs4 import BeautifulSoup
from datetime import datetime
import structlog

from music_scraper.models import Album
from music_scraper.album_finders.album_finder_base import AlbumFinderBase
from music_scraper.album_finders.exceptions import AlbumFinderPageNotFound
from music_scraper.clients import WebDriver
from music_scraper.clients.exceptions import WebDriverFailure
from music_scraper.factories import WebDriverFactory

BANDCAMP_URL_BASE = "https://bandcamp.com/"
BANDCAMP_URL_TEMPLATE = "?g={}&s=new&p={}&gn=0&f=all&w={}"


_LOGGER = structlog.get_logger(__name__)


class AlbumFinderBandcamp(AlbumFinderBase):
    def __init__(self, driver_factory: WebDriverFactory, pages: List[int]):
        self._url = BANDCAMP_URL_BASE
        self._driver_factory = driver_factory
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
            else:
                _LOGGER.warning("skipping album with insufficient data")

    def _process_response(self, page_html: str) -> Iterator[Album]:
        soup = BeautifulSoup(page_html, "html.parser")
        return self._find_albums_in_soup(soup)

    def _get_albums_from_url(self, url: str, web_driver: WebDriver) -> Iterator[Album]:
        try:
            page_html = web_driver.get_page_html(url)
        except WebDriverFailure as err:
            raise AlbumFinderPageNotFound(f"page not found due to web driver failure: {str(err)}")
        return self._process_response(page_html)

    def _get_page_url(self, page: int) -> str:
        return self._url + BANDCAMP_URL_TEMPLATE.format("all", page, -1)

    def _get_albums_from_page(self, page: int) -> Iterator[Album]:
        url = self._get_page_url(page)
        web_driver = self._driver_factory.build_web_driver()
        return self._get_albums_from_url(url, web_driver)

    def get_albums(self) -> Iterator[Album]:
        for page in self._pages:
            _LOGGER.info(f"Searching Bandcamp page {page} for albums...")
            try:
                for album in self._get_albums_from_page(page):
                    yield album
            except AlbumFinderPageNotFound as err:
                _LOGGER.warning(f"skipping page {page}: {str(err)}")
