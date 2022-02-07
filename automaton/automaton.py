from turtle import goto
from typing import Set, List, Tuple

EPSILON = ""

class Automaton:
    def __init__(self, states: set, initial_state: int, final_states: set, alphabet: List[str], transitions: dict) -> None:
        self.states = states
        self.initial_state = initial_state
        self.final_states = final_states
        self.alphabet = alphabet
        self.transitions = transitions
    
    @staticmethod
    def goto(states: set, text: str, transitions: dict) -> set:
        res = set()
        for s in states:
            if (s, text) in transitions:
                state = transitions[(s, text)]
                res = res.union(set(state))
        return res

    @staticmethod
    def epsilon_closure(states: set, transitions: dict) -> set:
        e_closure = states
        Q = [states]
        V = set()

        while Q:
            sts = Q.pop()
            to = Automaton.goto(sts, EPSILON, transitions)
            e_closure = e_closure.union(to)
            for state in to:
                if state not in V:
                    Q.append(set([state]))
                    V.add(state)
        return e_closure

    def nfa_to_dfa(automaton: "Automaton", lr=False) -> "Automaton":
        Q_dfa = []    
        alphabet = [c for c in automaton.alphabet]
        q0_dfa = Automaton.epsilon_closure(set([automaton.initial_state]), automaton.transitions)
        F_dfa = []
        transitions_dfa = {}
        s_number = {1: q0_dfa}
        states = [1]
        V = [q0_dfa]

        while states:
            number = states.pop(0)
            current = s_number[number]
            for c in alphabet:
                to = Automaton.goto(current, c, automaton.transitions)
                if to:
                    new_state = Automaton.epsilon_closure(to, automaton.transitions)
                    if new_state not in V:
                        V.append(new_state)
                        Q_dfa.append(new_state)
                        k = len(s_number) + 1
                        states.append(k)
                        transitions_dfa[number, c] = k
                        s_number[k] = new_state
                        i = new_state.intersection(set(automaton.final_states))
                        if i and (new_state not in F_dfa):
                            F_dfa.append(new_state)
                    else:
                        n = [number for number, str in s_number.items() if str == new_state][0]
                        transitions_dfa[(number, c)] = n
        
        if lr:
            new_states = [state for state in Q_dfa]
            new_transitions = { (new_states[i - 1], c): new_states[transitions_dfa[i, c] - 1] for i, c in transitions_dfa }
            return Automaton(new_states, new_states[0], new_states, alphabet, new_transitions)
        
        new_states = {state for state in s_number}
        new_transitions = {}
        f = []
        new_f = []
        k = 0
        for a, b in transitions_dfa:
            k += 1
            st = transitions_dfa[a, b]
            if (s_number[st] in F_dfa) and (s_number[st] not in f):
                f.append(s_number[st])
                new_f.append(new_states[st])
        
        for a, b in transitions_dfa:
            st = transitions_dfa[a, b]
            new_transitions[new_states[a], b] = new_states[st]
        aut = Automaton(new_states.values(), new_states[1], new_f, alphabet, new_transitions)
        return aut
                