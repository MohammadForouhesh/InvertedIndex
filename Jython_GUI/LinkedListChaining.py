from LinkedList import LinkedList


class ChaningLinkedList(LinkedList):
    class Node(LinkedList.Node):
        def __init__(self, key, value, prev, after):
            self.key = key
            self.value = value
            self.doc_list = list()
            self.prev = prev
            self.after = after

    def __init__(self):
        super(ChaningLinkedList, self).__init__()

    def __setitem__(self, key, value, set_doc=None):
        self.insert_between(key, value, self.trailer.prev, self.trailer, set_doc=set_doc)

    def insert_between(self, key, value, predecessor, successor, set_doc=None):
        newest = self.Node(key, value, predecessor, successor)
        newest.doc_list.append(set_doc)
        predecessor.after = newest
        successor.prev = newest
        self.size += 1
        return newest
