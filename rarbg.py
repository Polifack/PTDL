import time
import requests
import constants


class Torrent():
    '''
    brief
    {
        "filename":"Off.Piste.2016.iNTERNAL.BDRip.x264-LiBRARiANS",
        "category":"Movies/x264",
        "download":"magnet:..."
    }

    extended
    {
        "title":"Off.Piste.2016.iNTERNAL.BDRip.x264-LiBRARiANS",
        "category":"Movies/x264",
        "download":"magnet:...",
        "seeders":12,
        "leechers":6,
        "size":504519520,
        "pubdate":"2017-05-21 02:13:49 +0000",
    }
    '''

    def __init__(self, mapping):
        self._raw = mapping
        self.category = self._raw['category']
        self.download = self._raw['download']
        self.filename = self._raw.get('filename') or self._raw.get('title')
        self.size = (self._raw.get('size')/1024**3)
        self.pubdate = self._raw.get('pubdate')
        self.seeders = self._raw.get('seeders')
        self.leechers = self._raw.get('leechers')

    def __getattr__(self, key):
        value = self._raw.get(key)
        if value is None:
            raise AttributeError('%s not exists' % key)
        return value


def json_hook(dct):
    if 'download' in dct:
        return Torrent(dct)
    return dct


def request(func):
    def wrapper(self, *args, **kwargs):
        max_retries = constants.CONNECTION_RETRIES
        retries = 0
        while retries < max_retries:
            time.sleep(constants.RETRY_TIME)
            print("[*] Attempt ", retries)
            try:
                resp = func(self, *args, **kwargs)
                body = resp.json(object_hook=json_hook)

                error_code = body.get('error_code')
                if error_code:
                    print("[!] Error code returned: ", body)
                    retries += 1
                    continue
                elif 'torrent_results' not in body:
                    print("[!] No Torrent Results in Body", body)
                    retries += 1
                    continue
                else:
                    print("[*] Results found")
                    return body['torrent_results']
            except Exception as exp:
                print('[!] Unexpected exception %s', exp)
    return wrapper


class Rarbg():
    def __init__(self):
        self.endpoint = constants.RARBG_ENDPOINT
        self.session = requests.Session()
        self.user_agent = '{appid}/{version}'.format(
            appid=constants.APP_ID,
            version=constants.APP_VERSION)
        self.token = self.get_token()

    def get_token(self):
        params = {
            'get_token': 'get_token'
        }
        resp = self.do_request('GET', self.endpoint, params)
        content = resp.json()
        print("[*] Token adquiered: ", content['token'])
        return content['token']

    def do_request(self, method, url, params=None):
        if not params:
            params = dict()

        params.update({
            'app_id': constants.APP_ID
        })

        headers = {
            'user-agent': self.user_agent
        }

        prepared_request = requests.Request(
            method, url, params=params, headers=headers).prepare()
        resp = self.session.send(prepared_request)
        resp.raise_for_status()

        return resp

    def do_query(self, mode, **kwargs):
        # Format the params
        params = {
            'mode': mode,
            'token': self.token,
            'format': 'json_extended'
        }

        if 'categories' in kwargs:
            params['category'] = ';'.join(
                [str(c) for c in kwargs['categories']])
            del kwargs['categories']

        for key, value in kwargs.items():
            if key not in [
                    'sort', 'limit',
                    'search_string'
            ]:
                raise ValueError('unsupported parameter %s' % key)

            if value is None:
                continue

            params[key] = value

        # Do query request
        return self.do_request('GET', self.endpoint, params)

    @request
    def search(self, **kwargs):
        """
        Search torrents.

        sort: (optional) sort torrents, possibile values are
                'seeders', 'leechers' or 'last'
        limit: (optional) limit how many torrents will be returned,
                possibile values are 25, 50 or 100
        categories: (optional) what kind of torrents should be
                searched, categories should be a list of int
        search_string: (optional)
        extended_response: (optional) return full context of torrent,
                default is False

        :returns: a list of Torrents

        :raises: ValueError
        """
        return self.do_query('search', **kwargs)
