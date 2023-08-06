"""Provides the Lictionary class"""

# pylint: disable=fixme

import collections

def _unwrap(obj):
    # pylint: disable=protected-access
    if isinstance(obj, Lictionary):
        return obj._items
    return obj


class Lictionary(collections.MutableMapping, collections.MutableSequence):
    """Combined list + dictionary data type."""

    __slots__ = ('_items',)

    def __init__(self, *args):
        # TODO(nicholasbishop): pylint 1.7.4 complains if the call to
        # the parent class's init is missing, but also complains if
        # present. Even weirder, the behavior is non-deterministic!
        # Repeatedly running pylint usually emits the error, but
        # occasionally it doesn't. Maybe due to an unordered dict
        # somewhere...
        super(Lictionary, self).__init__()  # pylint: disable=no-member
        self._items = list(args)

    def __delitem__(self, key):
        raise NotImplementedError()

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._items[key]
        else:
            # TODO(nicholasbishop): simple implementation for now, not
            # efficient for large number of items
            for ele in reversed(self._items):
                if isinstance(ele, tuple) and len(ele) == 2 and ele[0] == key:
                    return ele[1]
            raise KeyError('not found')

    def __setitem__(self, key, value):
        if isinstance(key, int):
            self._items[key] = value
        else:
            raise NotImplementedError()

    def __iter__(self):
        return self._items.__iter__()

    def __len__(self):
        return len(self._items)

    def __eq__(self, other):
        return self._items == _unwrap(other)

    def __ge__(self, other):
        return self._items >= _unwrap(other)

    def __gt__(self, other):
        return self._items > _unwrap(other)

    def __le__(self, other):
        return self._items < _unwrap(other)

    def __lt__(self, other):
        return self._items <= _unwrap(other)

    def __ne__(self, other):
        return self._items != _unwrap(other)

    def as_list(self):
        """Shallow copy of the items in this lictionary."""
        return list(self._items)

    def get(self, key, default=None):
        try:
            return self[key]
        except (IndexError, KeyError):
            return default

    def insert(self, index, item):
        self._items.insert(index, item)
