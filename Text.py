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
    
    #Represents the kind of sequences of characters able to be analyzed
    # w for words, l for letters
    types_of_sequences = ['w', 'l', 'p']
    
    def __init__(self, filename):
        """Initializes a Text."""
        super( Text, self ).__init__(Text.get_text_from_txt_file(filename))

    def clean_splitted_text(str_sequences):
        # Clean up sequences. Remove whitespace, remove punctuation
        str_sequences = [x.rstrip(".,").strip() for x in str_sequences]
        # Removes empty string
        str_sequences = filter(None, str_sequences)
        
        return str_sequences

    def get_text_from_txt_file(filename_in):
        """Rips the text from a plain text file as a str."""
        if os.path.isfile(filename_in):
            with io.open(filename_in, 'r') as file:
                lines = file.readlines()
            
            lines = [x.strip() for x in lines]
            return " ".join(lines)

        else:
            logging.error("No such filename: " + filename_in)
            sys.exit(0)
    
    def parse_phrases(self):
        split_text = self.text.split(".")
            
        split_text = Text.clean_splitted_text(split_text)
        return [Phrase(x) for x in split_text]
    
    def parse_words(self):
        split_text = self.text.split(" ")
        
        split_text = Text.clean_splitted_text(split_text)
        return [Word(x) for x in split_text]
    
    def parse_letters(self):
        split_text = list(self.text)
        
        split_text = Text.clean_splitted_text(split_text)
        return [Letter(x) for x in split_text]
    
    def split_text_by_sequence(self, kind=types_of_sequences[0]):
        """
            Splits the text by sequence and returns a list
            
            i.e. "Bill. Is. Cool." => words (w) => ["Bill.", "Is.", "Cool."]
            "Bill. Is. cool." => letters (l) => ["B", "i", "l", "l", "I", "s", ...]
            "Bill. Is very. cool." => phrases (p) => ["Bill", "Is very", "Cool"]
        """
        if kind in Text.types_of_sequences:
            if kind == 'w':
                return self.parse_words()
            
            elif kind == 'p':
                return self.parse_phrases()

            elif kind == 'l':
                return self.parse_letters()
        
        else:
            logging.error("No such type available cannot split: " + kind)
            logging.error("try: " + str(Text.types_of_sequences))
            sys.exit(0)
        
    def rank_by_total_count(self, kind=types_of_sequences[0]):
        """
            Returns a list of tuples containing the number of occurrences of each
            sequence [words (w), letters (l) or phrases (p)] found in the Text and
            the str form of the sequences.
            
            The list is sorted by number of occurences in decreasing order.
        """
        if kind in Text.types_of_sequences:
            sequences = self.split_text_by_sequence(kind)
            
            occurences = Counter( [str(x) for x in sequences] )
            
            return occurences.most_common()
        
        else:
            logging.error("No such type available cannot rank by occurrences: "
                          + kind)
            logging.error("try: " + str(Text.types_of_sequences))
            sys.exit(0)
    
    def rank_by_number_of_matches(self, sequence_to_match, kind=types_of_sequences[0]):
        """
            Returns a list of tuples containing the number of matches found in
            each sequence [words (w), letters (l) or phrases (p)] of the Text and
            the str form of the sequence.
            
            The list is sorted by number of matches in decreasing order.
        """
        if kind in Text.types_of_sequences:
            sequences = self.split_text_by_sequence(kind)
            set_of_sequences = set(sequences)
            
            ranked_by_matches = []
            
            for sequence in set_of_sequences:
                ranked_by_matches.append( (sequence, sequence.count(sequence_to_match) ) )

            ranked_by_matches.sort(reverse=True, key=lambda x: x[1])
            
            return ranked_by_matches
        
        else:
            logging.error("No such type available cannot rank by matches: " + kind)
            logging.error("try: " + str(Text.types_of_sequences))
            sys.exit(0)

    def find_all_adverbs(self):
        """Finds all the adverbs in the text."""
        words = self.split_text_by_sequence('w')
        adverbs = []
        
        for word in words:
            word_obj = Word(word)
            if word_obj.isAdverb():
                adverbs.append(word)
        
        return adverbs
    
    def __repr__(self):
        return self.__str__()