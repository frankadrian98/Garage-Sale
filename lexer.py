from typing import List
from token_ import Token, TokenRegex


def tokenize(program: str, token_regexs: List[TokenRegex]):
    start = 0
    tokens: List[Token] = []
    line = 1
    column = 1
    if not program:
        return []

    while True:
        valid = False

        for tp in token_regexs:
            token = tp.match(program[start:], start, line, column)
            if not token:
                continue
         
            if token.value != None:
                tokens.append(token)
            start = token.end
            valid = True
            if token.line != line:
                column = 1
            else:
                column += token.end - token.start
            line = token.line
            break

        if not valid:
            raise Exception()
        if start == len(program): 
            return tokens


