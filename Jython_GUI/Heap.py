from collections import Container

class Heap(Container):
    array = []

    # Allows "if item in tree:"
    def __contains__(self, item):
        return self._contains(item, 1)

    def _contains(self, item, index):
        if item > self.array[index-1]:
            return False
        elif item < self.array[index-1]:
            if len(self.array) > index * 2:
                return self._contains(item, index*2) or self._contains(item, index*2+1)
            elif len(self.array) > index * 2 + 1:
                return self._contains(item, index*2)
            else:
                return False
        else:
            return True

    def add(self, item):
        self.array.append(item)
        self._bubble(len(self.array)-1)

    def _bubble(self, index):
        # Note: we take 1-based indexes, but convert them to 0-based ones
        index = index-1
        if self.array[index] > self.array[index/2]:
            tmp = self.array[index]
            self.array[index] = self.array[index/2]
            self.array[index/2] = tmp
            self._bubble(index/2)

    # Useful for debugging. Prints the whole tree
    def __repr__(self):
        return self._repr(1)

    def _repr(self, index, indent=0):
        # Note: we use 1-based indexes here
        string = ""
        string = ('\t' * indent) + str(self.array[index-1]) + '\n'

        if len(self.array) >= index * 2:
            string += ('\t' * (indent+1)) + 'Left:\n'
            string += self._repr(index*2, indent+1)

        if len(self.array) >= index * 2 + 1:
            string += ('\t' * (indent+1)) + 'Right:\n'
            string += self._repr(index*2+1, indent+1)

        return string


if __name__ == '__main__':
    from random import randint

    values = []
    tree = Heap()
    for i in range(40):
        val = randint(0, 100)
        tree.add(val)
        values.append(val)

    print(tree)  # uses __repr__
    print(values)
    print(25 in tree)  # uses __contains__
    print(25 in values)