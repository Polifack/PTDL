import rarbg
import yify
import sys
import subprocess
import webbrowser

import constants

if __name__ == "__main__":
    print("[*] Starting")

    client = None
    results = None
    client = sys.argv[1]
    query = sys.argv[2]

    if client == "-yify":
        print("[*] Querying yify")
        client = yify.Yify()
        results = client.search(query_term=query)
    
    if client == "-rarbg":
        print("[*] Querying rarbg")
        client = rarbg.Rarbg()
        results = client.search(search_string=query)

    if client == None:
        print("[!] Error: No torrent source found")
        print("[!] Please specify source with -<source>")
        exit()

    if results == None:
        print("[!] Error: No results found")
        exit()

    ctr = 0
    dict = []
    print("{:-<102}".format(""))

    print("[{:2}] | {:50} | {:10} | {:10} | {:6} | {:6} |".format(
        "id", "filename", "up date", "size ", "seed", "leech"))

    print("{:-<102}".format(""))

    for item in results:

        t_file = item.filename[0:50]
        t_size = item.size
        t_date = item.pubdate
        t_seed = item.seeders
        t_lech = item.leechers

        print("[{:2}] | {:50} | {:.10} | {:10} | {:6} | {:6} |".format(
            str(ctr), t_file, t_date, t_size, t_seed, t_lech))

        dict.append(item.download)
        ctr += 1

    dl = input("[*] input download number: ")
    magnet = dict[int(dl)]
    subprocess.Popen(['xdg-open', magnet],
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
