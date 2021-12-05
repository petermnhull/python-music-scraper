import pytest
from mock import MagicMock
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from music_scraper.clients.web_driver import WebDriver
from music_scraper.clients.exceptions import WebDriverFailure

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
    web_driver._driver.close.assert_called()


def test_web_driver_get_page_html_failure(web_driver):
    web_driver._driver.get.side_effect = WebDriverException
    with pytest.raises(WebDriverFailure):
        web_driver.get_page_html("")
