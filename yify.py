import requests
import constants
from request import request


class Yify():
    def __init__(self):
        self.mode=constants.DL_MODE_YIFY
        self.endpoint = constants.YIFY_ENDPOINT
        self.session = requests.Session()
        self.user_agent = '{appid}/{version}'.format(
            appid=constants.APP_ID,
            version=constants.APP_VERSION)

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

    def do_query(self, **kwargs):
        # Format the params
        params = {
        }

        if 'genre' in kwargs:
            params['genre'] = ';'.join(
                [str(c) for c in kwargs['genre']])
            del kwargs['genre']

        for key, value in kwargs.items():
            if key not in [
                    'page', 'limit',
                    'quality', 'minimum_rating',
                    'query_term', 'genre',
                    'sort_by', 'order_by'
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

            limit:  
                    type:       integer unsigned
                    values:     [1-50]
                    default:    20
                    meaning:    number of results retrieved

            page:   
                    type:       integer unsigned
                    default:    1
                    meaning:    pagination of the <limit> results

            quality:
                    type:       constant string
                    values:     720p, 1080p, 2160p, 3D
                    default:    none
                    meaning:    quality of the searched movie

            minimum_rating:
                    type:       integer unsigned
                    values:     [1-10]
                    default:    none
                    meaning:    filter movies by imdb rating

            query_term:
                    type:       string
                    values:     any
                    default:    none
                    meaning:    query to filter results

            genre:
                    type:       string
                    values:     any
                    default:    ALL
                    meaning:    query genre by http://www.imdb.com/genre/

            sort_by:
                    type:       string
                    values:     title, year, rating, peers, 
                                seeds, download_count, like_count,  date_added
                    default:    date_added
                    meaning:    result sorting condition

            order_by:
                    type:       string
                    values:     asc,desc
                    default:    desc
                    meaning:    sort_by conditional order
        """

        return self.do_query(**kwargs)
