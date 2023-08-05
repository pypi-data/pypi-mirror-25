# aiospotify [![PyPI version](https://badge.fury.io/py/aiospotify.svg)](https://badge.fury.io/py/aiospotify) ![BuildStatus](https://travis-ci.org/jdr023/aiospotify.svg?branch=master) [![Coverage Status](https://coveralls.io/repos/github/jdr023/aiospotify/badge.svg?branch=master)](https://coveralls.io/github/jdr023/aiospotify?branch=master) [![CodeFactor](https://www.codefactor.io/repository/github/jdr023/aiospotify/badge)](https://www.codefactor.io/repository/github/jdr023/aiospotify)
A Python wrapper for Spotify's [Web API](https://developer.spotify.com/web-api/). It's request-agnostic, so it should easily integrate into your project's design.

Install
-------
This wrapper uses Python 3.6. You can download the release [here](https://www.python.org/downloads/release/python-360/).
```Bash
$ pip install aiospotify
```

Usage
-----
Each method requires a `token`, which can be obtained after creating a Spotify [application](https://developer.spotify.com/my-applications/#!/) and making an instance of Aiospotify with your app's credentials.

Using aiohttp:
```Python
from aiospotify import Aiospotify

client = Aiospotify(client_id='CLIENT_ID', client_secret='CLIENT_SECRET')    
token = await client.init_auth()

# Search for an album by its name
search_results = await client.search('abbey road', token, type='album')

# Search for a specific track by its Spotify ID
track = await client.search_track('3n3Ppam7vgaVa1iaRUc9Lp', token)
```
Using requests:
```Python
from aiospotify import Aiospotify, connectors

client = Aiospotify(client_id='CLIENT_ID', 
                    client_secret='CLIENT_SECRET', 
                    connector=connectors.ReqConnector())    
token = client.init_auth()

# Search for an artist by their name
search_results = client.search('death grips', token, type='artist')
```
Methods return dictionary objects defined by Spotify's [object model](https://developer.spotify.com/web-api/object-model/).

Contribute
----------
Feel free to open an [Issue](https://github.com/jdr023/aiospotify/issues/new) or submit PRs.
