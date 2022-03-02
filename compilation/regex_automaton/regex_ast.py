from collections import deque
import string
import typing
from abc import ABC, abstractmethod
from compilation.regex_automaton.automaton import Automaton

def multi_union(*automaton_list):
    return automaton_list[0] | multi_union(*automaton_list[1:]) if len(automaton_list) > 1 else automaton_list[0]


class Node(ABC):   

    @abstractmethod
    def handle(self):
        pass


class AtomicNode(Node,ABC):   
    def __init__(self, value):
        self.value = value
    
    
class UnaryNode(Node,ABC):
    def __init__(self, node):
        self.node = node

    
    def handle(self):
        return self.handle_op(self.node.handle())

    @abstractmethod
    def handle_op(self,value):
        pass 
    

class BinaryNode(Node):
    
    def __init__(self, left, right):
        self.left = left
        self.right = right
        
    def handle(self):
        left = self.left.handle()
        right = self.right.handle()
        return self.handle_op(left,right)

    @abstractmethod
    def handle_op(self,left,right):
        pass

class EpsilonNode(AtomicNode):
    def __init__(self):
        super().__init__('ε')
        
    def handle(self):
        return Automata(1,{},{0:[]})
    

class ElementNode(AtomicNode):
       
    def handle(self):
        return Automaton(2, {(0, self.value): (1,)}, {1: []})

class RangeNode(BinaryNode):

    def handle_op(self,left,right):
        return [v for v in range(left,right + 1)]

class UnionNode(BinaryNode):

    def handle_op(self,left,right):
        return left | right

class ConcatNode(BinaryNode):

    def handle_op(self,left,right):
        return left & right

class ComplementNode(UnaryNode):

    def handle_op(self,value):
        if not isinstance(value,list):
            value = [value]
        value = [v for v in string.printable if v not in list(map(chr,value))]
        return multi_union(*[Automaton(2, {(0, v): (1,)}, {1: []}) for v in value])

class BracketNode(UnaryNode):

    def handle_op(self,value):
        if not isinstance(value,list):
            value = [value]
        return multi_union(*[Automaton(2, {(0, chr(v)): (1,)}, {1: []}) for v in value])

class InnerBracketNode(AtomicNode):

    def handle(self):
        return ord(self.value)

class MultiElemBracketNode(BinaryNode):

    def handle_op(self, left, right):
        if not isinstance(left, list):
            left = [left]
        if not isinstance(right, list):
            right = [right]
        return left + right
    

class StarNode(UnaryNode):

    def handle_op(self,value):
        return value.closure()

class PlusNode(UnaryNode):

    def handle_op(self,value):
        return value & value.closure()

class QuestionNode(UnaryNode):

    def handle_op(self,value):
        return value | Automata(1,{},{0:[]})