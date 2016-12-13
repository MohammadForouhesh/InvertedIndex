from LinkedList import LinkedList
from LinkedQueue import LinkedQueue


class TrieST:
    R = 256

    class Node:
        def __init__(self):
            self.value = str()
            self._next = [None] * TrieST.R

    def __init__(self):
        self.root = self.Node()
        self.number_of_keys = 0
        self.valid_words = LinkedQueue()
        self.docs = LinkedList()

    def __sizeof__(self):
        return self.number_of_keys

    def __len__(self):
        return self.__sizeof__()

    def is_empty(self):
        return self.__sizeof__() == 0

    def __getitem__(self, key):
        x = self.get(self.root, key, 0)
        if x is None:
            return None
        return str(x.value)

    def __contains__(self, key):
        return self.__getitem__(key) is not None

    def get(self, x, key, d):
        if x is None:
            return None
        if d == len(key):
            return x
        char = key[d]
        return self.get(x._next[int(ord(char))], key, d + 1)

    def put(self, key, value):
        if value is None:
            del key
        else:
            self.root = self.set(self.root, key, value, 0)

    def set(self, x, key, value, d):
        if x is None:
            x = self.Node()
        if d == len(key):
            if x.value is None:
                self.number_of_keys += 1
            x.value = value
            return x
        char = key[d]
        x._next[int(ord(char))] = self.set(x._next[int(ord(char))], key, value, d + 1)
        return x

    def keys(self):
        return self.keysWithPrefix("")

    def keysWithPrefix(self, prefix):
        result = LinkedQueue()
        x = self.get(self.root, prefix, 0)
        self.collect(x, str(prefix), result)
        return result

    def collect(self, x, prefix, result):
        if x is None:
            return
        if x.value is not None:
            result.enqueue(str(prefix))
        for i in range(self.R):
            prefix += chr(i)
            self.collect(x._next[i], prefix, result)
            prefix = prefix[:-1]

    def keysThatMatch(self, pattern):
        result = LinkedQueue()
        self.patternMatching(self.root, str(), pattern, result)
        return result

    def patternMatching(self, x, prefix, pattern, result):
        if x is None:
            return
        d = len(prefix)
        if d == len(pattern) and x.value is not None:
            result.enqueue(str(prefix))
        if d == len(pattern):
            return

        char = pattern[d]
        if char == '.':
            for i in range(self.R):
                prefix += str(i)
                self.patternMatching(x._next[i], prefix, pattern, result)
                prefix = prefix[:-1]
        else:
            prefix += str(char)
            self.patternMatching(x._next[int(ord(char))], prefix, pattern, result)
            prefix = prefix[:-1]

    def longestPrefix(self, query):
        length = self.longestPrefixOf(self.root, query, 0, -1)
        if length == -1:
            return None
        else:
            return query[:length]

    def longestPrefixOf(self, x, query, d, length):
        if x is None:
            return length
        if x.value is not None:
            length = d
        if d == len(query):
            return length
        char = query[d]
        return self.longestPrefixOf(x._next[int(ord(char))], query, d + 1, length)
    
    def add_doc(self, doc_name):
        self.docs.append(doc_name)
    
    def traverse(self):
        query = self.keys()
        for q in query:
            if self[q.element] != '':
                yield(q.element)
    
    def validation(self):
        for v in self.traverse():
            self.valid_words.enqueue(v)
    
    def delete(self, key, x=None, d=None):
        if x is None and d is None:
            self.root = self.delete(key, x=self.root, d=0)
        if x is None:
            return None
        if d == len(key):
            if x.value is not None:
                self.number_of_keys -= 1
            x.value = None
        else:
            char = key[d]
            x._next[int(ord(char))] = self.delete(x._next[int(ord(char))], key, d + 1)

        # remove subtrie rooted at x if it is completely empty
        if x.value is not None:
            return x
        for i in range(self.R):
            if x._next[i] is not None:
                return x
        return None

