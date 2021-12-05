import pytest
import os
from mock import MagicMock
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from freezegun import freeze_time
from datetime import datetime

from music_scraper.album_finders.album_finder_bandcamp import AlbumFinderBandcamp
from music_scraper.clients import WebDriver
from music_scraper.models import Album
from music_scraper.factories import WebDriverFactory

MOCK_BANDCAMP_RESPONSE_PATH = os.path.join(
    "tests", "album_finders", "response_album_finder_bandcamp.txt"
)


@pytest.fixture
def album_finder_bandcamp() -> AlbumFinderBandcamp:
    selenium_web_driver = MagicMock(spec=webdriver.Chrome)
    with open(MOCK_BANDCAMP_RESPONSE_PATH) as f:
        response_text = f.read()
    selenium_web_driver.get.return_value = None
    selenium_web_driver.page_source = response_text
    web_driver = WebDriver(selenium_web_driver)

    web_driver_factory = MagicMock(spec=WebDriverFactory)
    web_driver_factory.build_web_driver.return_value = web_driver

    album_finder_bandcamp = AlbumFinderBandcamp(web_driver_factory, [0])
    return album_finder_bandcamp


@freeze_time("2021-01-01")
def test_album_finder_get_albums(album_finder_bandcamp: AlbumFinderBandcamp):

    albums = list(album_finder_bandcamp.get_albums())

    assert len(albums) == 8
    assert albums[0] == Album(
        "Ominous Forest", ["Psuchag\\xc5\\x8dgoi"], "album", datetime(2021, 1, 1)
    )
    assert albums[7] == Album(
        "Sun Rockabillies Volume 1", ["Various Artists"], "album", datetime(2021, 1, 1)
    )


def test_album_finder_get_albums_failure_non_blocking(album_finder_bandcamp: AlbumFinderBandcamp):
    selenium_web_driver = MagicMock(spec=webdriver.Chrome)
    selenium_web_driver.get.side_effect = WebDriverException
    web_driver = WebDriver(selenium_web_driver)
    album_finder_bandcamp._driver_factory.build_web_driver.return_value = web_driver
    albums = list(album_finder_bandcamp.get_albums())
    assert len(albums) == 0
