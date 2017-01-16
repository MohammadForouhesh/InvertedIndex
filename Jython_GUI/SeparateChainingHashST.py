
from random import randrange

from UnsortedTable import UnsortedTableMap
from LinkedQueue import LinkedQueue


class SCHashST:
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

    def __getitem__(self, key, get_doc=False, trav=False):
        j = self._hash_function(key)
        return self._bucket_getitem(j, key, get_doc=get_doc, trav=trav)

    def __contains__(self, val):
        for i in self:
            if val == self[i]:
                return True
        return False

    def __setitem__(self, key, value):
        j = self._hash_function(key)
        self._bucket_setitem(j, key, value, None)
        if self._n > len(self._table) // 2:                     # keep load factor <= 0.5
            self._resize(2 * len(self._table) - 1)              # number 2^x - 1 is often prime by Fermat theoriem

    def setitem_(self, key, value, set_doc):
        j = self._hash_function(key)
        self._bucket_setitem(j, key, value, set_doc)
        if self._n > len(self._table) // 2:                     # keep load factor <= 0.5
            self._resize(2 * len(self._table) - 1)              # number 2^x - 1 is often prime by Fermat theoriem

    def __delitem__(self, key):
        j = self._hash_function(key)
        self._bucket_delitem(j, key)
        self._n -= 1

    def items(self):
        return [(key, self[key], self.__getitem__(key, get_doc=True)) for key in self]

    def _resize(self, c):
        old = list(self.items())
        self._table = c * [None]
        self._n = 0
        for (k, v, doc) in old:
            self.setitem_(k, v, set_doc=doc)

    def _bucket_getitem(self, j, key, get_doc=False, trav=False):
        bucket = self._table[j]
        # if bucket is None:
            # raise KeyError('Key Error: ' + repr(key))
        return bucket.__getitem__(key, get_doc=get_doc, trav=trav)

    def _bucket_setitem(self, j, key, value, set_doc):              # j = hash code
        if value in self:
            for (k, v, d) in self.items():
                if d != set_doc and value == v:
                    self.__getitem__(k, trav=True).doc_list.append(set_doc)
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

    def traverse(self):
        for i in self:
            yield self[i]

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
        stopwordsSCHashST.setitem_(i, q.element, "ahmadPanah")
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
                        words_tree.setitem_(counter, value, _file)
                        counter += 1
                fp.close()

    print(counter)

    for i in words_tree:
        print words_tree.__getitem__(i, get_doc=True)

    print(len(words_tree))