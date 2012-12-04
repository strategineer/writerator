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
from Word import Word

class Text(object):
    """Represents a human language text."""
    
    #Represents the kind of sequences of characters able to be analyzed
    # w for words, l for letters
    types_of_sequences = ['w', 'l', 'p']
    
    def clean_splitted_text(str_sequences):
        # Clean up sequences. Remove whitespace, remove punctuation
        str_sequences = [x.rstrip(".,").strip() for x in str_sequences]
        # Removes empty string
        str_sequences = filter(None, str_sequences)
        
        return str_sequences
    
    def __init__(self, filename):
        """Initializes a Text."""
        self.load_from_txt_file(filename)

    def load_from_txt_file(self, filename_in):
        """Loads more text from a plain text file into a Text object."""
        if os.path.isfile(filename_in):
            with io.open(filename_in, 'r') as file:
                lines = file.readlines()
            
            lines = map(lambda line: line.strip(), lines)
            self.text = " ".join(lines)

        else:
            logging.error("No such filename: " + filename_in)
            sys.exit(0)

    def split_text_by_sequence(self, kind=types_of_sequences[0]):
        """
            Splits the text by sequence and returns a list
            
            i.e. "Bill. Is. Cool." => words (w) => ["Bill.", "is.", "cool."]
            "Bill is cool" => letters (l) => ["B", "i", "l", "l", "i", "s", ...]
        """
        logging.debug("Entering Text.split_text_by_sequence ...")
        if kind in Text.types_of_sequences:
            kind_class = None
            if kind == 'w':
                split_text = self.text.split(" ")
                
                split_text = Text.clean_splitted_text(split_text)
                for sequence in split_text:
                    split_text = [Word(x) for x in split_text]
            
            elif kind == 'p':
                split_text = self.text.split(".")
                
                split_text = Text.clean_splitted_text(split_text)
                for sequence in split_text:
                    split_text = [Phrase(x) for x in split_text]

            elif kind == 'l':
                split_text = list(self.text)
                
                split_text = Text.clean_splitted_text(split_text)
                for sequence in split_text:
                    split_text = [Letter(x) for x in split_text]

            logging.debug("Exiting Text.split_text_by_sequence ...")
            return split_text
        
        else:
            logging.error("No such type available cannot split: " + kind)
            logging.error("try: " + str(Text.types_of_sequences))
            sys.exit(0)
        
    def rank_by_total_count(self, number_of_words_to_display, kind=types_of_sequences[0]):
        """
            Returns a list containing the words (w), letters (l) or phrases (p)
            within a text ranked by the number of occurences from largest to
            smallest.
        """
        logging.debug("Entering Text.rank_by_total_count ...")
        if kind in Text.types_of_sequences:
            sequences = self.split_text_by_sequence(kind)
            
            occurences = Counter( map(lambda sequence: str(sequence) ,sequences) )
            
            return occurences.most_common()[:number_of_words_to_display]
        
        else:
            logging.error("No such type available cannot rank by occurrences: "
                          + kind)
            logging.error("try: " + str(Text.types_of_sequences))
            sys.exit(0)
    
    def rank_by_number_of_matches(self, sequence_to_match, number_of_words_to_display, kind=types_of_sequences[0]):
        logging.debug("Entering Text.rank_by_number_of_matches ...")
        if kind in Text.types_of_sequences:
            sequences = self.split_text_by_sequence(kind)
            set_of_sequences = set(sequences)
            
            ranked_by_matches = []
            
            for sequence in set_of_sequences:
                ranked_by_matches.append( (sequence, sequence.count(sequence_to_match) ) )

            ranked_by_matches.sort(reverse=True, key=lambda x: x[1])
            
            return ranked_by_matches[:number_of_words_to_display]
        
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
    
    def __str__(self):
        """Returns str form of Text"""
        return self.text

    
    def __repr__(self):
        return self.__str__()