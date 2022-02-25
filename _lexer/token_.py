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
    def __init__(self,name:str, exp: str, process: Callable = None):
        self.name = name
        #self.exp: re.Pattern = re.compile(exp)
        self.exp = exp
        self.regex = RegexEngine()
        self.process = process


    

    def match(self, text: str, start: int, line: int, column: int):
        def f_spaces(text):
            c = 0
            for s in text[start:]:
                if not str(s).isspace():
                    break
                c+=1
            return c
        spaces = f_spaces(text)
        matched,_,matches = self.regex.match(self.exp, text,return_matches= True,continue_matching=True)
        if matched:
            pass
        else:
            return False
        match = None
        for m in matches:
            if m[0].start == 0:
                match = m[0]
        if not match:
            return False
        if self.process:
            value = self.process(match.match)
        else:
            value = match.match

        for c in match.match:
            if c == '\n':
                line += 1
                col = 1

        return Token(self.name, value, match.start+start, match.end+start, line, column)
