from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from music_scraper.clients.exceptions import WebDriverFailure

DRIVER_DEFAULT_LOADING_TIME = 0


class WebDriver:
    """
    Heavy web driver to scrape Javascript-heavy websites that
    aren't accessible with the HTTP Client alone.

    Wraps external Selenium library.
    """

    def __init__(self, driver: webdriver.Chrome):
        self._driver = driver

    def _ensure_page_loads(self) -> None:
        self._driver.maximize_window()
        self._driver.implicitly_wait(DRIVER_DEFAULT_LOADING_TIME)

    def get_page_html(self, url: str) -> str:
        try:
            self._driver.get(url)
        except WebDriverException as err:
            raise WebDriverFailure(f"web driver failed: {str(err)}")
        self._ensure_page_loads()
        html = self._driver.page_source
        self._driver.close()
        return html
