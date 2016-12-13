
class LinkedStack():

    # ---------------------------------------------- Nested Class --------------------------------------------------
    class Node:

        def __init__(self, element, _next):  # initialize node field
            self.element = element  # reference to current element
            self._next = _next  # reference to the next node

    # --------------------------------------------- Stack Methods --------------------------------------------------
    def __init__(self):
        self.head = self.Node(None, None)  # head is a kind of node
        self.size = 0

    def __len__(self):
        return self.size

    def __iter__(self):
        if self.is_empty():
            yield
        current = self.head
        while current is not None:
            yield current
            current = current._next

    def is_empty(self):
        return self.size == 0

    def push(self, element):
        self.head = self.Node(element, self.head)  # created and linked a new node
        self.size += 1  # size is incremented

    def top(self):
        if self.is_empty():
            raise Exception("stack is empty")
        return self.head.element

    def pop(self):
        if self.is_empty():
            raise Exception("stack is empty")
        answer = self.head.element
        self.head = self.head._next  # bypass the former node :)
        self.size -= 1  # size decremented
        return answer

    def querry(self):
        """
        for TTD and debuging.
        """
        for k in self:
            print(k.element)
