
import os

import re

from LinkedList import LinkedList
from LinkedQueue import LinkedQueue


class TST:

    # ----------------------------------------- inner class ----------------------------------------------

    class Node:
        def __init__(self, key_char):
            self.key_char = key_char
            self.left = None
            self.mid = None
            self.right = None
            self.doc_list = []
            self.value = int(-1)

    # -------------------------------------- end of inner class ------------------------------------------

    def __init__(self):
        self.root = TST.Node(" ")
        self.size = 0
        self.valid_words = []
        self.docs = LinkedList()

    def __sizeof__(self):
        return self.size

    def __contains__(self, item):
        if item is None:
            raise Exception("nothing to be contained!!!")
        return self[item] is not None

    def __getitem__(self, item, get_doc=None, trav=False):
        if item is None:
            raise Exception("call __getitem__ with None argument")
        if len(item) == 0:
            raise Exception("item must have length >= 1")
        x = self.get(self.root, item, 0)
        if x is None:
            return None
        if get_doc is None and trav is False:
            return x.value

        elif get_doc is not None:
            return x.doc_list
        elif trav:
            return x

    def intable(self, stream):
        try:
            integer = int(stream)
            return True, integer
        except Exception :
            return False, Exception

    def get(self, x, item, d):
        """
        return sub-trie corresponding to given key
        """
        if x is None:
            return None
        if len(item) == 0:
            raise Exception("item must have length >= 1")
        char = item[d]
        if char < x.key_char:
            return self.get(x.left, item, d)
        elif char > x.key_char:
            return self.get(x.right, item, d)
        elif d < len(item) - 1:
            return self.get(x.mid, item, d + 1)
        else:
            return x

    def put(self, item, value, set_doc):
        """
        Inserts the key-value pair into the symbol table
        """
        if item is None:
            raise Exception("call __setitem__ with None argument")
        else:
            self.size += 1
        self.root = self.set(self.root, item, int(value), 0, set_doc)

    def set(self, x, item, value, d, set_doc):
        char = item[d]
        if x is None:
            x = TST.Node(char)

        if char < x.key_char:
            x.left = self.set(x.left, item, int(value), d, set_doc)
        elif char > x.key_char:
            x.right = self.set(x.right, item, int(value), d, set_doc)
        elif d < len(item) - 1:
            x.mid = self.set(x.mid, item, int(value), d + 1, set_doc)
        else:
            x.value = int(value)

        x.doc_list.append(set_doc)
        return x

    def longestPrefixOf(self, query):
        if query is None:
            raise Exception("call longestPrefixOf() with None argument")
        if len(query) == 0:
            return None
        length = int(0)
        x = self.root
        i = 0
        while x is not None and i < len(query):
            char = query[i]
            if char < x.key_char:
                x = x.left
            elif char > x.key_char:
                x = x.right
            else:
                i += 1
                if x.value is not None:
                    length = i
                x = x.mid

        return query[0:length]  # testing required

    def keys(self):
        queue = LinkedQueue()
        self.collect(self.root, str(), queue)
        return queue  # queue is iterable?

    def keysWithPrefix(self, prefix):

        if prefix is None:
            raise Exception("call keysWithPrefix() with None argument")
        queue = LinkedQueue()
        x = self.root
        x = self.get(x, prefix, 0)
        if x is None:
            return queue
        if x.value is not None:
            queue.enqueue(prefix)
        self.collect(x.mid, str(prefix), queue)
        return queue

    def collect(self, x, prefix, queue):
        if x is None:
            return None
        self.collect(x.left, prefix, queue)
        if x.value is not None:
            queue.enqueue(str(prefix) + x.key_char)
        self.collect(x.mid, str(prefix) + str(x.key_char), queue)
        # prefix = prefix[:-1]
        self.collect(x.right, prefix, queue)

    def keysThatMatch(self, pattern):
        queue = LinkedQueue()
        self.patternMatching(self.root, str(), 0, pattern, queue)
        return queue

    def patternMatching(self, x, prefix, i, pattern, queue):
        """
        some kind of collector
        """
        if x is None:
            return
        char = pattern[i]
        if char == '.' or char < x.key_char:
            self.patternMatching(x.left, prefix, i, pattern, queue)
        if char == '.' or char == x.key_char:
            if i == len(pattern) - 1 and x.value is not None:
                queue.enqueue(str(prefix) + str(x.key_char))
            if i < len(pattern) - 1:
                self.patternMatching(x.mid, str(prefix) + str(x.key_char), i + 1, pattern, queue)
                prefix = prefix[:-1]

        if char == '.' or char > x.key_char:
            self.patternMatching(x.right, prefix, i, pattern, queue)

    def add_doc(self, doc_name):
        self.docs.append(doc_name)

    def traverse(self):
        if self.size == 0:
            raise Exception("empty tst can't be traversed")
        for q in self.keys():
            if self[q.element] is not None and self[q.element] != -1:
                yield q.element

    def validation(self):
        for v in self.traverse():
            self.valid_words.append(v)



if __name__ == '__main__':
    tst = TST()
    tstStp = TST()

    fileQueue = LinkedQueue()

    fp = open("StopWords.txt", '+r')
    for line in fp.readlines():
        key = (line.rstrip('\n\r'))
        fileQueue.enqueue(key)
    fp.close()

    i = 0
    for q in fileQueue:
        tstStp.put(str(q.element), i, None)
        i += 1
    tstStp.validation()
    counter = 0
    for subdir, dirs, files in os.walk("/home/maometto/Documents/d"):
        for file in files:
            if file.endswith('.txt'):
                fp = open(os.path.join(subdir, file), 'r+')
                DATA = fp.read().replace('\n', ' ')
                for key in re.findall(r"[\w']+", DATA):
                    if len(tstStp.keysThatMatch(key)) == 0:
                        if len(tst.keysThatMatch(key)) == 0:
                            tst.put(str(key), counter, file)
                            print(key , "====================son of the keys====================")
                            counter += 1

                fp.close()
    tst.validation()
    print(len(tst.valid_words), "=----------TST-----------=")

    i = 0
    for t in tst.traverse():
        print(t)
        i += 1
    print(i)
