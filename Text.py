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
import re

from collections import Counter

class Text(object):
    """Represents a human language text."""
    
    #Represents the kind of sequences of characters able to be analyzed
    # w for words, l for letters
    types_of_sequences = ['w', 'l', 'p']

    def __init__(self, filename=None):
        """Initializes a Text."""
        self.text = ""
        
        if filename:
            self.load_from_txt_file(filename)

    def load_from_txt_file(self, filename_in):
        """Loads more text from a plain text file into a Text object."""
        if os.path.isfile(filename_in):
            with io.open(filename_in, 'r') as file:
                lines = file.readlines()
            
            lines = map(lambda line: line.strip(), lines)
            self.text += " ".join(lines)

        else:
            logging.error("No such filename: " + filename_in)
            sys.exit(0)

    def split_text_by_sequence(self, kind=types_of_sequences[0]):
        """
            Splits the text by sequence and returns a list
            
            i.e. "Bill. Is. Cool." => words (w) => ["Bill.", "is.", "cool."]
            "Bill is cool" => letters (l) => ["B", "i", "l", "l", "i", "s", ...]
        """
        if kind in Text.types_of_sequences:
            if kind == 'w':
                split_text = self.text.split(" ")
            
            elif kind == 'p':
                split_text = self.text.split(".")

            elif kind == 'l':
                split_text = list(self.text)
            
            # Clean up sequences. Remove whitespace, remove punctuation
            split_text = map(lambda sequence: sequence.rstrip(".,").strip(), split_text)
            
            # Removes empty string
            split_text = filter(None, split_text)
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

        if kind in Text.types_of_sequences:
            sequences = self.split_text_by_sequence(kind)
            
            occurences = Counter(sequences)
            
            return occurences.most_common()[:number_of_words_to_display]
        
        else:
            logging.error("No such type available cannot rank by occurrences: "
                          + kind)
            logging.error("try: " + str(Text.types_of_sequences))
            sys.exit(0)
    
    def rank_by_number_of_matches(self, sequence_to_match, number_of_words_to_display, kind=types_of_sequences[0]):
        
        if kind in Text.types_of_sequences:
            sequences = self.split_text_by_sequence(kind)
            set_of_sequences = set(sequences)
            
            ranked_by_matches = []
            
            for sequence in set_of_sequences:
                ranked_by_matches.append( ( sequence, sequence.count(sequence_to_match) ) )

            ranked_by_matches.sort(reverse=True, key=lambda x: x[1])
            
            return ranked_by_matches[:number_of_words_to_display]
        
        else:
            logging.error("No such type available cannot rank by matches: " + kind)
            logging.error("try: " + str(Text.types_of_sequences))
            sys.exit(0)
    
    def find_all_adverbs(self):
        """Finds all the adverbs in the text."""
        adverbs = re.findall(r"\w+ly", self.text)
        return adverbs
    
    def __str__(self):
        """Prints out the text"""
        
        output = ""
        
        logging.error("__str__ NOT IMPLEMENTED")
        sys.exit(0)
        
        return output

    
    def __repr__(self):
        return self.__str__()