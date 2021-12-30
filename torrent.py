class Torrent():
    '''
    attributes
    {
        "title: Title of the file from the torrent"
        "download: Magnet Link"
        "seeders: Seeders of the torrent"
        "leechers: Leechers of the torrent"
        "size: Filesize in GB"
        "pubdate: Date that the torrent was indexed"
    }
    '''

    def __init__(self, dl, fn, s, pd, sd, lc):
        self.download = dl
        self.filename = fn
        self.size = s
        self.pubdate = pd
        self.seeders = sd
        self.leechers = lc

    def __getattr__(self, key):
        value = self._raw.get(key)
        if value is None:
            raise AttributeError('%s not exists' % key)
        return value
