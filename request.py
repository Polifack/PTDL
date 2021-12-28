import constants
import time

from torrent import Torrent


def json_hook(dct):
    if 'download' in dct:
        return Torrent(dct)
    return dct


def request(func):
    '''
        Wrapper that makes a request retry itself until a 
        constant-defined number of attempts is reached.

        Also sleeps between each request.
    '''

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
