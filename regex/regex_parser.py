import numpy as np
from .regex_lexer import RegLexer
from .regex_token import *
from .regex_ast import *
from functools import lru_cache

class RegParser:


    def __init__(self):
        self.lexer = RegLexer()
    @lru_cache(maxsize=4)
    def parse(self, exp: str):
        
        def get_range(start: str, end: str):

            ans = ''
            i = ord(start)
            while i <= ord(end):
                ans += chr(i)
                i += 1

            return ans

        def next_token_reset(exp: str):

            tokens = self.lexer.tokenize(exp)
            i = -1

            def next_token(not_consumed: bool = False):

                nonlocal i
                nonlocal tokens
                nonlocal current_token

                if not_consumed:
                    return tokens[i+1] if len(tokens) > i+1 else None

                i += 1
                if i < len(tokens):
                    current_token = tokens[i]
                else:
                    current_token = None

            return next_token

        def parse_exp():
            return RegNode(parse_exp_extend())

        def parse_exp_extend(is_capturing: bool = True, group_name: str = 'group'):

            _start = False 
            _end = False

            if type(current_token) is Start or type(current_token) is ComplementToken:
                next_token()
                _start = True

            current_node = parse_group(is_capturing=is_capturing, group_name=group_name)

            if isinstance(current_token, EOFToken):
                next_token()
                _end = True
            else:
                _end = False

            if _start:
                current_node.children.appendleft(StartNode())
            if _end:
                current_node.children.append(EOFNode())

            if isinstance(current_token, OrToken):
                next_token()
                current_node = OrNode(current_node, parse_exp_extend())

            return current_node

        def parse_group(is_capturing: bool = True, group_name: str = 'group'):

            childrens = deque() 

            while current_token is not None and not isinstance(current_token, OrToken) and not isinstance(current_token, RParenthesisToken) and not isinstance(current_token, EOFToken):

                new_children = parse_range_el()
                next_token()

                if isinstance(current_token, EOFToken):
                    childrens.append(new_children)
                    break

                if isinstance(current_token, OperatorToken):
                    if isinstance(current_token, QuestionToken):
                        new_children.min = 0
                        new_children.max = 1
                    elif isinstance(current_token, StarToken):
                        new_children.min = 0
                        new_children.max = np.inf
                    else:
                        new_children.min = 1
                        new_children.max = np.inf
                    next_token()
                elif isinstance(current_token, LBraceToken):
                    parse_brace(new_children)

                childrens.append(new_children)

            return GroupNode(childrens,is_capturing,group_name)

        def parse_brace(new_children: Node):

            next_token()
            fst_value = '' 
            snd_value = ''

            try:
                while isinstance(current_token, ElementToken):
                    fst_value += current_token.symbol
                    next_token()
                if fst_value == '':
                    fst_value == 0
                else:
                    fst_value = int(fst_value)

                if isinstance(current_token, RBraceToken):
                    if type(fst_value) is int:
                        new_children.min = fst_value
                        new_children.max = fst_value
                        next_token()
                        return
                    else:
                        raise Exception()

                next_token()
                while isinstance(current_token, ElementToken):
                    snd_value += current_token.symbol
                    next_token()
                if snd_value == '':
                    snd_value == np.inf
                else:
                    snd_value = int(snd_value)

                next_token()

                new_children.min = fst_value if type(fst_value) is int else 0
                new_children.max = snd_value if type(snd_value) is int else np.inf

            except Exception as e:
                raise Exception('Invalid brace syntax.')

        def parse_range_el():
            if isinstance(current_token, LBracketToken):
                next_token()
                inner = parse_inner()
                if isinstance(current_token, RBracketToken):
                    return inner
                else:
                    raise Exception('Missing \']\', please check the regex.')
            else:
                return parse_single()

        def parse_inner():

            nonlocal current_token
            _str = ''
            if current_token is None:
                raise Exception('Missing \']\', please check the regex.')

            positive = True
            if isinstance(current_token, ComplementToken):
                positive = False
                next_token()

            _prev = None
            while current_token is not None:
                if isinstance(current_token, RBracketToken):
                    break

                if isinstance(current_token, SpaceToken):
                    _str += current_token.symbol
                    next_token()
                    continue

                if not isinstance(current_token, ElementToken):
                    current_token = ElementToken(current_token.symbol)

                if next_token(not_consumed=True) is None:
                    raise Exception("Missing  \']'\ , please check the regex.")
                elif isinstance(next_token(not_consumed=True), MinusToken):
                    _prev = current_token.symbol
                    next_token()
                    if isinstance(next_token(not_consumed=True), RBracketToken) or isinstance(next_token(not_consumed=True), SpaceToken):
                        _str += _prev + current_token.symbol
                    else:
                        next_token() 
                        if next_token is None:
                            raise Exception("Missing  \']'\ , please check the regex.")
                        elif ord(_prev) > ord(current_token.symbol):
                            raise Exception("Range values reversed, please check the regex")
                        else:
                            _str += get_range(_prev,current_token.symbol)
                else:
                    _str += current_token.symbol
                next_token()

            return RangeNode("".join(sorted(set(_str))), positive)

        def parse_single():
            group_name = None
            if isinstance(current_token, ElementToken):
                return ElementNode(current_token.symbol)
            elif isinstance(current_token, WildCardToken):
                return DotNode()
            elif isinstance(current_token, SpaceToken):
                return SpaceNode()
            elif isinstance(current_token, LParenthesisToken):
                next_token()
                is_capturing = True
                if type(current_token) is QuestionToken:
                    next_token()
                    if current_token.symbol == ':':
                        is_capturing = False
                        next_token()
                    elif current_token.symbol == '<':
                        next_token()
                        group_name = parse_group_name()
                    else:
                        if current_token is None:
                            raise Exception('Unterminated group')
                        else:
                            raise Exception('Invalid group')
                res = parse_exp_extend(is_capturing,group_name)
                if isinstance(current_token, RParenthesisToken):
                    return res
                else:
                    raise Exception('Missing right parenthesis \')\'')
            else:
                raise Exception('Unescaped special character {}'.format(current_token.symbol))

        def parse_group_name():
            if current_token is None:
                raise Exception('Unterminated named group name.')
            group_name = ''
            while current_token.symbol != '>':
                group_name += current_token.symbol
                next_token()
                if current_token is None:
                    raise Exception('Unterminated named group name.')
            if len(group_name) == 0:
                raise Exception('Unexpected empty named group name.')
            next_token()
            return group_name

        current_token = None
        next_token = next_token_reset(exp)
        next_token()

        ast = parse_exp()
        if current_token is not None:
            raise Exception("Unable to parse the entire regex.\nCheck the regex and try again.")
        return ast