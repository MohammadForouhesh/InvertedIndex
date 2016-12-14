import os

import re

from LinkedList import LinkedList
from LinkedQueue import LinkedQueue


class TrieST:
    R = 256

    class Node:
        def __init__(self):
            self.value = str()
            self.doc_list = []
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

    def __getitem__(self, key, get_doc=None, trav=False):
        x = self.get(self.root, key, 0)
        if x is None:
            return None
        if get_doc is None and trav is False:
            return str(x.value)
        elif get_doc is not None:
            return x.doc_list
        elif trav:
            return x

    def __contains__(self, key):
        return self.__getitem__(key) is not None

    def get(self, x, key, d):
        if x is None:
            return None
        if d == len(key):
            return x
        char = key[d]
        return self.get(x._next[int(ord(char))], key, d + 1)

    def put(self, key, value, set_doc):
        if value is None:
            del key
        else:
            self.root = self.set(self.root, key, value, 0, set_doc)

    def set(self, x, key, value, d, set_doc):
        if x is None:
            x = self.Node()
        if d == len(key):
            if x.value is None:
                self.number_of_keys += 1
            x.value = value
            if set_doc is not None:
                x.doc_list.append(set_doc)
            return x
        char = key[d]
        x._next[int(ord(char))] = self.set(x._next[int(ord(char))], key, value, d + 1, set_doc)
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


if __name__ == '__main__':
    trie = TrieST()
    trieStp = TrieST()

    fileQueue = LinkedQueue()
    fp = open("StopWords.txt", '+r')
    for line in fp.readlines():
        key = (line.rstrip('\n'))
        fileQueue.enqueue(key)
    fp.close()
    i = 0
    for q in fileQueue:
        trieStp.put(str(q.element), i, None)
        i += 1
    trieStp.validation()

    counter = 0
    for subdir, dirs, files in os.walk("/home/maometto/Documents/d/"):
        for _file in files:
            if _file.endswith('.txt'):
                fp = open(os.path.join(subdir, _file), 'r+')
                DATA = fp.read().replace('\n', ' ')
                for key in re.findall(r"[\w']+", DATA):
                    if len(trieStp.keysWithPrefix(key)) == 0:
                        trie.put(str(key), counter, _file)
                        counter += 1
                fp.close()
    trie.validation()
    print(counter)



    try :
        for s in trie.keysThatMatch("afterward"):
            print(s.element)
    except Exception as err:
        print(err)

    print("-------------------------Test traverse and correct words")
    for t in trie.traverse():
        print(t)
    print("-------------------------Number of valid words")
    print(len(trie.valid_words))
