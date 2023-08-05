from . import endpoints

try:
    import aiohttp
    import asyncio

    class AioConnector:
        """Asynchronous connector using aiohttp/asyncio."""
        def __init__(self, session=None, loop=None):
            self.loop = loop or asyncio.get_event_loop()
            self.session = session or aiohttp.ClientSession(loop=self.loop)

        def __del__(self):
            self.session.close()

        async def _make_req(self, endpoint, data):
            """Makes an API request to Spotify.
            
            Parameters
            ----------
            endpoint
                The endpoint to send the request, either an authorization
                uri when requesting an access token or a url for the Web API.
            data
                The data to send to the endpoint, either a payload for the
                Web API or an authorization header to request an access token.
            """
            if endpoint == endpoints.AUTH_URL:
                response = await self.session.post(endpoint, data=data)
            else:
                response = await self.session.get(endpoint, headers=data)
            return response

        @staticmethod
        async def wrap(endpoint, response):
            """Helper function for formatting data from specific endpoints.

            Parameters
            ----------
            endpoint
                The source of the response.
            response
                The data received after making a request.
            """
            data = await response.json()
            if endpoint == endpoints.AUTH_URL:
                return data['access_token']
            if 'v1/search' in endpoint:
                type_ = next(iter(data))
                return data[type_]['items']
            if '?ids=' in endpoint:
                type_ = next(iter(data))
                return data[type_]
            return data

        async def fetch(self, endpoint, data, retries=3):
            """Send and process a request to Spotify.
            
            Parameters
            ----------
            endpoint
                The HTTP/HTTPS endpoint where the request is sent.
            data
                The dictionary of data to send to the endpoint.
            retries
                The number of times to retry the request upon failure.
            """
            while retries:
                response = await self._make_req(endpoint, data)
                if response.status == 200:
                    data = await self.wrap(endpoint, response)
                    return data
                # Retry on Gateway Timeout error
                if response.status == 504:
                    await asyncio.sleep(1)
                    retries -= 1
                else:
                    break
except ImportError as e:
    raise Exception('You must install `aiohttp` and `asyncio` to use AioConnector.') from e

try:
    import time
    import requests

    class ReqConnector:
        """Alternative connector using requests."""

        def __init__(self, session=None):
            self.session = session or requests.session()

        def __del__(self):
            self.session.close()

        def _make_req(self, endpoint, data):
            """Makes an API request to Spotify.

            Parameters
            ----------
            endpoint
                The endpoint to send the request, either an authorization
                uri when requesting an access token or a url for the Web API.
            data
                The data to send to the endpoint, either a payload for the
                Web API or an authorization header to request an access token.
            """
            if endpoint == endpoints.AUTH_URL:
                response = self.session.post(endpoint, data=data)
            else:
                response = self.session.get(endpoint, headers=data)
            return response

        @staticmethod
        def wrap(endpoint, response):
            """Helper function for formatting data from specific endpoints.

            Parameters
            ----------
            endpoint
                The source of the response.
            response
                The data received after making a request.
            """
            data = response.json()
            if endpoint == endpoints.AUTH_URL:
                return data['access_token']
            if 'v1/search' in endpoint:
                type_ = next(iter(data))
                return data[type_]['items']
            if '?ids=' in endpoint:
                type_ = next(iter(data))
                return data[type_]
            return data

        def fetch(self, endpoint, data, retries=3):
            """Send and process a POST request to Spotify.

            Parameters
            ----------
            endpoint
                The HTTP/HTTPS endpoint where the request is sent.
            data
                The dictionary of data to send to the endpoint.
            retries
                The number of times to retry the request upon failure.
            """
            while retries:
                response = self._make_req(endpoint, data)
                if response.status_code == 200:
                    return self.wrap(endpoint, response)
                # Retry on Gateway Timeout error
                elif response.status_code == 504:
                    time.sleep(1)
                    retries -= 1
                else:
                    break
except ImportError as e:
    raise Exception('You must install `requests` to use ReqConnector.') from e
