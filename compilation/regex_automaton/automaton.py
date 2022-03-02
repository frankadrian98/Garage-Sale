
from typing import List, Dict, Tuple, Any
import itertools as it


class CustomSet(set):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = -1
        self.is_final = False
        self.types = []

class Automaton:
    
    def __init__(self,states,transitions,final_states,initial_state = 0): 
        self.states = states
        self.transitions = transitions
        self.final_states = final_states
        self.initial_state = initial_state
        self.current = initial_state

        self.alphabet = set()
        for (_, symbol) in transitions.keys():
            if symbol:
                self.alphabet.add(symbol)
    
    def __and__(self,other):
        return self.concat(other)

    def __or__(self,other):
        return self.union(other)

    def __str__(self):
        """"Pretty Print"""

        output = "\nAutomaton" + \
                 "\nStates " + str(self.states) + \
                 "\nAlphabet " + str(self.alphabet) + \
                 "\nTransitions " + str(self.transitions) + \
                 "\nInital State " + str(self.initial_state) + \
                 "\nFinal States " + str(self.final_states)

        return output
    
    def match(self, program, start_index=0):
        self.current = self.initial_state
        step_count = start_index
        for i in range(start_index, len(program)):
            _next = self.transitions.get((self.current, program[i]), [None])[0]
            if not _next:
                return self.current in self.final_states.keys(), i - start_index
            self.current = _next
        if start_index != len(program):
            step_count += 1
        return self.current in self.final_states.keys(), step_count - start_index
    
    def get_type(self, state):
        types = self.final_states.get(state)
        if not types:
            return
        return min(types,key= lambda x:x[1])[0]
    
    def add_type(self, type):
        transitions = dict(self.transitions)
        finals = {k: value + [type] for k, value in self.final_states.items()}       
        return Automaton(self.states, transitions, finals, self.initial_state)
        
    
    def move(self, states, symbol):
        n_states = set()
        for state in states:
            if p_states := self.transitions.get((state, symbol)):
                n_states.update(set(p_states))
        return list(n_states)
    
    def e_closure(self, states):
        visited = set(states)
        n_states = CustomSet(states)
        stack = list(visited)
        while stack:
            state = stack.pop()
            if p_states := self.transitions.get((state, "")):
                n_states.update(p_states)
                for n_state in p_states:
                    if n_state not in visited:
                        stack.append(n_state)
                visited.update(p_states)
        return n_states
    
    def nfa_to_dfa(self):
        transitions = {}        
        start = self.e_closure([self.initial_state])
        start.id = 0
        start.is_final = any(s in self.final_states for s in start)
        start.types = set()
        for types in (self.final_states.get(s) for s in start if s in self.final_states):
            start.types.update(types)        
        states = [start]
        pending = [start]        
        while pending:
            state = pending.pop()
            for symbol in self.alphabet:
                q = self.e_closure(self.move(state, symbol))
                if not q:
                    continue
                
                if q not in states:
                    q.id = len(states)
                    q.is_final = any(s in self.final_states for s in q)
                    q.types = set()
                    for types in (self.final_states.get(s) for s in q if s in self.final_states):
                        q.types.update(types)
                    states.append(q)
                    pending.append(q)
                else:
                    for s in states:
                        if q == s:
                            q = s                
                transitions[(state.id, symbol)] = (q.id,)        
        finals = {s.id: list(s.types) for s in states if s.is_final}        
        return Automaton(len(states), transitions, finals, start.id) 
    
    def concat(self, other: "Automaton"):
        l1 = self.states
        l2 = other.states
        states = l1 + l2
        initial = self.initial_state
        transitions = dict(self.transitions)        
        for state in self.final_states:
            transitions[(state, "")] = transitions.get((state, ''), ()) + (other.initial_state + l1,)       
        for (state, c), new_states in other.transitions.items():
            transitions[(state + l1, c)] = tuple([s + l1 for s in new_states])               
        finals = {s + l1: list(types) for s, types in other.final_states.items()}        
        return Automaton(states, transitions, finals, initial)

    def union(self, other: "Automaton"):
        transitions = {}
        start = 0
        offset = self.states + 1        
        transitions[(start, '')] = (self.initial_state + 1, other.initial_state + offset)        
        for (state, c), new_state in self.transitions.items():
            transitions[(state + 1, c)] = tuple(ns + 1 for ns in new_state)
        for (state, c), new_state in other.transitions.items():
            transitions[(state + offset, c)] = tuple(ns + offset for ns in new_state)              
        finals = {s + 1: list(types) for s, types in self.final_states.items()}
        finals.update({s + offset: list(types) for s, types in other.final_states.items()})        
        return Automaton(self.states + other.states + 1, transitions, finals, start)

    def closure(self):
        transitions = dict(self.transitions)        
        for state in self.final_states:
            transitions[(state, '')] = transitions.get((state, ''), ()) + (self.initial_state,)        
        finals = {k: list(types) for k, types in self.final_states.items()}        
        all_types = set()
        for types in finals.values():
            all_types.update(types)        
        finals.update({self.initial_state: list(all_types)})      
        return Automaton(self.states, transitions, finals, self.initial_state)
   

