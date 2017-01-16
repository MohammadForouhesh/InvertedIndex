from collections import MutableMapping
from random import randrange

from UnsortedTable import UnsortedTableMap
from LinkedListChaining import ChaningLinkedList
from LinkedQueue import LinkedQueue


class SCHashST(MutableMapping):
    """Hash map implemented with separate chaining for collision resolution.
    class _Item:
        \"""store key-value pairs.\"""

        def __init__(self, k, v):
            self._key = k
            self._value = v
            self.doc_list = list()

        def __eq__(self, other):
            return self._key == other._key

        def __ne__(self, other):
            return not (self == other)

        def __lt__(self, other):
            return self._key < other._key
"""
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

    def __getitem__(self, key, get_doc=False):
        j = self._hash_function(key)
        return self._bucket_getitem(j, key, get_doc=get_doc)

    def __contains__(self, val):
        for i in self:
            if val == self[i]:
                return True
        return False

    def __setitem__(self, key, value, set_doc=None):
        j = self._hash_function(key)
        self._bucket_setitem(j, key, value, set_doc=set_doc)
        if self._n > len(self._table) // 2:                     # keep load factor <= 0.5
            self._resize(2 * len(self._table) - 1)              # number 2^x - 1 is often prime by Fermat theoriem

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

    def _bucket_getitem(self, j, key, get_doc=False):
        bucket = self._table[j]
        if bucket is None:
            raise KeyError('Key Error: ' + repr(key))
        return bucket.__getitem__(key, get_doc=get_doc)

    def _bucket_setitem(self, j, key, value, set_doc=None):
        if value in self:
            return

        if self._table[j] is None:
            self._table[j] = UnsortedTableMap()
        oldsize = len(self._table[j])
        self._table[j].__setitem__(key, value, set_doc=set_doc)
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
                for key in bucket:                                 # chaining
                    yield key


if __name__ == '__main__':
    import os, re
    stopwordsSCHashST = SCHashST()
    fileQueue = LinkedQueue()

    fp = open("StopWords.txt", '+r')
    for line in fp.readlines():
        key = (line.rstrip('\r\n'))
        fileQueue.enqueue(key)
    fp.close()

    i = 0
    for q in fileQueue:
        stopwordsSCHashST[i] = q.element
        i += 1

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
                for value in re.findall(r"[\w']+", DATA):
                    if value not in stopwordsSCHashST:
                        words_tree.__setitem__(counter, value, set_doc=_file)

                        counter += 1
                fp.close()

    print(counter)

    for i in words_tree:
        print words_tree.__getitem__(i,get_doc=True).doc_list

    print(len(words_tree))