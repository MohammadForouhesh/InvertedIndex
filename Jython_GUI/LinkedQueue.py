
class LinkedQueue:
    """
    FIFO implementation of queue with using linked list as internal storage
    """

    # ---------------------------------------------- Nested Class --------------------------------------------------
    class Node:
        "light weight class for storing liked node"

        def __init__(self, element, _next):                                        # initialize node field
            self.element = element                                                 # reference to current element
            self._next = _next                                                     # reference to the next node

    # --------------------------------------------- Stack Methods --------------------------------------------------
    def __init__(self):
        self._head = self.Node(None, None)
        self._tail = self.Node(None, None)
        self._size = 0

    def __len__(self):
        """
        return the number of elements in the linked list
        :return: integer
        """
        return self._size

    def __iter__(self):
        """
        iterate thorough the linked list
        """
        if self.is_empty():
            yield
        current = self._head
        while current is not None:
            yield current
            current = current._next

    def is_empty(self):
        """

        :return: bool True if list is empty and False otherwise
        """
        return self._size == 0

    def first(self):
        """
        just Return the first element in the queue
        """
        if self.is_empty():
            raise Exception("empty Error")
        return self._head.element

    def dequeue(self):
        """
        remove and return the first element
        """
        if self.is_empty():
            raise Exception("empty Error")
        var = self._head.element
        self._head = self._head._next
        self._size -= 1
        if self.is_empty():
            self._tail = None
        return var

    def enqueue(self, element):
        newest = self.Node(element, None)
        if self.is_empty():
            self._head = newest
        else:
            self._tail._next = newest
        self._tail = newest
        self._size += 1

    def querry(self):
        """
        for TTD and debuging.
        """
        for k in self:
            print(k.element)
