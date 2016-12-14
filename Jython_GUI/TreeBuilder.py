
import os
import re

from BST import BST
from LinkedList import LinkedList
from LinkedQueue import LinkedQueue
from TST import TST
from TrieST import TrieST


class TreeBuilder:
    def __init__(self, tree_type, directory_entered):
        self.tree_type = tree_type
        self.files_list = list()
        self.stopwordsBST = BST()
        self.stopwordsTST = TST()
        self.stopwordsTrie = TrieST()
        self.words_tree = TST()
        self.stopwords_init()
        self._build(directory_entered)

    def stopwords_init(self):
        fileQueue = LinkedQueue()
        fp = open("StopWords.txt", '+r')
        for line in fp.readlines():
            key = (line.rstrip('\n'))
            fileQueue.enqueue(key)
        fp.close()

        i = 0
        for q in fileQueue:
            self.stopwordsTST.put(str(q.element), i, None)
            i += 1
        self.stopwordsTST.validation()

        for q in fileQueue:
            self.stopwordsBST.insert(str(q.element), None)

        i = 0
        for q in fileQueue:
            self.stopwordsTrie.put(str(q.element), i, None)
            i += 1
        self.stopwordsTrie.validation()

    def _build(self, directory_entered):
        if True:  # os.path.isdir(directory_entered.get()):
            if unicode(self.tree_type) == unicode('TST'):
                print("----------------------------------------")
                print("TST")
                print(type(self.tree_type))
                print("----------------------------------------")

                # TST Tree
                self.words_tree = TST()
                counter = 0
                for subdir, dirs, files in os.walk(directory_entered.toString()):
                    for _file in files:
                        if _file.endswith('.txt'):
                            self.files_list.append(str(_file))
                            fp = open(os.path.join(subdir, _file), 'r+')
                            DATA = fp.read().replace('\n', ' ')
                            for key in re.findall(r"[\w']+", DATA):
                                if len(self.stopwordsTST.keysWithPrefix(key)) == 0:
                                    # if len(self.words_tree.keysThatMatch(key)) == 0:
                                    self.words_tree.put(str(key), counter, _file)
                                    counter += 1

                            fp.close()

                self.words_tree.validation()

                print("--------------------------Test traverse and correct words")
                i = 0
                for t in self.words_tree.traverse():
                    print(t)
                    i += 1
                print(i)

            elif unicode(self.tree_type) == unicode('BST'):

                print("----------------------------------------")
                print(type(self.tree_type))
                print("----------------------------------------")
                # BST Search
                del self.words_tree
                self.words_tree = BST()
                print(type(self.words_tree))

                for subdir, dirs, files in os.walk(directory_entered.toString()):
                    for _file in files:
                        if _file.endswith('.txt'):
                            self.files_list.append((str(_file)))
                            fp = open(os.path.join(subdir, _file), 'r+')
                            DATA = fp.read().replace('\n', ' ')
                            for key in re.findall(r"[\w']+", DATA):
                                if self.stopwordsBST[key] is None:
                                    self.words_tree.insert(str(key), _file)
                            fp.close()

                print(type(self.words_tree))

            elif unicode(self.tree_type) == unicode('TrieST'):
                print("----------------------------------------")
                print("TrieST")
                print(type(self.tree_type))
                print("----------------------------------------")
                # Trie Search
                self.words_tree = TrieST()
                counter = 0
                for subdir, dirs, files in os.walk(directory_entered.toString()):
                    for _file in files:
                        if _file.endswith('.txt'):
                            self.files_list.append((str(_file)))
                            fp = open(os.path.join(subdir, _file), 'r+')
                            DATA = fp.read().replace('\n', ' ')
                            for key in re.findall(r"[\w']+", DATA):
                                if len(self.stopwordsTrie.keysWithPrefix(key)) == 0:
                                    self.words_tree.put(str(key), counter, _file)
                                    counter += 1
                            fp.close()
                self.words_tree.validation()

        else:
            pass
