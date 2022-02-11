import re

from typing import Callable, List
from regex.regex_engine import RegexEngine, Match

class Token():
    def __init__(self, name: str, value: str, start: int, end: int, line: int, col: int) -> None:
        self.name = name
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

    
class TokenRegex():
    def __init__(self, name: str, exp: str, process: Callable = None):
        self.name = name
        self.exp: re.Pattern = re.compile(exp)
        # self.exp = exp
        # self.regex = RegexEngine()
        self.process = process
 
    def match(self, text: str, start: int, line: int, column: int):
        matched: re.Match = self.exp.match(text, start)
        if not matched:
            return False

        end = matched.end()
        if self.process:
            value = self.process(matched.group())
        else:
            value = matched.group()

        for c in matched.group():
            if c == '\n':
                line += 1
                col = 1

        return Token(self.name, value, start, end, line, column)

    # def match(self, text: str, start: int, line: int, col: int):
    #     matched, _, matches = self.regex.match(self.exp, text, True,True)
    #     if not matched:
    #         return False
    #     final_list = []
    #     for tokenl in matches:
    #         end = tokenl[0].end
    #         start = tokenl[0].start 
    #         if self.process:
    #             value = self.process(tokenl[0].match)
    #         else:
    #             value = tokenl[0].match
    #         for c in tokenl[0].match:
    #             if c == '\n':
    #                 line += 1
    #                 col = 1
    #         final_list.append(Token(self.name,value,start,end,line,col))
    #     return final_list
