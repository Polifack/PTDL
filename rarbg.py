import requests
import constants
from request import request


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
