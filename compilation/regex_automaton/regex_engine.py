
class RegexEngine:

    def __init__(self,grammar,gramar_starter,lexer,parse_func):
        self.grammar = grammar
        self.grammar_starter = gramar_starter
        self.lexer = lexer()
        self.parse_func = parse_func

    def compile(self,expr):

        tokens = self.lexer.tokenize(expr)
        ast = self.parse_func(self.grammar,{},tokens,self.grammar_starter)
        return ast.handle().nfa_to_dfa()

