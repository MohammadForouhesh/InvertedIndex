from collections import MutableMapping


class UnsortedTableMap(MutableMapping):
    class _Item:
        """store key-value pairs."""

        def __init__(self, k, v):
            self._key = k
            self._value = v
            self.doc_list = [None]*12

        def __eq__(self, other):
            return self._key == other._key

        def __ne__(self, other):
            return not (self == other)

        def __lt__(self, other):
            return self._key < other._key

    def __init__(self):
        self._table = []

    def __getitem__(self, k, get_doc=False):
        for item in self._table:
            if k == item._key:
                if get_doc:
                    return item
                return item._value
        raise KeyError('Key Error: ' + repr(k))

    def __setitem__(self, k, v, set_doc=None):
        for item in self._table:
            if k == item._key:
                item._value = v
                item.doc_list.append(set_doc)
                return
        self._table.append(self._Item(k, v))

    def __delitem__(self, k):
        for j in range(len(self._table)):
            if k == self._table[j]._key:
                self._table.pop(j)
                return  # and quit
        raise KeyError('Key Error: ' + repr(k))

    def __len__(self):
        return len(self._table)

    def __iter__(self):
        for item in self._table:
            yield item._key                                     # yield the KEY