# Word automata compression algorithm

Finite State Automata experiment on words. A prefix automaton is built from a list of words. I implemented a compression algorithm to minimize the size of the automaton by merging suffixes.

On a lexicon of 355k words, the algorithm compresses the prefix automaton to 15.33% of its original size and the resulting automaton is provably minimal in terms of number of states.

run:  python word_automata.py -i lexicon_english.txt -v