import rarbg
import sys
import subprocess
import webbrowser

import constants

if __name__ == "__main__":
    print("[*] Starting")

    query = sys.argv[1]
    client = rarbg.Rarbg()
    results = client.search(search_string=query)

    if results == None:
        print("[!] Error: No results found after %d retries",
              constants.CONNECTION_RETRIES)
        exit()

    ctr = 0
    dict = []
    print("{:-<100}".format(""))

    print("[{:2}] | {:50} | {:10} | {:8} | {:6} | {:6} |".format(
        "id", "filename", "up date", "size ", "seed", "leech"))

    print("{:-<100}".format(""))

    for item in results:

        t_file = item.filename[0:50]
        t_size = item.size
        t_date = item.pubdate
        t_seed = item.seeders
        t_lech = item.leechers

        print("[{:2}] | {:50} | {:.10} | {:05.2f} GB | {:6} | {:6} |".format(
            str(ctr), t_file, t_date, t_size, t_seed, t_lech))

        dict.append(item.download)
        ctr += 1

    dl = input("[*] input download number: ")
    magnet = dict[int(dl)]
    subprocess.Popen(['xdg-open', magnet],
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
