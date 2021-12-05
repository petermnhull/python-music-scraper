from selenium.webdriver import ChromeOptions, Chrome
from selenium.webdriver.chrome.service import Service

from music_scraper.clients import WebDriver


class WebDriverFactory:
    def __init__(self, chrome_driver_path: str):
        self._chrome_driver_path = chrome_driver_path

    @staticmethod
    def _get_selenium_options() -> ChromeOptions:
        options = ChromeOptions()
        options.add_argument("headless")
        options.add_argument("--no-sandbox")
        return options

    def _build_selenium_driver(self) -> Chrome:
        chrome_service = Service(self._chrome_driver_path)
        driver = Chrome(service=chrome_service, options=self._get_selenium_options())
        return driver

    def build_web_driver(self) -> WebDriver:
        selenium_driver = self._build_selenium_driver()
        return WebDriver(selenium_driver)
