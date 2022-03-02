from typing import List
from compilation._lexer.token_ import Token, TokenRegex
from compilation.regex_automaton.regex_engine import RegexEngine
from compilation.regex_automaton.regex_lexer import RegLexer
from compilation.regex_automaton.regex_ast import multi_union
from compilation._parser._parser import parse 
from compilation.regex_automaton.regex_grammar import test_grammar
from functools import lru_cache

@lru_cache
def tokenize(program: str, token_regexs: List[TokenRegex]):
    token_regexs = list(token_regexs)
    regex_engine = RegexEngine(test_grammar,test_grammar['O'][0],RegLexer,parse)
    for priority,tr in enumerate(token_regexs):
        tr.automaton = regex_engine.compile(tr.exp)
        tr.automaton = tr.automaton.add_type((tr.type,priority))
    lexer_automaton = multi_union(*map(lambda x: x.automaton, token_regexs)).nfa_to_dfa()
    tokens = []
    line = 1
    column = 1
    str_i = 0
    while str_i < len(program):
        were_match, match_len = lexer_automaton.match(program,str_i)

        if not were_match and match_len == 0:
            raise Exception('Invalid character '+program[str_i]+ ' at line '+str(line)+' column '+str(column))

        start = str_i
        end = str_i + match_len
        match = program[start:end]
        str_i = end
        match_type = lexer_automaton.get_type(lexer_automaton.current)

        if match_type == 'newline':
            line+=1
            column = 0
            continue
        
        if match_type == 'space':
            column += match_len
            continue        

        tokens.append(Token(match_type,match,start,end,line,column))
        column +=  match_len
    
    return tokens


