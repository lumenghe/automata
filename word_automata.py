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
    def __init__(self):
        self.initial_state = State()
        self.compressed = False # once an automaton is compressed, we cannot add new words
        self.mode = "history"

    def __iter__(self):
        """
        generator listing all the states in the automaton
        mark: memorize states already encountered, only list new states (useful when
            the automaton is compressed
        history: list both states and the word leading to each state
        """
        if self.mode == 'mark':
            marked = set()
            stack = [self.initial_state]
        elif self.mode == 'history':
            stack = [("", self.initial_state)]
        else:
            raise ValueError("unknown mode '{}'".format(self.mode))

        while stack:
            if self.mode == 'mark':
                state = stack.pop()
                if state not in marked:
                    marked.add(state)
                    stack += state.transitions.values()
                    yield state
            else: # history mode
                history, state = stack.pop()
                for l,s in state.transitions.items():
                    stack.append((history+l, s))
                yield history, state

    def add_word(self, word, count=False):
        """
        Add transition in the automaton to recognize a new word
        """
        if self.compressed:
            raise RuntimeError("Automaton is compressed. Cannot add new words (recognized language might become different)!")
        current_state = self.initial_state
        for letter in word:
            current_state = current_state.next_state(letter, add_transition=True)
        current_state.is_final = True

    def accept_word(self, word):
        """
        Check if a word is accepted or not by the automaton
        """
        current_state = self.initial_state
        for letter in word:
            current_state = current_state.next_state(letter)
            if current_state == None:
                return False
        return current_state.is_final

    def print_words(self):
        """
        Print all the words recognized by the automaton
        """
        self.mode = "history"
        for h,s in self:
            if s.is_final:
                print(h)

    def get_leaves(self):
        """
        Get the list of leaf states (without outgoing transition)
        """
        self.mode = "mark"
        leaves = []
        for s in self:
            if not len(s.transitions):
                leaves.append(s)
        return leaves

    def count_words(self):
        """
        Count the number of words recognized by the automaton
        """
        self.mode = "history"
        count = 0
        for _, s in self:
            if s.is_final:
                count += 1
        return count

    def count_states(self):
        """
        Count the number of states in the automaton
        """
        self.mode = "mark"
        count = 0
        for s in self:
            count += 1
        return count

    def renumber_states(self):
        """
        Change state ids to be consecutive
        """
        self.mode = "mark"
        count = 0
        for s in self:
            s.number = count
            count += 1
        State.count = count

    def __str__(self):
        self.mode = "mark"
        r = ""
        for s in self:
            r += str(s)
            for l,t in s.transitions.items():
                r += " " + l + ":" + str(t)
            r += "\n"
        return r.strip()

    def merge_states(self, states):
        """
        Merge a list of states in the automaton
        """
        if not len(states):
            raise ValueError("Cannot merge empty list of states!")
        if any(s.is_final != states[0].is_final for s in states):
            raise ValueError("Cannot merge final and non-final states!")
        new_state = State()
        new_state.is_final = states[0].is_final
        for s in states:
            for letter,child in s.transitions.items():
                c = new_state.transitions.get(letter, child)
                if c != child:
                    raise RuntimeError("Critical error when merging states (states should not be merged)!")
                new_state.transitions[letter] = child
            for p,letters in s.parents.items():
                for l in letters:
                    p.transitions[l] = new_state
            new_state.parents.update(s.parents)
            del s
        return new_state
