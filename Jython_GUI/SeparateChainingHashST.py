from collections import MutableMapping
from random import randrange


class SCHashST(MutableMapping):
    """Hash map implemented with separate chaining for collision resolution."""
    class _Item:
        """store key-value pairs."""

        def __init__(self, k, v):
            self._key = k
            self._value = v

        def __eq__(self, other):
            return self._key == other._key

        def __ne__(self, other):
            return not (self == other)

        def __lt__(self, other):
            return self._key < other._key                   # compare items based on their keys

    def __init__(self, cap=11, p=109345121):
        self._table = cap * [None]
        self._n = 0
        self._prime = p
        self._scale = 1 + randrange(p - 1)
        self._shift = randrange(p)

    def _hash_function(self, key):
        return (hash(key) * self._scale + self._shift) % self._prime % len(self._table)

    def __len__(self):
        return self._n

    def __getitem__(self, key):
        j = self._hash_function(key)
        return self._bucket_getitem(j, key)

    def __setitem__(self, key, value):
        j = self._hash_function(key)
        self._bucket_setitem(j, key, value)
        if self._n > len(self._table) // 2:                     # keep load factor <= 0.5
            self._resize(2 * len(self._table) - 1)              # number 2^x - 1 is often prime

    def __delitem__(self, key):
        j = self._hash_function(key)
        self._bucket_delitem(j, key)
        self._n -= 1

    def _resize(self, c):
        old = list(self.items())
        self._table = c * [None]
        self._n = 0
        for (k, v) in old:
            self[k] = v

    def _bucket_getitem(self, j, key):
        bucket = self._table[j]
        if bucket is None:
            raise KeyError('Key Error: ' + repr(key))
        return bucket[key]

    def _bucket_setitem(self, j, key, value):
        for i in self:
            if value == self[i]:
                return
        
        if self._table[j] is None:
            self._table[j] = UnsortedTableMap()
        oldsize = len(self._table[j])
        self._table[j][key] = value
        if len(self._table[j]) > oldsize:
            self._n += 1

    def _bucket_delitem(self, j, key):
        bucket = self._table[j]
        if bucket is None:
            raise KeyError('Key Error: ' + repr(key))
        del bucket[key]

    def __iter__(self):
        for bucket in self._table:
            if bucket is not None:
                for key in bucket:          # chaining
                    yield key


class UnsortedTableMap(MutableMapping):
    class _Item:
        """store key-value pairs."""
        def __init__(self, k, v):
            self._key = k
            self._value = v

        def __eq__(self, other):
            return self._key == other._key

        def __ne__(self, other):
            return not (self == other)

        def __lt__(self, other):
            return self._key < other._key  # compare items based on their keys

    def __init__(self):
        self._table = []

    def __getitem__(self, k):
        for item in self._table:
            if k == item._key:
                return item._value
        raise KeyError('Key Error: ' + repr(k))

    def __setitem__(self, key, value):
        for item in self._table:
            if key == item._key:
                item._value = value
                return
        self._table.append(self._Item(key, value))

    def __delitem__(self, key):
        for j in range(len(self._table)):
            if key == self._table[j]._key:
                self._table.pop(j)
                return  # and quit
        raise KeyError('Key Error: ' + repr(key))

    def __len__(self):
        return len(self._table)

    def __iter__(self):
        for item in self._table:
            yield item._key                                     # yield the KEY


if __name__ == '__main__':
    import os, re
    print("----------------------------------------")
    print("SCHashST")
    print("----------------------------------------")
    # Trie Search
    words_tree = SCHashST()
    counter = 0
    for subdir, dirs, files in os.walk("/home/maometto/Documents/black"):
        for _file in files:
            if _file.endswith('.txt'):
                #self.files_list.append((str(_file)))
                fp = open(os.path.join(subdir, _file), 'r+')
                DATA = fp.read().replace('\n', ' ')
                for key in re.findall(r"[\w']+", DATA):
                    # if len(self.stopwordsTrie.keysWithPrefix(key)) == 0:
                        # if len(self.words_tree.keysThatMatch(key)) == 0:
                    words_tree[counter] = key
                    counter += 1
                fp.close()

    print(counter)
    val = 'state'

    for i in words_tree:
        if val == words_tree[i]:
            print(True)

    for i in words_tree:
        print words_tree[i]

    print(len(words_tree))