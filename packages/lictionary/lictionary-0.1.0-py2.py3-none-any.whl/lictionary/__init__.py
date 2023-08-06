class Lictionary(object):
    __slots__ = ('_items',)

    def __init__(self, items=None):
        self._items = items or []

    def append(self, item):
        self._items.append(item)

    @property
    def items(self):
        return self._items

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._items[key]
        else:
            # TODO(nicholasbishop): simple implementation for now, not
            # efficient for large number of items
            for item in reversed(self._items):
                if (isinstance(item, tuple) and len(item) == 2 and
                    item[0] == key):
                    return item[1]
            raise KeyError('not found')

    def get(self, key, default=None):
        try:
            return self[key]
        except (IndexError, KeyError):
            return default
