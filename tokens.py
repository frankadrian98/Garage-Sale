from enum import Enum/

class TokenTypes(Enum):

    #Keywords
    AND = 1
    FOR = 2
    RETURN = 3
    BREAK = 4
    ELSE = 5
    IF = 6
    OR = 7
    WHILE = 8
    CLASS = 9

    #Operators
    ADD = 10
    SUBSTRACT = 11
    MULTIPLY = 12
    DIVIDE = 13
    GREATER = 14
    GREATER_EQUAL = 15
    LOWER = 16
    LOWER_EQUAL = 17
    EQUAL = 18
    NOT_EQUAL = 19
    ADD_EQUAL = 20
    SUBSTRACT_EQUAL = 21
    MULTIPLY_EQUAL = 22
    DIVIDE_EQUAL = 23

    #Delimiters
    LEFT_PARENTHESIS = 24
    RIGHT_PARENTHESIS = 25
    LEFT_BRACKET = 26
    RIGHT_BRACKET = 27
    LEFT_BRACES = 28
    RIGHT_BRACES = 29
    COMMA = 30
    DOTS = 31
    ASSIGN = 32
    COLON = 33
    SEMI_COLON = 34
    LINE_BREAK = 35

    #Literals 
    STRING = 36
    INT = 37
    FLOAT = 38

    #Specials
    TABS = 39
    SPACE = 40
    COMMENT = 41
    IDENTIFIER = 42

class Token:

    def __init__(self, line: int, column: int, token_type: TokenTypes, lexeme: str)
        self.line = line
        self.column = column
        self.token_type = token_type
        self.lexeme = lexeme
    
    