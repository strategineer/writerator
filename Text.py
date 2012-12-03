#!/usr/bin/env python3
#!/usr/bin/env python3

import logging
import os
import io
import sys

from collections import Counter

class Text(object):
    """Represents a human language text."""
    
    #Represents the kind of sequences of characters able to be analyzed
    # w for words, l for letters
    types_of_sequences = ['w', 'l']

    def __init__(self, filename=None):
        """Initializes a Text."""
        self.text = ""
        
        if filename:
            self.load_from_txt_file(filename)
    
    #Loads the text from a .txt file
    def load_from_txt_file(self, filename_in):
        
        if os.path.isfile(filename_in):
            with io.open(filename_in, 'r') as file:
                lines = file.readlines()
            
            self.text = " ".join(lines)

        else:
            logging.error("No such filename: " + filename_in)
            sys.exit(0)

    #Splits the text by sequence and returns a list
    # i.e. "Bill is cool" => words (w) => ["Bill", "is", "cool"]
    # "Bill is cool" => letters (l) => ["B", "i", "l", "l", "i", "s", ...]
    def split_text_by_sequence(self, kind=types_of_sequences[0]):
        
        if kind in Text.types_of_sequences:
            if kind == 'w':
                split_text = self.text.split(" ") 
            elif kind == 'l':
                split_text = list(self.text)
            
            split_text = filter(lambda sequence: sequence.strip(), split_text)
            
            return split_text
        
        else:
            logging.error("No such type available cannot rank: " + kind)
            logging.error("try: " + str(Text.types_of_sequences))
            sys.exit(0)
            
    # Returns a list containing the words (w) or letters (l) within a text ranked
    # by the number of occurences from largest to smallest
    def rank_by_occurences(self, kind=types_of_sequences[0]):
        if kind in Text.types_of_sequences:
            sequences = self.split_text_by_sequence(kind)
            
            occurences = Counter(sequences)
            
            return occurences.most_common()
        
        else:
            logging.error("No such type available cannot rank: " + kind)
            logging.error("try: " + str(Text.types_of_sequences))
            sys.exit(0)


    def __str__(self):
        """Prints out the text"""
        
        output = ""
        
        logging.error("__str__ NOT IMPLEMENTED")
        sys.exit(0)
        
        return output

    
    def __repr__(self):
        return self.__str__()