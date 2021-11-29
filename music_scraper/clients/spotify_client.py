from typing import Dict, Iterator, List
import time
import structlog
from urllib.parse import quote
import requests


from music_scraper.clients.http_client import HTTPClient
from music_scraper.clients.exceptions import (
    SpotifyTemporaryFailure,
    SpotifyAnalysisNotFound,
    SpotifyUnhandledError,
    SpotifyRecordNotFound,
)
from music_scraper.models import (
    Album,
    Song,
    SpotifyAlbumSearchResult,
    SpotifyAlbumTracksResult,
    SpotifyAlbumTrack,
)


SPOTIFY_BASE_URL = "https://api.spotify.com/v1/"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_DEFAULT_RETRY_AFTER = 1


_LOGGER = structlog.get_logger(__name__)


class SpotifyClient:
    def __init__(
        self,
        http_client: HTTPClient,
        client_id: str,
        client_secret: str,
    ):
        self._client_id = client_id
        self._client_secret = client_secret
        self._http_client = http_client
        self._set_headers()

    @staticmethod
    def _process_token_response(response: requests.Response) -> str:
        response_data = response.json()
        return response_data["access_token"]

    def _get_token(self) -> str:
        data = {"grant_type": "client_credentials"}
        auth = (self._client_id, self._client_secret)
        response = self._http_client.do_post(SPOTIFY_TOKEN_URL, data, {}, auth)
        return self._process_token_response(response)

    def _set_headers(self) -> None:
        token = self._get_token()
        self._headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }

    @staticmethod
    def _handle_not_found_error(response: requests.Response) -> None:
        response_data = response.json()
        error = response_data.get("error", None)
        if error:
            message = error.get("message", None)
            if message == "analysis not found":
                raise SpotifyAnalysisNotFound("analysis not found")

    def _raise_for_error(self, response: requests.Response) -> None:
        status_code = response.status_code
        if status_code == 503 or status_code == 504 or status_code == 401:
            raise SpotifyTemporaryFailure(f"spotify temporarily unavailable ({status_code})")
        if status_code == 404:
            self._handle_not_found_error(response)
        if status_code == 429:
            raise SpotifyTemporaryFailure("spotify rate limit hit")
        raise SpotifyUnhandledError(f"unhandled {status_code} error")

    def _process_get_response(
        self, response: requests.Response, expected_status_code=200
    ) -> requests.Response:
        if response.status_code != expected_status_code:
            self._raise_for_error(response)
        return response

    def _get(self, url: str) -> requests.Response:
        response = self._http_client.do_get(url, self._headers)
        return self._process_get_response(response)

    def _handle_temporary_failure(self, err: Exception) -> None:
        _LOGGER.warning(f"temporary failure: {str(err)}")
        self._set_headers()
        time.sleep(SPOTIFY_DEFAULT_RETRY_AFTER)

    def _get_data_with_retry(self, url: str) -> Dict:
        try:
            response = self._get(url)
        except SpotifyTemporaryFailure as err:
            self._handle_temporary_failure(err)
            return self._get_data_with_retry(url)
        return response.json()

    @staticmethod
    def _find_matching_album_id_from_search_result(
        search_result: SpotifyAlbumSearchResult, album: Album
    ) -> str:
        album_id = search_result.find_matching_album_id(album)
        if not album_id:
            raise SpotifyRecordNotFound(f"no matching spotify album found for '{str(album)}'")
        return album_id

    def _process_album_search_response_data(self, response_data: Dict, album: Album) -> str:
        search_result = SpotifyAlbumSearchResult.parse_obj(response_data)
        return self._find_matching_album_id_from_search_result(search_result, album)

    @staticmethod
    def _get_album_search_url(album: Album) -> str:
        album_query_string = quote(album.title + " " + " ".join(album.artists))
        url = SPOTIFY_BASE_URL + f"search?q={album_query_string}&type=album"
        return url

    def _get_album_id(self, album: Album) -> str:
        url = self._get_album_search_url(album)
        response_data = self._get_data_with_retry(url)
        return self._process_album_search_response_data(response_data, album)

    @staticmethod
    def _process_album_tracks_response_data(response_data: Dict) -> List[SpotifyAlbumTrack]:
        search_result = SpotifyAlbumTracksResult.parse_obj(response_data)
        return search_result.items

    def _get_tracks_from_album_id(self, album_id: str) -> List[SpotifyAlbumTrack]:
        url = SPOTIFY_BASE_URL + f"albums/{album_id}/tracks"
        response_data = self._get_data_with_retry(url)
        return self._process_album_tracks_response_data(response_data)

    def get_songs_from_album(self, album: Album) -> Iterator[Song]:
        album_id = self._get_album_id(album)
        for track in self._get_tracks_from_album_id(album_id):
            yield Song.from_spotify_track(track, album_id)
