import string


class Token:
    pass


class ElementToken(Token):
    def __init__(self, value: str):
        super().__init__()
        self.type = 'element'
        self.value = value


class WildCardToken(Token):
    def __init__(self, wildcard_symbol: str):
        super().__init__()
        self.type = 'wildcard'
        self.wildcard_symbol = wildcard_symbol
        self.value = wildcard_symbol

class Dot(WildCardToken):
    def __init__(self):
        super().__init__('.')

class SpaceToken(Token):
    def __init__(self, space_symbol: str):
        super().__init__()
        self.type = 'space'
        self.space_symbol = space_symbol
        self.value = string.whitespace

class StartToken(Token):
    def __init__(self, start_symbol: str):
        super().__init__()
        self.type = 'start'
        self.start_symbol = start_symbol
        self.value = start_symbol


class Start(StartToken):
    def __init__(self):
        super().__init__('^')


class EOFToken(Token):
    def __init__(self, eof_symbol: str):
        super().__init__()
        self.type = 'end'
        self.eof_symbol = eof_symbol
        self.value = eof_symbol


class EOF(EOFToken):
    def __init__(self):
        super().__init__('$')


class EscapeToken(Token):
    def __init__(self):
        super().__init__()
        self.type = 'escape'
        self.escape_symbol = '\\'
        self.value = '\\'


class CommaToken(Token):
    def __init__(self):
        super().__init__()
        self.type = 'comma'
        self.value = ','


class ParenthesisToken(Token):
    def __init__(self, side: str):
        super().__init__()
        self.type = 'parenthesis'
        self.side = side


class LParenthesisToken(ParenthesisToken):
    def __init__(self):
        super().__init__('L')
        self.type = 'pl'
        self.value = '('


class RParenthesisToken(ParenthesisToken):
    def __init__(self):
        super().__init__('R')
        self.type = 'pr'
        self.value = ')'


class BraceToken(Token):
    def __init__(self, side: str):
        super().__init__()
        self.type = 'brace'
        self.side = side


class LBraceToken(BraceToken):
    def __init__(self):
        super().__init__('L')
        self.type = 'bl'
        self.value = '{'


class RBraceToken(BraceToken):
    def __init__(self):
        super().__init__('R')
        self.type = 'br'
        self.value = '}'


class BracketToken(Token):
    def __init__(self, side: str):
        super().__init__()
        self.type = 'bracket'
        self.side = side


class LBracketToken(BracketToken):
    def __init__(self):
        super().__init__('L')
        self.type = 'sbl'
        self.value = '['


class RBracketToken(BracketToken):
    def __init__(self):
        super().__init__('R')
        self.type = 'sbr'
        self.value = ']'


class OperatorToken(Token):
    def __init__(self, quantity: int, operator_symbol: str):
        super().__init__()
        #self.type = 'operator'
        self.quantity = quantity
        self.operator_symbol = operator_symbol
        self.value = operator_symbol

class StarToken(OperatorToken):
    def __init__(self):
        super().__init__('ZeroOrMore','*')
        self.type = 'star'


class PlusToken(OperatorToken):
    def __init__(self):
        super().__init__('OneOrMore','+')
        self.type = 'plus'


class QuestionToken(OperatorToken):
    def __init__(self):
        super().__init__('ZeroOrOne','?')
        self.type = 'question'


class OrToken(Token):
    def __init__(self):
        super().__init__()
        self.type = 'or'
        self.value = '|'


class ComplementToken(Token):
    def __init__(self):
        super().__init__()
        self.type = 'not'
        self.value = '^'


class MinusToken(Token):
    def __init__(self):
        super().__init__()
        self.type = 'minus'
        self.ch = '-'
        self.value = '-'