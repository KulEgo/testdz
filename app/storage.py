class Storage:
    def __init__(self):
        self._data = {}

    def add_link(self, short_link, original_url):
        self._data[short_link] = original_url

    def get_link(self, short_link):
        return self._data.get(short_link)
