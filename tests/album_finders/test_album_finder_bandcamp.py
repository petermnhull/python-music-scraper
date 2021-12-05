import pytest
import os
from mock import MagicMock
from selenium import webdriver
from freezegun import freeze_time
from datetime import datetime

from music_scraper.album_finders.album_finder_bandcamp import AlbumFinderBandcamp
from music_scraper.clients import WebDriver
from music_scraper.models import Album

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
    album_finder_bandcamp = AlbumFinderBandcamp(web_driver, [0])
    return album_finder_bandcamp


@freeze_time("2021-01-01")
def test_album_finder_get_albums(album_finder_bandcamp: AlbumFinderBandcamp):

    albums = list(album_finder_bandcamp.get_albums())

    album_finder_bandcamp._web_driver._driver.get.assert_called_once_with(
        "https://bandcamp.com/?g=all&s=new&p=0&gn=0&f=all&w=-1"
    )
    assert len(albums) == 8
    assert albums[0] == Album(
        "Ominous Forest", ["Psuchag\\xc5\\x8dgoi"], "album", datetime(2021, 1, 1)
    )
    assert albums[7] == Album(
        "Sun Rockabillies Volume 1", ["Various Artists"], "album", datetime(2021, 1, 1)
    )
