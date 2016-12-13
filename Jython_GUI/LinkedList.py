
class LinkedList:
    class Node:
        """
        Lightweight, nonpublic class for storing a doubly linked node.
        """

        def __init__(self, element, prev, after):  # initialize node's fields
            self.element = element  # user's element
            self.prev = prev  # previous node reference
            self.after = after

    def __init__(self):
        """
        Create an empty list.
        """
        self.header = self.Node(None, None, None)
        self.trailer = self.Node(None, None, None)
        self.header.after = self.trailer  # trailer is after header
        self.trailer.prev = self.header  # header is before trailer
        self.size = 0

    def __len__(self):
        return self.size

    def __iter__(self):
        if self.is_empty():
            yield self.Node(None, None, None)
        current = self.header
        while current is not None:
            yield current
            current = current.after

    def is_empty(self):
        return self.size == 0

    def insert_between(self, element, predecessor, successor):
        newest = self.Node(element, predecessor, successor)  # linked to neighbors
        predecessor.after = newest
        successor.prev = newest
        self.size += 1
        return newest

    def delete_node(self, node):
        predecessor = node.prev
        successor = node.after
        predecessor.after = successor
        successor.prev = predecessor
        self.size -= 1
        element = node.element  # record deleted element
        node.prev = node.after = node.element = None  # deprecate node
        return element

    # -----------------------------------------------------------------------------------------------------------------

    def add_first(self, element):
        return self.insert_between(element, self.header, self.header.after)

    def add_last(self, element):
        return self.insert_between(element, self.trailer.prev, self.trailer)

    def add_before(self, prevElement, element):
        original = self.search(prevElement)
        return self.insert_between(element, original.prev, original)

    def add_after(self, nextElement, element):
        original = self.search(nextElement)
        return self.insert_between(element, original, original.after)

    # ------------------------------------------------------------------------------------------------------------------

    def delete(self, undesireElement):
        original = self.search(undesireElement)
        if original is None:
            return
        return self.delete_node(original)

    def search(self, desireElement):
        head = self.header
        while head.after is not None:
            head = head.after
            if head.element == desireElement:
                return head
        return None
