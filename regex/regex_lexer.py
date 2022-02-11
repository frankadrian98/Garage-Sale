from functools import lru_cache
from .regex_token import *


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
                tokens.append(WildcardToken())
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
            elif char == '{':
                tokens.append(LBraceToken())
                pos += 1
                while pos < len(exp):
                    char = exp[pos]
                    if char == ',':
                        tokens.append(CommaToken())
                    elif self.is_digit(char):
                        tokens.append(ElementToken(char))
                    elif char == '}':
                        tokens.append(RBraceToken())
                        break
                    else:
                        raise Exception('Bad token at index ${}.'.format(pos))
                    pos += 1
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

l = RegLexer()
