
from typing import Callable, List


class Token:
    def __init__(self, name: str, value: str, start: int, end: int, line: int, col: int) -> None:
        self.type = name
        self.value = value
        self.start = start
        self.end = end
        self.line = line
        self.col = col

    def __eq__(self, other: "Token") -> bool:
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return '('+self.name+', "'+str(self.value)+'"'+')'


class TokenRegex:
    def __init__(self,name:str, exp: str, process: Callable = None):
        self.type = name
        self.exp = exp
        self.automaton = None



