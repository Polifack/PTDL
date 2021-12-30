# PythonTorrentDownLoader

Python script for searching and downloading totally legal torrents. Currently only supports RARBG and YIFY torrents.

## Usage

```bash
$ python main.py -<query_site> "torrent_query"

where query site is [rarbg | yify]
```

## Considerations

### Request Limit

RARBG queries usually takes some attempts due to server overload.
By default the script only retries the query for RARBG Torrents 20 times, if more retries needed change the value in const.py.

### YIFY Site

YIFY Only allows download for movies.
If the query in YIFY does not answer any data we assume that the movie is not uploaded yet or does not exist.

## Future Work

Integration with Piratebay, Nyaa, Kickasstorrent and 1377x

## License
[GPL-3](https://www.gnu.org/licenses/gpl-3.0.en.html)