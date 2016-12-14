from LinkedList import LinkedList


class BST:
    class Node:
        def __init__(self, parent, key):
            self.key = key
            self.parent = parent
            self.left = None
            self.right = None
            self.size = 1
            self.repetition = 1
            self.doc_list = []

        # --------------------------------------------------------------------------------------

        def update_stats(self):
            """Updates this node's size based on its children's sizes."""
            self.size = (0 if self.left is None else self.left.size) \
                        + (0 if self.right is None else self.right.size)

        # --------------------------------------------------------------------------------------

        def insert(self, key, NodeType, set_doc):
            self.size += 1
            if key < self.key:
                if self.left is None:
                    self.left = NodeType(self, key)
                    if set_doc is not None:
                        self.doc_list.append(set_doc)
                    return self.left
                else:
                    return self.left.insert(key, NodeType, set_doc)
            elif key == self.key:
                self.repetition += 1
                if set_doc is not None:
                    self.doc_list.append(set_doc)
                return
            else:
                if self.right is None:
                    self.right = NodeType(self, key)
                    if set_doc is not None:
                        self.doc_list.append(set_doc)
                    return self.right
                else:
                    return self.right.insert(key, NodeType, set_doc)

        # ---------------------------------------------------------------------------------------

        def find(self, key, get_doc):
            """Return the node for key if it is in this tree, or None otherwise."""
            if key == self.key:
                if get_doc is not None:
                    return self.doc_list
                return self
            elif key < self.key:
                if self.left is None:
                    return None
                else:
                    return self.left.find(key, get_doc)
            else:
                if self.right is None:
                    return None
                else:
                    return self.right.find(key, get_doc)

        # ----------------------------------------------------------------------------------------

        def rank(self, key):
            """Return the number of keys <= key in the subtree rooted at this node."""
            left_size = 0 if self.left is None else self.left.size
            if key == self.key:
                return left_size + 1
            elif key < self.key:
                if self.left is None:
                    return 0
                else:
                    return self.left.rank(key)
            else:
                if self.right is None:
                    return left_size + 1
                else:
                    return self.right.rank(key) + left_size + 1

        def minimum(self):
            """Returns the node with the smallest key in the subtree rooted by this node."""
            current = self
            while current.left is not None:
                current = current.left
            return current

        def successor(self):
            """
            Returns the node with the smallest key larger than this node's key,
            or None if this has the largest key in the tree.
            """
            if self.right is not None:
                return self.right.minimum()
            current = self
            while current.parent is not None and current.parent.right is current:
                current = current.parent
            return current.parent

        # -------------------------------------------------------------------------------------------

        def delete(self):
            """"Delete this node from the tree."""
            if self.left is None or self.right is None:
                if self is self.parent.left:
                    self.parent.left = self.left or self.right
                    if self.parent.left is not None:
                        self.parent.left.parent = self.parent
                else:
                    self.parent.right = self.left or self.right
                    if self.parent.right is not None:
                        self.parent.right.parent = self.parent
                current = self.parent
                while current.key is not None:
                    current.update_stats()
                    current = current.parent
                return self
            else:
                s = self.successor()
                self.key, s.key = s.key, self.key
                return s.delete()

        # ---------------------------------------------check for error-------------------------------

        def check(self, lower_key, higher_key):
            """
            Checks that the subtree rooted at key is a valid BST
            and all keys are between (lower_key, higher_key).
            """
            if lower_key is not None and self.key <= lower_key:
                raise Exception("BST RI violation")
            if higher_key is not None and self.key >= higher_key:
                raise Exception("BST RI violation")
            if self.left is not None:
                if self.left.parent is not self:
                    raise Exception("BST RI violation")
                self.left.check(lower_key, self.key)
            if self.right is not None:
                if self.right.parent is not self:
                    raise Exception("BST RI violation")
                self.right.check(self.key, higher_key)
            if self.size != 1 + (0 if self.left is None else self.left.size) + (
                    0 if self.right is None else self.right.size):
                raise Exception("BST RI violation")

        def __repr__(self):
            return "<BST Node, key:" + str(self.key) + ">"

    def __init__(self, NodeType=Node):
        self.root = None
        self.NodeType = NodeType
        self.psroot = self.NodeType(None, None)
        self.content = []
        self.docs = LinkedList()

    # -------------------------------------------------------------------------------------------------
    def reroot(self):
        self.root = self.psroot.left

    def insert(self, key, set_doc):
        """Insert key into this BST, modifying it in-place."""
        if self.root is None:
            self.psroot.left = self.NodeType(self.psroot, key)
            self.reroot()
            self.root.update_stats()
            return self.root
        else:
            return self.root.insert(key, self.NodeType, set_doc)

    def add_doc(self, doc_name):
        self.docs.add_last(doc_name)

    # --------------------------------------------------------------------------------------------------

    def __getitem__(self, key, get_doc=None):
        """Return the node for key if is in the tree, or None otherwise."""
        if self.root is None:
            return None
        else:
            return self.root.find(key, get_doc)

    def rank(self, key):
        """The number of keys <= key in the tree."""
        if self.root is None:
            return 0
        else:
            return self.root.rank(key)

    def traverse(self):
        self._traverse()
        for i in self.content:
            yield i

    def _traverse(self, node=None):
        if node is None:
            node = self.root

        self.content.append(node.key)
        if node.left is not None:
            self._traverse(node=node.left)
        if node.right is not None:
            self._traverse(node=node.right)

    def delete(self, key):
        node = self.find(key)
        if node is None:
            raise Exception("nadari in klid ro")
        deleted = node.delete()
        self.reroot()
        return deleted

    # -------------------------------------------------------------------------------------------------

    def check(self):
        if self.root is not None:
            self.root.check(None, None)  # check in the Node class

    def __str__(self):
        if self.root is None:
            return '<empty tree>'

        def recurse(node):
            if node is None: return [], 0, 0
            label = str(node.key)
            left_lines, left_pos, left_width = recurse(node.left)
            right_lines, right_pos, right_width = recurse(node.right)
            middle = max(right_pos + left_width - left_pos + 1, len(label), 2)
            pos = left_pos + middle // 2
            width = left_pos + middle + right_width - right_pos
            while len(left_lines) < len(right_lines):
                left_lines.append(' ' * left_width)
            while len(right_lines) < len(left_lines):
                right_lines.append(' ' * right_width)
            if (middle - len(label)) % 2 == 1 and node.parent is not None and \
                            node is node.parent.left and len(label) < middle:
                label += '.'
            label = label.center(middle, '.')
            if label[0] == '.': label = ' ' + label[1:]
            if label[-1] == '.': label = label[:-1] + ' '
            lines = [' ' * left_pos + label + ' ' * (right_width - right_pos),
                     ' ' * left_pos + '/' + ' ' * (middle - 2) +
                     '\\' + ' ' * (right_width - right_pos)] + \
                    [left_line + ' ' * (width - left_width - right_width) + right_line

                     for left_line, right_line in zip(left_lines, right_lines)]
            return lines, pos, width

        return '\n'.join(recurse(self.root)[0])
