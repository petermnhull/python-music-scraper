import pytest
from typing import Dict

from music_scraper.clients import HTTPClient


@pytest.fixture
def http_client() -> HTTPClient:
    return HTTPClient()


@pytest.mark.parametrize(
    "headers, expected",
    [
        (
            {},
            {
                "User-Agent": "Mozilla/5.0 "
                "(X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
                "Accept-Encoding": "gzip, deflate",
                "Accept": "*/*",
                "Connection": "keep-alive",
            },
        ),
        (
            {"Addition-Header": "123abc"},
            {
                "User-Agent": "Mozilla/5.0 "
                "(X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
                "Accept-Encoding": "gzip, deflate",
                "Accept": "*/*",
                "Connection": "keep-alive",
                "Addition-Header": "123abc",
            },
        ),
        (
            {"Addition-Header": "123abc", "Connection": "keep-not-alive"},
            {
                "User-Agent": "Mozilla/5.0 "
                "(X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
                "Accept-Encoding": "gzip, deflate",
                "Accept": "*/*",
                "Connection": "keep-not-alive",
                "Addition-Header": "123abc",
            },
        ),
    ],
)
def test_http_client_enhance_headers(http_client: HTTPClient, headers: Dict, expected: Dict):
    print(http_client._enhance_headers(headers))
    assert http_client._enhance_headers(headers) == expected
