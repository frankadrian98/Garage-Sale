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
            token = tp.match(program, start, line, column)
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




    # tp_index = 0        
    # while tp_index < len(token_regexs):
    #     valid = False
        
    #     token_list: List[Token] = token_regexs[tp_index].match(program, start, line, column)

    #     if len(token_list)==0:
    #         tp_index+=1
    #         continue
    #     valid = True
    #     for token in token_list:    
    #         if token.value != None:
    #             tokens.append(token)
    #         if token.line != line:
    #             column = 1
    #         else:
    #             column += token.end - token.start
    #         line = token.line
    #     tp_index+=1
    #     if not valid:
    #         raise Exception(f"Token error {token}")
    # tokens.sort(key=lambda x:x.start)

    # return tokens