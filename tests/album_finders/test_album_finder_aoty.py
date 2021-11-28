import pytest
from mock import MagicMock
import os
import datetime
from freezegun import freeze_time

from music_scraper.album_finders import AlbumFinderAOTY
from music_scraper.clients import HTTPClient
from music_scraper.models import Album
from tests.helpers import MockResponse


MOCK_AOTY_RESPONSE_PATH = os.path.join("tests", "album_finders", "response_album_finder_aoty.txt")


@pytest.fixture
def album_finder_aoty() -> AlbumFinderAOTY:
    http_client = MagicMock(spec=HTTPClient)
    with open(MOCK_AOTY_RESPONSE_PATH) as f:
        response_text = f.read()

    http_client.do_get.return_value = MockResponse(response_text, 200)
    return AlbumFinderAOTY(http_client)


@freeze_time("2021-01-01")
def test_album_finder_aoty_get_albums(album_finder_aoty: AlbumFinderAOTY):
    albums = list(album_finder_aoty.get_albums())
    assert len(albums) == 66

    expected_album = Album(
        title="Henki",
        artists=["Richard Dawson & Circle"],
        release_type="album",
        found_at=datetime.datetime(2021, 1, 1),
    )
    assert albums[0] == expected_album
