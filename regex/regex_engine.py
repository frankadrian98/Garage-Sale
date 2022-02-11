from typing import Callable
from .regex_parser import RegParser
from .regex_ast import Node, ElementNode, GroupNode, LeafNode, ComplementNode, OrNode, RangeNode, RegNode, DotNode, EOFNode, StartNode

class Match:
    def __init__(self, ast_id: int, start: int, end: int, string: str, name: str) -> None:
        self.ast_id = ast_id
        self.name = name
        self.start = start
        self.end = end
        self.match = string[start:end]

class RegexEngine:
    def __init__(self):
        self.parser = RegParser()

    def match(self, exp: str, string: str, return_matches: bool = False, continue_matching: bool = False):

        def r_matches(ans: bool, pos: int, _matches: list, return_matches: bool):
            if return_matches:
                return ans, pos, _matches
            else:
                return ans, pos

        _matches = []
        str_consumed_pos = 0

        ans, pos, matches = self.match_and_return(exp, string)
        if ans:
            str_consumed_pos += pos
            _matches.append(matches)
        else:
            return r_matches(ans, str_consumed_pos, _matches, return_matches)

        if not continue_matching:
            return r_matches(ans, str_consumed_pos, _matches, return_matches)

        while True:
            string = string[pos:]
            if not len(string) > 0:
                return r_matches(ans, str_consumed_pos, _matches, return_matches)
            ans, pos, matches = self.match_and_return(exp, string)
            if ans:
                str_consumed_pos += pos
                _matches.append(matches)
            else:
                return r_matches(True, str_consumed_pos, _matches, return_matches)

    def match_and_return(self, exp: str, string: str):

        ast = self.parser.parse(exp)
        matches = []

        pos = 0

        def r_matches(ans: bool, pos: int):
            nonlocal matches
            matches.reverse()
            return ans, pos, matches

        def backtrack(_stack: list, pos: int, current: int):

            if len(_stack) == 0:
                return False, pos, current

            node_index, _min, matched_times, consumed_list = _stack.pop()

            if matched_times == _min:
                for cons in consumed_list:
                    pos -= cons
                return backtrack(_stack, pos, node_index)
            else:
                last_consumed = consumed_list.pop()
                new_pos = pos - last_consumed
                _stack.append(
                    (node_index, _min, matched_times - 1, consumed_list))
                return True, new_pos, current

        def save_matches(match_group: Callable, ast: Node, string: str, start: int):
            nonlocal matches

            ans, end = match_group(ast, string)

            if ast.is_capturing and ans == True:
                already_matched = False
                for match in matches:
                    if match.ast_id == ast.id:
                        match = Match(ast.id, start, end, string, ast.group_name)
                        already_matched = True
                        break
                if not already_matched:
                    matches.append(Match(ast.id, start, end, string, ast.group_name))

            return ans, end

        def match_group(ast: Node, string: str):

            nonlocal pos
            _stack = []
            current_node = ast.children[0] 
            i = 0 

            while i < len(ast.children):
                current_node = ast.children[i]

                if isinstance(current_node, OrNode):
                    before_pos = pos
                    _min,_max = current_node.min,current_node.max
                    j = 0
                    consumed_list = []
                    backtracking = False

                    while j < _max:
                        temp_pos = pos
                        ans, new_pos = match_group(ast=current_node.left, string=string)
                        if ans == True:
                            pass
                        else:
                            pos = temp_pos
                            ans, new_pos = match_group(current_node.right,string)

                        if ans == True:
                            consumed_list.append(new_pos - temp_pos)
                        elif _min <= j:
                            break
                        else:
                            can_bt, bt_pos, bt_i = backtrack(_stack, pos, i)
                            if can_bt:
                                i = bt_i
                                pos = bt_pos
                                backtracking = True
                                break
                            else:
                                return False, pos
                        j += 1
                    if not backtracking:
                        _stack.append((i, _min, j, consumed_list))
                        i += 1
                    continue

                elif isinstance(current_node, GroupNode):
                    _min, _max = current_node.min, current_node.max
                    j = 0
                    consumed_list = []
                    before_pos = pos
                    backtracking = False

                    while j < _max:
                        temp_pos = pos
                        ans, new_pos = save_matches(match_group, current_node, string, pos)
                        if ans == True:
                            consumed_list.append(new_pos - temp_pos)
                        elif _min <= j:
                            break
                        else:
                            can_bt, bt_pos, bt_i = backtrack(_stack, pos, i)
                            if can_bt:
                                i = bt_i
                                pos = bt_pos
                                backtracking = True
                                break
                            else:
                                return False, pos
                        j += 1

                    if not backtracking:
                        _stack.append((i, _min, j, consumed_list))
                        i += 1
                    continue

                elif isinstance(current_node, LeafNode):

                    _min, _max = current_node.min, current_node.max
                    j = 0
                    consumed_list = []
                    before_pos = pos
                    backtracking = False

                    while j < _max:
                        if pos < len(string):
                            if current_node.is_match(string[pos], pos, len(string)):
                                if not (isinstance(current_node, StartNode) or isinstance(current_node, EOFNode)):
                                    consumed_list.append(1)
                                    pos += 1
                            else:
                                if _min <= j:
                                    break
                                can_bt, bt_pos, bt_i = backtrack(_stack, before_pos, i)
                                if can_bt:
                                    i = bt_i
                                    pos = bt_pos
                                    backtracking = True
                                    break
                                else:
                                    return False, pos
                        else:
                            if isinstance(current_node, StartNode) or isinstance(current_node, EOFNode) and current_node.is_match(pos=pos, str_len=len(string)):
                                pass
                            elif _min <= j:
                                break
                            else:
                                can_bt, bt_pos, bt_i = backtrack(_stack, before_pos, i)
                                if can_bt:
                                    i = bt_i
                                    pos = bt_pos
                                    backtracking = True
                                    break
                                else:
                                    return False, pos
                        j += 1
                    if not backtracking:
                        _stack.append((i, _min, j, consumed_list))
                        i += 1
                    continue
                else:
                    return False, pos

            return True, pos

        i = 0
        _ = 0

        if len(string) == 0:
            ans, consumed = save_matches(match_group,ast,string,0)
            return r_matches(ans, consumed)

        while pos < len(string):
            ans, _ = save_matches(match_group,ast, string,pos)
            i += 1
            if ans:
                return r_matches(True, pos)
            else:
                pos = i
        return r_matches(False, _)
    
