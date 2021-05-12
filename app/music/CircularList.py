from random import choice

class CircularList:

    def __init__(self, list_val):
        self.list = list_val

    def choice(self):
        return choice(self.list)

    def contains(self, element):
        return element in self.list

    def size(self):
        return len(self.list)

    def append(self, element):
        self.list.append(element)

    def get(self, index):
        length = len(self.list)
        while index < 0:
            index += length
        while index >= length:
            index -= length
        return self.list[index]

    def index(self, element):
        return self.list.index(element)

    def __str__(self):
        return str(self.list)