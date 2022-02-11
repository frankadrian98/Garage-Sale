import string


class Token:
    pass


class ElementToken(Token):
    def __init__(self, symbol: str):
        super().__init__()
        self.type = 'element'
        self.symbol = symbol


class WildCardToken(Token):
    def __init__(self, wildcard_symbol: str):
        super().__init__()
        self.type = 'wildcard'
        self.wildcard_symbol = wildcard_symbol
        self.symbol = wildcard_symbol

class Dot(WildCardToken):
    def __init__(self):
        super().__init__('.')

class SpaceToken(Token):
    def __init__(self, space_symbol: str):
        super().__init__()
        self.type = 'space'
        self.space_symbol = space_symbol
        self.symbol = string.whitespace

class StartToken(Token):
    def __init__(self, start_symbol: str):
        super().__init__()
        self.type = 'start'
        self.start_symbol = start_symbol
        self.symbol = start_symbol


class Start(StartToken):
    def __init__(self):
        super().__init__('^')


class EOFToken(Token):
    def __init__(self, eof_symbol: str):
        super().__init__()
        self.type = 'end'
        self.eof_symbol = eof_symbol
        self.symbol = eof_symbol


class EOF(EOFToken):
    def __init__(self):
        super().__init__('$')


class EscapeToken(Token):
    def __init__(self):
        super().__init__()
        self.type = 'escape'
        self.escape_symbol = '\\'
        self.symbol = '\\'


class CommaToken(Token):
    def __init__(self):
        super().__init__()
        self.type = 'comma'
        self.symbol = ','


class ParenthesisToken(Token):
    def __init__(self, side: str):
        super().__init__()
        self.type = 'parenthesis'
        self.side = side


class LParenthesisToken(ParenthesisToken):
    def __init__(self):
        super().__init__('L')
        self.symbol = '('


class RParenthesisToken(ParenthesisToken):
    def __init__(self):
        super().__init__('R')
        self.symbol = ')'


class BraceToken(Token):
    def __init__(self, side: str):
        super().__init__()
        self.type = 'brace'
        self.side = side


class LBraceToken(BraceToken):
    def __init__(self):
        super().__init__('L')
        self.symbol = '{'


class RBraceToken(BraceToken):
    def __init__(self):
        super().__init__('R')
        self.symbol = '}'


class BracketToken(Token):
    def __init__(self, side: str):
        super().__init__()
        self.type = 'bracket'
        self.side = side


class LBracketToken(BracketToken):
    def __init__(self):
        super().__init__('L')
        self.symbol = '['


class RBracketToken(BracketToken):
    def __init__(self):
        super().__init__('R')
        self.symbol = ']'


class OperatorToken(Token):
    def __init__(self, quantity: int, operator_symbol: str):
        super().__init__()
        self.type = 'operator'
        self.quantity = quantity
        self.operator_symbol = operator_symbol
        self.symbol = operator_symbol

class StarToken(OperatorToken):
    def __init__(self):
        super().__init__('ZeroOrMore','*')


class PlusToken(OperatorToken):
    def __init__(self):
        super().__init__('OneOrMore','+')


class QuestionToken(OperatorToken):
    def __init__(self):
        super().__init__('ZeroOrOne','?')


class OrToken(Token):
    def __init__(self):
        super().__init__()
        self.type = 'or'
        self.symbol = '|'


class ComplementToken(Token):
    def __init__(self):
        super().__init__()
        self.type = 'complement'
        self.symbol = '^'


class MinusToken(Token):
    def __init__(self):
        super().__init__()
        self.type = 'minus'
        self.ch = '-'
        self.symbol = '-'