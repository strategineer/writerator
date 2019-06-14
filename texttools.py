import logging
import sys
from functools import total_ordering

import re
import os
import io
import random
from collections import Counter

from hyphen import Hyphenator

from prob import ProbabilityCounter

MAX_POEM_LINE_ITERATIONS = 100
MAX_FUZZ_FOR_SYLLABLES = 0
# TODO(keikakub): figure out a better way of improving the end of lines than banning weird words
FORBIDDEN_LAST_WORDS = set(
    ["and", "the", "to", "of", "for", "a", "into", "from", "that", "was", "each", "on", "in", "your", "then", "were", "their"])


@total_ordering
class BasicText(object):
    """Represents a BasicText used for inheritance."""

    def __init__(self):
        """Initializes a BasicText."""
        self._text = None

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, new_text):
        self._text = new_text

    @text.deleter
    def text(self):
        del self._text

    def count(self, to_count):
        """Counts the number of times to_count appears in BasicText"""
        return self.text.count(to_count)

    def __hash__(self):
        """Computes a hash code for BasicText objects"""
        return hash(self.text)

    def __eq__(self, other):
        if isinstance(other, BasicText):
            return self.text == other.text
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, BasicText):
            return self.text < other.text
        else:
            return NotImplemented

    def __str__(self):
        """Returns str form of BasicText"""
        return self.text

    def __repr__(self):
        return self.__str__()


class Sentence(BasicText):
    """Represents a Sentence."""

    def __init__(self, text):
        """Initializes a Sentence."""
        self.text = text

    @BasicText.text.setter
    def text(self, new_text):
        self._text = new_text.strip(" .") + "."


class Word(BasicText):
    """Represents a Word."""

    if "hyphen" in sys.modules:
        h_en = Hyphenator('en_US')

    def __init__(self, text):
        """Initializes a Word."""
        self.text = text

    @BasicText.text.setter
    def text(self, new_text):
        self._text = new_text.strip(""" (),.?!;:\"\'""")

    def count_syllables(self):
        """ Counts the number of syllables for an English language Word.  """
        n_syllables = len(Word.h_en.syllables(self.text))
        if n_syllables != 0:
            return n_syllables
        return 1

    def is_adverb(self):
        """Determines whether word is an adverb."""
        return re.match(r"\w+ly", self.text)


class Text(BasicText):
    """Represents a human language text."""

    _element_types = ['characters', 'words', 'sentences']

    def __init__(self, file):
        """Initializes a Text."""
        # Rips the text from a plain text file and returns it as a str.
        f = open(file, 'r') if file else sys.stdin
        lines = f.readlines()
        lines = [x.strip() for x in lines]
        self.text = " ".join(lines)
        if f is not sys.stdin:
            f.close()
        self.first_word_picker = None
        self.markov_chain_word_pickers = None

        self._words = None
        self._sentences = None
        self._characters = None

    @property
    def characters(self):
        if not self._characters:
            self._characters = self._split_by_element_type(Text._element_types[0])
        return self._characters

    @characters.setter
    def characters(self, characters):
        self._characters = characters

    @property
    def words(self):
        if not self._words:
            self._words = self._split_by_element_type(Text._element_types[1])
        return self._words

    @words.setter
    def words(self, words):
        self._words = words

    @property
    def sentences(self):
        if not self._sentences:
            self._sentences = self._split_by_element_type(Text._element_types[2])
        return self._sentences

    @sentences.setter
    def sentences(self, sentences):
        self._sentences = sentences

    def get_elements(self, element_type):
        assert element_type in Text._element_types, f"No such type available cannot rank by matches: {element_type}"
        if element_type == Text._element_types[0]:
            return self.characters
        elif element_type == Text._element_types[1]:
            return self.words
        elif element_type == Text._element_types[2]:
            return self.sentences
        logger.error("Fatal error: element_type not found")
        sys.exit(1)

    def _split_by_element_type(self, element_type):
        """
            Splits a text into a list elements depending on the given
            element_type.
        """
        assert element_type in Text._element_types, f"No such type available cannot rank by matches: {element_type}"
        if element_type == Text._element_types[0]:
            # Parses a Text and returns a list containing the characters.
            return list(self.text)

        elif element_type == Text._element_types[1]:
            # Parses a Text and returns a list containing the words as Words.
            words = self.text.split(" ")
            return [Word(word) for word in words if word]

        elif element_type == Text._element_types[2]:
            # Parses a Text and returns a list containing the sentences as Sentences.
            sentences = self.text.split('.')
            return [Sentence(sentence) for sentence in sentences if sentence]

    def generate_poem(self, syllables_per_line):
        """Generate poems using the words contained within the Text"""
        # TODO(keikakub): improve this algorithm, this method kind of sucks
        #   (Markov Chains would be a good start to generating poetry that makes more sense)
        n_words = len(self.words) - 1
        if not self.first_word_picker:
            self.first_word_picker = ProbabilityCounter(Counter(self.words))
        unique_words = list(set(self.words))
        if not self.markov_chain_word_pickers:
            self.markov_chain_word_pickers = {}
        # Generate a poem.
        poem_lines = []
        fail_count = 0
        for syllables_needed in syllables_per_line:
            # Generate a poem line.
            poem_line = ""
            random_words = []
            n_syllables = 0
            next_word = None
            while True:
                if next_word:
                    if next_word not in self.markov_chain_word_pickers:
                        adjacent_words = [
                            self.words[i + 1]
                            for i, e in enumerate(self.words)
                            if e == next_word and i < n_words
                        ]
                        self.markov_chain_word_pickers[
                            next_word] = ProbabilityCounter(
                                Counter(adjacent_words))
                    next_word = self.markov_chain_word_pickers[next_word].get()
                else:
                    next_word = self.first_word_picker.get()
                random_words.append(next_word)
                n_syllables += next_word.count_syllables()
                if abs(n_syllables -
                       syllables_needed) <= MAX_FUZZ_FOR_SYLLABLES and str(
                           next_word) not in FORBIDDEN_LAST_WORDS:
                    # The words have the right number of syllables, let's combine them and return.
                    break
                elif n_syllables > syllables_needed:
                    fail_count += 1
                    if fail_count > MAX_POEM_LINE_ITERATIONS:
                        # We're at the fail-safe limit, let's return with the words we have anyway.
                        break
                    # The words have too many syllables, let's try again.
                    random_words = []
                    next_word = None
                    n_syllables = 0

            poem_line = " ".join([str(word) for word in random_words])
            print(poem_line.lower().capitalize())

    def calculate_Gunning_Fog_Index(self):
        """Calculates and returns the text's Gunning-Fog index."""
        complex_words = [word for word in self.words if word.count_syllables() >= 3]

        n_words = len(self.words)
        n_complex_words = len(complex_words)
        n_sentences = len(self.sentences)

        return (0.4) * ((n_words / n_sentences) + 100 *
                        (n_complex_words / n_words))

    def _make_occurrences_Counter(self, element_type):
        """Returns a Counter with the elements decided by kind, either
         words, characters or sentences as keys from within a Text."""
        assert element_type in Text._element_types, f"No such type available cannot rank by occurrences: {element_type}"
        elements = self.get_elements(element_type)
        return Counter([str(x) for x in elements])

    def count_occurrences(self, element_to_count, element_type):
        """Return the total number of times an element appears in a Text."""
        assert element_type in Text._element_types, f"No such type available cannot rank by occurrences: {element_type}"
        occurrences = self._make_occurrences_Counter(element_type)
        if element_to_count in occurrences:
            return occurrences[element_to_count]
        else:
            return 0

    def rank_by_number_of_matches(self, matches_to_check, element_type):
        """
            Returns a list of tuples containing the number of matches found in
            each element of the Text and the str form of the element.

            The list is sorted by number of matches in decreasing order.
        """
        assert isinstance(matches_to_check, list)
        assert element_type in Text._element_types, f"No such type available cannot rank by matches: {element_type}"
        set_of_elements = set(self.get_elements(element_type))
        ranked_by_matches = []
        for element in set_of_elements:
            current_element_count = 0
            for match in matches_to_check:
                current_element_count += element.count(match)
            ranked_by_matches.append((element, current_element_count))
        ranked_by_matches.sort(reverse=True, key=lambda x: x[1])
        return ranked_by_matches

    def rank_by_total_count(self, element_type):
        """
            Returns a list of tuples containing the number of occurrences of each
            element found in the Text and
            the str form of the elements.

            The list is sorted by number of occurrences in decreasing order.
        """
        assert element_type in Text._element_types, f"No such type available cannot rank by occurrences: {element_type}"
        occurrences = self._make_occurrences_Counter(element_type)
        return occurrences.most_common()

    def find_all_adverbs(self):
        """Finds all the adverbs in the text."""
        words = self.ds[Text._element_types[1]]
        adverbs = []

        for word in words:
            if word.is_adverb():
                adverbs.append(word)

        return adverbs
