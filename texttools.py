#!/usr/bin/env python3

import logging
import sys
from functools import total_ordering

import re
import os
import io
import random
from collections import Counter

from hyphen import Hyphenator

from datastore import DataStore
from prob import ProbabilityCounter

MAX_POEM_LINE_ITERATIONS = 100
MAX_FUZZ_FOR_SYLLABLES = 0
FORBIDDEN_LAST_WORDS = set(["and", "the", "to", "of", "for", "a", "into", "from"])

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

    def countSyllables(self):
        """ Counts the number of syllables for an English language Word.  """
        n_syllables = len(Word.h_en.syllables(self.text))
        if n_syllables != 0:
            return n_syllables
        return 1

    def isAdverb(self):
        """Determines whether word is an adverb."""
        return re.match(r"\w+ly", self.text)

class Text(BasicText):
    """Represents a human language text."""

    _element_types = ['characters', 'words', 'sentences']

    def __init__(self, filename):
        """Initializes a Text."""
        assert filename
        self.filename = filename
        self.text = self.get_text_from_txt_file()
        self.first_word_picker = None
        self.markov_chain_word_pickers = None

        ds_keys_values = []
        if DataStore.is_to_be_computed(filename):
            logging.debug(f"{filename}'s cache needs to be recomputed")
            ds_keys_values = self.__compute_ds_keys_values()

        database = DataStore(filename, ds_keys_values)
        self.ds = database

    def get_text_from_txt_file(self):
        """Rips the text from a plain text file and returns it as a str."""
        if os.path.isfile(self.filename):
            with io.open(self.filename, 'r') as file:
                lines = file.readlines()

            lines = [x.strip() for x in lines]

            return " ".join(lines)

        else:
            logging.error("No such filename cannot get text: " + self.filename)
            sys.exit(1)

    def __compute_ds_keys_values(self):
        """
            Computes process intensive data as key-value pairs and returns a
            list containing each.
        """
        data_tuples = []

        words = self._split_by_element_type(Text._element_types[1])
        words_tpl = (Text._element_types[1], words)
        data_tuples.append(words_tpl)

        sentences = self._split_by_element_type(Text._element_types[2])
        sentences_tpl = (Text._element_types[2], sentences)
        data_tuples.append(sentences_tpl)

        characters = self._split_by_element_type(Text._element_types[0])
        characters_tpl = (Text._element_types[0], characters)
        data_tuples.append(characters_tpl)

        return data_tuples

    def _split_by_element_type(self, element_type):
        """
            Splits a text into a list elements depending on the given
            element_type.
        """
        def _parse_sentences(text):
            """Parses a Text and returns a list containing the sentences as Sentences"""
            sentences = text.split('.')

            return [Sentence(sentence) for sentence in sentences if sentence]

        def _parse_words(text):
            """Parses a Text and returns a list containing the words as Words"""
            words = text.split(" ")

            return [Word(word) for word in words if word]

        def _parse_characters(text):
            """Parses a Text and returns a list containing the characters"""
            characters = list(text)

            return characters

        if element_type == Text._element_types[0]:
            return _parse_characters(self.text)

        elif element_type == Text._element_types[1]:
            return _parse_words(self.text)

        elif element_type == Text._element_types[2]:
            return _parse_sentences(self.text)

    def generate_poem(self, syllables_per_line):
        """Generate poems using the words contained within the Text"""
        # TODO(keikakub): improve this algorithm, this method kind of sucks
        #   (Markov Chains would be a good start to generating poetry that makes more sense)
        words = self.ds[Text._element_types[1]]
        n_words = len(words) - 1
        if not self.first_word_picker:
            self.first_word_picker = ProbabilityCounter(Counter(words))
        unique_words = list(set(words))
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
                        adjacent_words = [words[i+1] for i, e in enumerate(words) if e == next_word and i < n_words]
                        self.markov_chain_word_pickers[next_word] = ProbabilityCounter(Counter(adjacent_words))
                    next_word = self.markov_chain_word_pickers[next_word].get()
                else:
                    next_word = self.first_word_picker.get()
                random_words.append(next_word)
                n_syllables += next_word.countSyllables()
                if abs(n_syllables - syllables_needed) <= MAX_FUZZ_FOR_SYLLABLES and str(next_word) not in FORBIDDEN_LAST_WORDS:
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
                    n_syllables  = 0

            poem_line = " ".join([str(word) for word in random_words])
            print(poem_line.lower().capitalize())

    def calculate_Gunning_Fog_Index(self):
        """Calculates and returns the text's Gunning-Fog index."""
        words = self.ds[Text._element_types[1]]
        complex_words = [word for word in words if word.countSyllables() >= 3]

        number_of_words = len(words)
        number_of_complex_words = len(complex_words)
        number_of_sentences = len(self.ds[Text._element_types[2]])

        return (0.4) * ( (number_of_words / number_of_sentences)
                         + 100 * (number_of_complex_words / number_of_words) )

    def _make_occurences_Counter(self, element_type):
        """Returns a Counter with the elements decided by kind, either
         words, characters or sentences as keys from within a Text."""
        elements = self.ds[element_type]
        return Counter( [str(x) for x in elements] )

    def count_occurences(self, element_to_count, element_type):
        """Return the total number of times an element appears in a Text."""
        occurences = self._make_occurences_Counter(element_type)

        if element_to_count in occurences:
            return occurences[element_to_count]
        else:
            return 0

    def rank_by_number_of_matches(self, matches_to_check, element_type):
        """
            Returns a list of tuples containing the number of matches found in
            each element of the Text and the str form of the element.

            The list is sorted by number of matches in decreasing order.
        """
        assert isinstance(matches_to_check, list)

        if element_type in Text._element_types:
            set_of_elements = set(self.ds[element_type])

            ranked_by_matches = []

            for element in set_of_elements:

                current_element_count = 0
                for match in matches_to_check:
                    current_element_count += element.count(match)

                ranked_by_matches.append( (element, current_element_count ) )

            ranked_by_matches.sort(reverse=True, key=lambda x: x[1])

            return ranked_by_matches

        else:
            logging.error("No such type available cannot rank by matches: " + element_type)
            logging.error("try: " + str(Text._element_types))
            sys.exit(1)

    def rank_by_total_count(self, element_type):
        """
            Returns a list of tuples containing the number of occurrences of each
            element found in the Text and
            the str form of the elements.

            The list is sorted by number of occurences in decreasing order.
        """
        if element_type in Text._element_types:
            occurences = self._make_occurences_Counter(element_type)

            return occurences.most_common()

        else:
            logging.error("No such type available cannot rank by occurrences: "
                          + element_type)
            logging.error("try: " + str(Text._element_types))
            sys.exit(1)

    def find_all_adverbs(self):
        """Finds all the adverbs in the text."""
        words = self.ds[Text._element_types[1]]
        adverbs = []

        for word in words:
            if word.isAdverb():
                adverbs.append(word)

        return adverbs
