from collections import deque
import itertools
import typing


class Node:
    id_iter = itertools.count()

    def __init__(self):
        self.id = next(Node.id_iter)
        self.type = 'Node'
        self.is_capturing = None

    def is_capturing(self):
        return self.is_capturing


class RegNode(Node):

    def __init__(self, child: Node):
        super().__init__()
        self.type = 'regNode'
        self.child = child
        self.children = deque([child])


class LeafNode(Node):

    def __init__(self):
        super().__init__()

    def is_match(self, char: str = ' ', str_index: int = 0, str_len: int = 0):
        return False


class ElementNode(LeafNode):

    def __init__(self, match: str):
        super().__init__()
        self.type = 'elementnode'
        self.match = match
        self.min = 1
        self.max = 1

    def is_match(self, char: str = ' ', str_index: int = 0, str_len: int = 0):
        return self.match == char


class DotNode(ElementNode):

    def __init__(self):
        super().__init__('any')
        self.type = 'dotNode'
        self.match = True

    def is_match(self, char: str = ' ', str_index: int = 0, str_len: int = 0):
        return char != '\n'


class SpaceNode(ElementNode):

    def __init__(self):
        super().__init__('apce')
        self.type = 'spaceNode'
        self.match = True

    def is_match(self, char: str = ' ', str_index: int = 0, str_len: int = 0):
        return char.isspace() and len(char) == 1


class RangeNode(LeafNode):

    def __init__(self, match: str, positive: bool = True):
        super().__init__()
        self.type = 'rangeNode'
        self.match = match
        self.min = 1
        self.max = 1
        self.positive = positive

    def is_match(self, char: str = ' ', str_index: int = 0, str_len: int = 0):
        return not((char in self.match) ^ self.positive)


class StartNode(LeafNode):

    def __init__(self):
        super().__init__()
        self.type = 'startNode'
        self.match = 0
        self.min = 1
        self.max = 1

    def is_match(self, char: str = ' ', str_index: int = 0, str_len: int = 0):
        return str_index == 0


class EOFNode(LeafNode):

    def __init__(self):
        super().__init__()
        self.type = 'eofNode'
        self.match = 'len(string)'
        self.min = 1
        self.max = 1

    def is_match(self, char: str = ' ', str_index: int = 0, str_len: int = 0):
        return str_index == str_len


class OrNode(Node):

    def __init__(self, left: Node, right: Node):
        super().__init__()
        self.type = 'orNode'
        self.left = left
        self.right = right
        self.children = [left, right]
        self.min = 1
        self.max = 1

class ComplementNode(Node):

    def __init__(self, child: Node):
        super().__init__()
        self.type = 'complementNode'
        self.child = child
        self.children = deque([child])

class GroupNode(Node):

    def __init__(self, children: typing.Deque[Node], capturing: bool = False, group_name: str = 'group'):
        super().__init__()
        self.type = 'groupNode'
        self.is_capturing = capturing
        self.group_name = group_name
        self.children = children
        self.min = 1
        self.max = 1
