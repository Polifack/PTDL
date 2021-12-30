import constants
import time
import json
import sys
import multiprocessing
import urllib.parse
from torrent import Torrent


def waiting():
    start_string = "[*] Processing"
    wait_strings = ["",".","..","..."]
    ctr = 0
    while True:
        time.sleep(1)
        idx=ctr%4
        print(start_string+wait_strings[idx],end="\r")
        ctr+=1


def parse_body_rarbg(dct):
    result = []
    for torrent in (dct['torrent_results']):
        title = torrent['title'] 
        download = torrent['download']
        seeders = torrent['seeders']
        leechers = torrent['leechers']
        size = "{0:.2f} GB".format(((torrent['size'])/(1024**3)))
        pubdate = torrent['pubdate']

        result.append(Torrent(download, title, size, pubdate, seeders, leechers))
    
    return result


def parse_body_yify(dct):
    result = []
    for element in (dct):
        for torrent in element['torrents']:
            # build title
            title = element['title_long']+":"+torrent['quality']+"-"+torrent['type']
            
            # build magnet link
            #magnet = magnet:?xt=urn:btih:<hash>&dn=<url_encoded movie name>&tr=<tr1>&tr=<tr2>
            url_encoded_movie_name = urllib.parse.quote_plus(element['title_long'])
            torrent_hash=torrent['hash']
            trackers_string = ""
            for tracker in constants.YIFY_TRACKERS:
                trackers_string+="&tr="+tracker

            download = "magnet:?xt=urn:btih:"+torrent_hash+"&dn="+url_encoded_movie_name+trackers_string
            
            seeders = torrent['seeds']
            leechers = torrent['peers']
            size = torrent['size']
            pubdate = torrent['date_uploaded']

            result.append(Torrent(download, title, size, pubdate, seeders, leechers))
    
    return result


def request(func):
    '''
        Wrapper that makes a request retry itself until a 
        constant-defined number of attempts is reached.

        Also sleeps between each request.
    '''

    def wrapper(self, *args, **kwargs):
        max_retries = constants.CONNECTION_RETRIES
        retries = 0

        wait_process = multiprocessing.Process(target = waiting)
        wait_process.start()

        while retries < max_retries:
            time.sleep(constants.RETRY_TIME)
            try:
                resp = func(self, *args, **kwargs)
                body = json.loads(resp.content)
                
                if (self.mode == constants.DL_MODE_RARBG):
                    if ("error_code" not in body.keys()):
                        wait_process.terminate()
                        print("[*] Results found")
                        return parse_body_rarbg(body)
                    else:
                        retries += 1
                        continue

                elif (self.mode == constants.DL_MODE_YIFY) :
                    if (body['data']['movie_count']>0):
                        wait_process.terminate()
                        return parse_body_yify(body['data']['movies'])
                    else:
                        wait_process.terminate()
                        print("[!] No movies found")
                        return None

            except Exception as exp:
                print('[!] Unexpected exception', exp)
        wait_process.terminate()
    return wrapper
