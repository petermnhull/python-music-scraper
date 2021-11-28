import pytest
from typing import Dict

from music_scraper.models import Album
from music_scraper.models.spotify_album_search import (
    SpotifyAlbumSearchResult,
    SpotifyAlbum,
)
from tests.helpers import (
    MOCK_ALBUM_SEARCH_MAP,
    MOCK_SEARCH_MODEL_ALBUMS_RESULT,
    MOCK_SEARCH_MODEL_ALBUM,
    MOCK_ALBUM_ONE,
    MOCK_ALBUM_TWO,
)


@pytest.mark.parametrize(
    "spotify_album, album, expected",
    [
        (MOCK_SEARCH_MODEL_ALBUM, MOCK_ALBUM_ONE, True),
        (MOCK_SEARCH_MODEL_ALBUM, MOCK_ALBUM_TWO, False),
    ],
)
def test_spotify_album_matches(spotify_album: SpotifyAlbum, album: Album, expected: bool):
    assert spotify_album.album_matches(album) == expected


@pytest.mark.parametrize(
    "input_data, expected",
    [
        (MOCK_ALBUM_SEARCH_MAP, MOCK_SEARCH_MODEL_ALBUMS_RESULT),
    ],
)
def test_spotify_album_search_result_parses(input_data: Dict, expected: SpotifyAlbumSearchResult):
    assert SpotifyAlbumSearchResult.parse_obj(input_data) == expected


@pytest.mark.parametrize(
    "album_results, album, expected",
    [
        (MOCK_SEARCH_MODEL_ALBUMS_RESULT, MOCK_ALBUM_ONE, "123abc"),
        (MOCK_SEARCH_MODEL_ALBUMS_RESULT, MOCK_ALBUM_TWO, ""),
    ],
)
def test_spotify_album_search_result_find_matching_album_id(
    album_results: SpotifyAlbumSearchResult, album: Album, expected: str
):
    assert album_results.find_matching_album_id(album) == expected
