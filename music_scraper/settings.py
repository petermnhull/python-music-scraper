import os


class SpotifyConfig:
    CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
    CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
