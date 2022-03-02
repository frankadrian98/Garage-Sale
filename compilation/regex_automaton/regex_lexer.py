from functools import lru_cache
from compilation.regex_automaton.regex_token import *


class RegLexer:
    def __init__(self):
        self.digits = '0123456789'

    def is_digit(self, char: str):
        return self.digits.find(char) > -1

    @lru_cache(maxsize=4)
    def tokenize(self, exp: str):
        tokens = []
        pos = 0
        escape_found = False
        while pos < len(exp):
            char = exp[pos]
            if escape_found:
                if char == 't':
                    tokens.append(ElementToken('\t'))
                if char == 's':
                    tokens.append(SpaceToken(char))
                else:
                    tokens.append(ElementToken(char))
            elif char == '\\':
                escape_found = True
                pos += 1 
                continue
            elif char == '.':
                tokens.append(Dot())
            elif char == '(':
                tokens.append(LParenthesisToken())
            elif char == ')':
                tokens.append(RParenthesisToken())
            elif char == '[':
                tokens.append(LBracketToken())
            elif char == '-':
                tokens.append(MinusToken())
            elif char == ']':
                tokens.append(RBracketToken())
            elif char == '^':
                if pos == 0:
                    tokens.append(Start())
                else:
                    tokens.append(ComplementToken())
            elif char == '$':
                tokens.append(EOF())
            elif char == '?':
                tokens.append(QuestionToken())
            elif char == '*':
                tokens.append(StarToken())
            elif char == '+':
                tokens.append(PlusToken())
            elif char == '|':
                tokens.append(OrToken())
            elif char == '}':
                tokens.append(RBraceToken())
            else:
                tokens.append(ElementToken(char))

            escape_found = False
            pos += 1

        return tokens


