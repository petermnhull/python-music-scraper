import pytest
from mock import MagicMock
from typing import Union, Dict, List
import json

from music_scraper.models import Album, Song
from music_scraper.clients import SpotifyClient, HTTPClient
from music_scraper.clients.exceptions import (
    SpotifyTemporaryFailure,
    SpotifyAnalysisNotFound,
    SpotifyUnhandledError,
    SpotifyRecordNotFound,
)
from tests.helpers import MockResponse, MOCK_ALBUM_ONE

MOCK_SPOTIFY_ENDPOINT = "https://mock.spotify.com/v1"


@pytest.fixture
def spotify_client() -> SpotifyClient:
    http_client = MagicMock(spec=HTTPClient)
    http_client.do_post.return_value = MockResponse('{"access_token": "999aaa"}', 200)
    return SpotifyClient(http_client, "123abc", "789xyz")


def test_spotify_client_init(spotify_client: SpotifyClient):
    expected_headers = {
        "Accept": "application/json",
        "Authorization": "Bearer 999aaa",
        "Content-Type": "application/json",
    }
    assert spotify_client._headers == expected_headers


@pytest.mark.parametrize(
    "status_code, response_data, expected",
    [
        (200, {}, "{}"),
        (429, {}, SpotifyTemporaryFailure),
        (503, {}, SpotifyTemporaryFailure),
        (504, {}, SpotifyTemporaryFailure),
        (404, {}, SpotifyUnhandledError),
        (404, {"error": {"message": "analysis not found"}}, SpotifyAnalysisNotFound),
    ],
)
def test_spotify_client_get_temporary_failure(
    spotify_client: SpotifyClient,
    status_code: int,
    response_data: Dict,
    expected: Union[str, Exception],
):
    spotify_client._http_client.do_get.return_value = MockResponse(
        json.dumps(response_data), status_code
    )
    if isinstance(expected, str):
        response = spotify_client._get(MOCK_SPOTIFY_ENDPOINT)
        assert response.status_code == status_code
        assert response.text == expected
    else:
        with pytest.raises(expected):
            spotify_client._get(MOCK_SPOTIFY_ENDPOINT)


@pytest.mark.parametrize(
    "album, response_data, expected",
    [
        (MOCK_ALBUM_ONE, {"albums": {"items": []}}, SpotifyRecordNotFound),
        (
            MOCK_ALBUM_ONE,
            {"albums": {"items": [{"id": "xyz999", "artists": [{"name": "not the artist"}]}]}},
            SpotifyRecordNotFound,
        ),
        (
            MOCK_ALBUM_ONE,
            {"albums": {"items": [{"id": "123abc", "artists": [{"name": "Random Collaborator"}]}]}},
            "123abc",
        ),
        (
            MOCK_ALBUM_ONE,
            {
                "albums": {
                    "items": [
                        {"id": "yyy000", "artists": [{"name": "someone else"}]},
                        {
                            "id": "123abc",
                            "artists": [{"name": "someone else"}, {"name": "Random Collaborator"}],
                        },
                    ]
                }
            },
            "123abc",
        ),
    ],
)
def test_spotify_get_album_id(
    spotify_client: SpotifyClient,
    album: Album,
    response_data: Dict,
    expected: Union[str, Exception],
):
    spotify_client._http_client.do_get.return_value = MockResponse(json.dumps(response_data), 200)
    if isinstance(expected, str):
        album_id = spotify_client._get_album_id(album)
        assert album_id == expected
    else:
        with pytest.raises(expected):
            spotify_client._get_album_id(album)


@pytest.mark.parametrize(
    "album, album_search_response, album_tracks_response, expected",
    [
        (
            MOCK_ALBUM_ONE,
            {"albums": {"items": [{"id": "123abc", "artists": [{"name": "Firstname Lastname"}]}]}},
            {
                "items": [
                    {
                        "id": "111zzz",
                        "name": "track one",
                        "artists": [{"name": "Firstname Lastname"}, {"name": "Someone Else"}],
                    },
                    {
                        "id": "999aaa",
                        "name": "track two",
                        "artists": [{"name": "Firstname Lastname"}],
                    },
                ],
                "total": 2,
            },
            [
                Song("track one", ["Firstname Lastname", "Someone Else"], "123abc", "111zzz"),
                Song("track two", ["Firstname Lastname"], "123abc", "999aaa"),
            ],
        ),
    ],
)
def test_spotify_get_songs_from_album(
    spotify_client: SpotifyClient,
    album: Album,
    album_search_response: Dict,
    album_tracks_response: Dict,
    expected: List[Song],
):
    mock_response_album_search = MockResponse(json.dumps(album_search_response), 200)
    mock_response_album_tracks = MockResponse(json.dumps(album_tracks_response), 200)
    spotify_client._http_client.do_get.side_effect = [
        mock_response_album_search,
        mock_response_album_tracks,
    ]
    assert list(spotify_client.get_songs_from_album(album)) == expected
