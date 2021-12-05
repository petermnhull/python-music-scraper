from selenium import webdriver
import time

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
        time.sleep(DRIVER_DEFAULT_LOADING_TIME)

    def get_page_html(self, url: str) -> str:
        self._driver.get(url)
        self._ensure_page_loads()
        return self._driver.page_source
