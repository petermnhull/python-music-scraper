import pytest
from mock import MagicMock
from selenium import webdriver

from music_scraper.clients.web_driver import WebDriver


TEST_URL = "https://albumwebsite.com/albums"


@pytest.fixture
def web_driver() -> WebDriver:
    selenium_web_driver = MagicMock(spec=webdriver.Chrome)
    selenium_web_driver.get.return_value = None
    selenium_web_driver.page_source = ""
    return WebDriver(selenium_web_driver)


def test_web_driver_get_page_html(web_driver):
    result = web_driver.get_page_html(TEST_URL)
    expected = ""
    assert result == expected
