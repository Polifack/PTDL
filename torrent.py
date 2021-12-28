class Torrent():
    '''
    attributes
    {
        "title: Title of the file from the torrent"
        "category: Category where the torrent is"
        "download: Magnet Link"
        "seeders: Seeders of the torrent"
        "leechers: Leechers of the torrent"
        "size: Filesize in GB"
        "pubdate: Date that the torrent was indexed"
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
