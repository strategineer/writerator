#!/usr/bin/env python3

# Copyright 2012 Bill Tyros
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os
import io
import sys
from collections import Counter

from BasicText import BasicText
from Phrase import Phrase
from Word import Word
from Letter import Letter


class Text(BasicText):
    """Represents a human language text."""
    
    # Represents the kinds of elements contained within texts, namely words (w),
    # letters(l), phrases(p)
    types_of_elements = ['w', 'l', 'p']
    
    def __init__(self, filename):
        """Initializes a Text."""
        super( Text, self ).__init__(Text.get_text_from_txt_file(filename))

    def clean_elements(elements):
        """
            Cleans a list of elements by removing unnecessary punctuation,
            whitespace from each element and returns the result.
        """
        # Clean up elements. Remove whitespace, remove punctuation
        elements = [element.rstrip(".,").strip() for element in elements]
        # Removes empty string
        elements = filter(None, elements)
        
        return elements

    def get_text_from_txt_file(filename_in):
        """Rips the text from a plain text file and returns it as a str."""
        if os.path.isfile(filename_in):
            with io.open(filename_in, 'r') as file:
                lines = file.readlines()
            
            lines = [x.strip() for x in lines]
            return " ".join(lines)

        else:
            logging.error("No such filename: " + filename_in)
            sys.exit(0)
    
    def parse_phrases(self):
        """Parses a Text and returns a list containing the phrases as Phrases"""
        phrases = self.text.split(".")
            
        phrases = Text.clean_elements(phrases)
        return [Phrase(phrase) for phrase in phrase]
    
    def parse_words(self):
        """Parses a Text and returns a list containing the words as Words"""
        words = self.text.split(" ")
        
        words = Text.clean_elements(words)
        return [Word(word) for word in words]
    
    def parse_letters(self):
        """Parses a Text and returns a list containing the letters as Letters"""
        letters = list(self.text)
        
        letters = Text.clean_elements(letters)
        return [Letter(letter) for letter in letters]
    
    def split_text_by_element(self, kind=types_of_elements[0]):
        """
            Splits the text by element and returns a list
            
            i.e. "Bill. Is. Cool." => words (w) => ["Bill.", "Is.", "Cool."]
            "Bill. Is. cool." => letters (l) => ["B", "i", "l", "l", "I", "s", ...]
            "Bill. Is very. cool." => phrases (p) => ["Bill", "Is very", "Cool"]
        """
        if kind in Text.types_of_elements:
            if kind == 'w':
                return self.parse_words()
            
            elif kind == 'p':
                return self.parse_phrases()

            elif kind == 'l':
                return self.parse_letters()
        
        else:
            logging.error("No such type available cannot split: " + kind)
            logging.error("try: " + str(Text.types_of_elements))
            sys.exit(0)
        
    def rank_by_total_count(self, kind=types_of_elements[0]):
        """
            Returns a list of tuples containing the number of occurrences of each
            element [words (w), letters (l) or phrases (p)] found in the Text and
            the str form of the elements.
            
            The list is sorted by number of occurences in decreasing order.
        """
        if kind in Text.types_of_elements:
            elements = self.split_text_by_element(kind)
            
            occurences = Counter( [str(x) for x in elements] )
            
            return occurences.most_common()
        
        else:
            logging.error("No such type available cannot rank by occurrences: "
                          + kind)
            logging.error("try: " + str(Text.types_of_elements))
            sys.exit(0)
    
    def rank_by_number_of_matches(self, string_to_match, kind=types_of_elements[0]):
        """
            Returns a list of tuples containing the number of matches found in
            each element [words (w), letters (l) or phrases (p)] of the Text and
            the str form of the element.
            
            The list is sorted by number of matches in decreasing order.
        """
        if kind in Text.types_of_elements:
            elements = self.split_text_by_element(kind)
            set_of_elements = set(elements)
            
            ranked_by_matches = []
            
            for element in set_of_elements:
                ranked_by_matches.append( (element, element.count(string_to_match) ) )

            ranked_by_matches.sort(reverse=True, key=lambda x: x[1])
            
            return ranked_by_matches
        
        else:
            logging.error("No such type available cannot rank by matches: " + kind)
            logging.error("try: " + str(Text.types_of_elements))
            sys.exit(0)

    def find_all_adverbs(self):
        """Finds all the adverbs in the text."""
        words = self.split_text_by_element('w')
        adverbs = []
        
        for word in words:
            word_obj = Word(word)
            if word_obj.isAdverb():
                adverbs.append(word)
        
        return adverbs
    
    def __repr__(self):
        return self.__str__()