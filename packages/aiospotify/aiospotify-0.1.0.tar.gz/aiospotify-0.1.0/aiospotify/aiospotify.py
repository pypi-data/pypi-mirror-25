from . import endpoints
from . import connectors


class Aiospotify:
    """Spotify API client.
    
    Parameters
    ----------
    client_id
        The client credentials provided by Spotify after registering an application.
    client_secret
        ”
    connector
        The Aiospotify connector used for making requests. 
        :class:`aiospotify.connectors.AioConnector` uses an asyncio/aiohttp implementation 
        and is used by default. :class:`aiospotify.ReqConnector uses requests.`
    """
    def __init__(self, client_id, client_secret, connector=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.connector = connector or connectors.AioConnector()

    def init_auth(self):
        """Request an access token using the given credentials."""
        return self.connector.fetch(endpoints.AUTH_URL,
                                    {'grant_type': 'client_credentials',
                                     'client_id': self.client_id,
                                     'client_secret': self.client_secret})

    def search(self, query, token, type='track', limit=10):
        """Get Spotify catalog information about artists, albums, tracks,
        or playlists that match a keyword string.
        
        Parameters
        ----------
        query
            The search query's keywords.
        type
            The type of item to search for, one of 'album', 'artist', 
            'playlist' or 'track'. Defaults to 'track'.
        token
            Credentials obtained from init_auth.
        limit
            The maximum number of results to return.
        """
        # Encode spaces
        query = query.replace(' ', '+')
        return self.connector.fetch(endpoints.SEARCH_URL.format(query, type, limit),
                                    {'Authorization': f'Bearer {token}'})

    def search_track(self, id_, token):
        """Get Spotify catalog information for a single track by its id.
        
        Parameters
        ----------
        id_
            The unique Spotify track id.
        token
            Credentials obtained from init_auth.
        """
        return self.connector.fetch(endpoints.TRACK_URL.format(id_),
                                    {'Authorization': f'Bearer {token}'})

    def search_tracks(self, ids: list, token):
        """Get catalog information for a list of tracks by their ids.

        Parameters
        ----------
        ids
            A list of Spotify track ids.
        token
            Credentials obtained from init_auth.
        """
        # Produce a comma-separated list of ids
        track_ids = '?ids=' + ','.join(ids)
        return self.connector.fetch(endpoints.TRACK_URL.format(track_ids),
                                    {'Authorization': f'Bearer {token}'})

    def search_album(self, id_, token):
        """Get Spotify catalog information for a single album by its id.
        
        Parameters
        ----------
        id_
            The unique Spotify album id.
        token
            Credentials obtained from init_auth.
        """
        return self.connector.fetch(endpoints.ALBUM_URL.format(id_),
                                    {'Authorization': f'Bearer {token}'})

    def search_albums(self, ids: list, token):
        """Get catalog information for a list of albums by their ids.

        Parameters
        ----------
        ids
            A list of Spotify album ids.
        token
            Credentials obtained from init_auth.
        """
        # Produce a comma-separated list of ids
        album_ids = '?ids=' + ','.join(ids)
        return self.connector.fetch(endpoints.ALBUM_URL.format(album_ids),
                                    {'Authorization': f'Bearer {token}'})

    def search_artist(self, id_, token):
        """Get Spotify catalog information for a single artist by their id.

        Parameters
        ----------
        id_
            The unique Spotify artist id.
        token
            Credentials obtained from init_auth.
        """
        return self.connector.fetch(endpoints.ARTIST_URL.format(id_),
                                    {'Authorization': f'Bearer {token}'})

    def search_artists(self, ids: list, token):
        """Get catalog information for a list of artists by their ids.

        Parameters
        ----------
        ids
            A list of Spotify artist ids.
        token
            Credentials obtained from init_auth.
        """
        # Produce a comma-separated list of ids
        artist_ids = '?ids=' + ','.join(ids)
        return self.connector.fetch(endpoints.ARTIST_URL.format(artist_ids),
                                    {'Authorization': f'Bearer {token}'})

    def search_playlist(self, pid, uid, token):
        """Get Spotify catalog information for a user's playlist.

        Parameters
        ----------
        pid
            The unique Spotify playlist id.
        uid
            The username of the owner of the playlist.
        token
            Credentials obtained from init_auth.
        """
        return self.connector.fetch(endpoints.PLAYLIST_URL.format(uid, pid),
                                    {'Authorization': f'Bearer {token}'})


if __name__ == '__main__':
    print('Aiospotify should be imported into a project.')
