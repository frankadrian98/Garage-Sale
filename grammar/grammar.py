from typing import List

class Symbol:
    
    def __init__(self, symbol: str):
        self.symbol = symbol
    
    def __str__(self):
        return self.symbol

class NonTerminal(Symbol):

    def __init__(self,symbol:str):
        super().__init__(symbol)
        self.productions = []
    
    def add_production(self, production):
        self.productions.append(production)


class Terminal(Symbol):

    def __init__(self, symbol):
        super().__init__(symbol)

class Sentence:

    def __init__(self,*symbols):
        self.symbols = [symbol for symbol in symbols]
    
    def __str__(self):
        return ''.join(symbol for symbol in self.symbols)

class Epsilon(Symbol):
    
    def __init__(self):
        super().__init__('epsilon')
    
    def __str__(self):
        return 'e'

class EOF(Terminal):
    
    def __init__(self):
        super().__init__('$')

class Production:
    def __init__(self,non_terminal:NonTerminal,sentence:Sentence,atribute = None):
        self.left = non_terminal
        self.right = sentence
        self.atribute = atribute
    
    
    def __str__(self):
        return f"{self.left} -> {' | '.join(sentence for sentence in self.right)}"

class Grammar:
    def __init__(self, start:NonTerminal,non_terminals:List[NonTerminal],terminals:List[Terminal],productions:List[Production]):
        self.start = NonTerminal
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.productions = productions
        self.epsilon = Epsilon()
        self.EOF = EOF()


    def add_production(self, production : Production):
        production.left.productions.append(production)
        self.productions.append(production)


    def IsInNonTerminals(self, name):
        return self.noTerminals.__contains__(name)


    def IsInTerminals(self, name):
        return self.terminals.__contains__(name)
