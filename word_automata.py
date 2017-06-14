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