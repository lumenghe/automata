"""
Finite State Automata experiment of words. A prefix automaton is built
from a list of words. I implemented a compression algorithm to minimize
the size of the automaton by merging suffixes.

run:  python word_automata.py -i lexicon_english.txt -v
"""
from __future__ import print_function
import argparse
from collections import defaultdict, deque


class State(object):
    """
    Class for representing a automata state. Transitions to other
    states are recored in a dictionary. Parents (states with transition
    to the current state are recorded as well for the compression algorithm)
    """
    count = 0 # to give a single id to each state
    def __init__(self, parents=[]):
        self.is_final = False
        self.parents = defaultdict(list)
        for l,p in parents:
            self.parents[p].append(l)
        self.number = State.count # unique id for the node
        State.count += 1
        self.transitions = {}

    def next_state(self, letter, add_transition=False):
        """
        Transition to the next state when reading a letter. If the transition
        does not exist and add_transition=True, the transition is added to the
        automaton.
        """
        if add_transition:
            if not letter in self.transitions:
                new_state = State(parents=[(letter,self)])
                self.transitions[letter] = new_state
        return self.transitions.get(letter, None)

    def __hash__(self):
        return self.number

    def __repr__(self):
        r = "S_{}".format(self.number)
        if self.is_final:
            r += "_F" # suffix for final states
        return r

class Automaton(object):
    """
    Class of automata. An automaton is initialized empty, transitions are added
    using add_word method.
    """