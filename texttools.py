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
import sys
from functools import *

import re
import os
import io
import random
from collections import Counter

from datastore import DataStore

@total_ordering
class BasicText(object):
    """Represents a BasicText used for inheritance."""

    def __init__(self, text):
        """Initializes a BasicText."""
        assert isinstance(text, str)
        self.text = text
#    
#    def isspace(self):
#        """Determines if a BasicText contains only whitespace"""
#        return self.text.isspace()
#    
#    def istitle(self):
#        """
#            Determines if a BasicText is a Title, i.e. each word
#            has first letter capitalized.
#        """
#        return self.text.istitle()
        
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
        super( Sentence, self ).__init__(text.strip(" .") + ".")
  
class Word(BasicText):
    """Represents a Word."""
    
    def __init__(self, text):
        """Initializes a Word."""
        super( Word, self ).__init__(text.strip(""" ,.?!;:\"\'"""))
        
    def countSyllables(self):
        """
            Counts the number of syllables for an English language Word.
            
            ~85% Accuracy apparently, but works on all words. Not only words in
            the dictionary
            
            COPYRIGHT Greg Fast, Dispenser (python port)

            Better Algorithm: http://pypi.python.org/pypi/PyHyphen/2.0.1
        """
        SubSyl = ('cial','tia','cius','cious','giu','ion','iou','sia$','.ely$',)
        AddSyl = ('ia','riet','dien','iu','io','ii','[aeiouym]bl$','[aeiou]{3}',
                  '^mc','ism$','([^aeiouy])\1l$', '[^l]lien','^coa[dglx].',
                  '[^gq]ua[^auieo]','dnt$',)

        word = self.text.lower()
        word = word.replace('\'', '')
        word = re.sub(r'e$', '', word);
        
        scrugg = re.split(r'[^aeiouy]+', word);
        for i in scrugg:
            if not i:
                scrugg.remove(i)
        
        syl = 0;
        for syll in SubSyl:
            if re.search(syll, word):
                syl -= 1
        
        for syll in AddSyl:
            if re.search(syll, word):
                syl += 1
                
        if len(word)==1:
            syl +=1    # 'x'
        
        # count vowel groupings
        syl += len(scrugg)
        
        return (syl or 1)    # got no vowels? ("the", "crwth")
    
    def isAdverb(self):
        """Determines whether word is an adverb."""
        if re.match(r"\w+ly", self.text):
            return True
        else:
            return False

class Text(BasicText):
    """Represents a human language text."""
    
    _element_types = ['characters', 'words', 'sentences']
    
    def __init__(self, filename):
        """Initializes a Text."""
        assert filename
        self.filename = filename
        super( Text, self ).__init__(self.get_text_from_txt_file())
        
        if DataStore.is_to_be_computed(filename):
            database = DataStore(filename, self.__compute_ds_keys_values())
        
        else:
            database = DataStore(filename)
        
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
            sys.exit(0)

    def __compute_ds_keys_values(self):
        """
            Computes process intensive data as key-value pairs and returns a
            list containing each.
        """        
        data_tuples = []
        
        words = self._split_by_element_type(Text._element_types[1])
        words_tpl = (Text._element_types[1], words)
        data_tuples.append(words_tpl)
        
        words_set_tpl = (Text._element_types[1] + "_set", set(words))
        data_tuples.append(words_set_tpl)
        
        sentences = self._split_by_element_type(Text._element_types[2])
        sentences_tpl = (Text._element_types[2], sentences)
        data_tuples.append(sentences_tpl)
        
        sentences_set_tpl = (Text._element_types[2] + "_set", set(sentences))
        data_tuples.append(sentences_set_tpl)
        
        characters = self._split_by_element_type(Text._element_types[0])
        characters_tpl = (Text._element_types[0], characters)
        data_tuples.append(characters_tpl)
        
        characters_set_tpl = (Text._element_types[0] + "_set", set(characters))
        data_tuples.append(characters_set_tpl)
        
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

    def generate_poems(self, syllables_per_line, number_to_generate):
        """Generate poems using the words contained within the Text"""
        def generate_poem_line(set_of_words, syllables_needed):
            random_words = []
            while True:
                random_words.append(random.choice(set_of_words))
                
                syllable_count = sum([word.countSyllables() for word in random_words])
                if syllable_count == syllables_needed:
                    new_line = " ".join([str(word) for word in random_words]).capitalize()
                    return new_line
                
                elif syllable_count < syllables_needed:
                    pass
                
                elif syllable_count > syllables_needed:
                    random_words = []
        
        unique_words = list(self.ds.get_data_from_db(Text._element_types[1] + "_set"))
        
        poems = []
        for i in range(0, int(number_to_generate)):
            poem_lines = []
            
            for syllables_needed in syllables_per_line:                    
                poem_line = generate_poem_line(unique_words, int(syllables_needed))
                    
                poem_lines.append(poem_line)
        
            poems.append(poem_lines)
            
        return poems
    
    def calculate_Gunning_Fog_Index(self):
        """Calculates and returns the text's Gunning-Fog index."""
        words = self.ds.get_data_from_db(Text._element_types[1])
        complex_words = [word for word in words if word.countSyllables() >= 3 and not word.istitle()]
        
        number_of_words = len(words)
        number_of_complex_words = len(complex_words)
        number_of_sentences = len(self.ds.get_data_from_db(Text._element_types[2]))
        
        return (0.4) * ( (number_of_words / number_of_sentences) 
                         + 100 * (number_of_complex_words / number_of_words) )

    def _make_occurences_Counter(self, element_type):
        """Returns a Counter with the elements decided by kind, either
         words, characters or sentences as keys from within a Text."""
        elements = self.ds.get_data_from_db(element_type)    
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
            elements = self.ds.get_data_from_db(element_type)
            set_of_elements = self.ds.get_data_from_db(element_type + "_set")
            
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
            sys.exit(0)

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
            sys.exit(0)

    def find_all_adverbs(self):
        """Finds all the adverbs in the text."""
        words = self.ds.get_data_from_db(Text._element_types[1])
        adverbs = []
        
        for word in words:
            if word.isAdverb():
                adverbs.append(word)
        
        return adverbs

def main():
    for word in ('honour', 'decode', 'decoded', 'oiseau', 'mathematical',
                 'abe','hippopotamus', 'reincarnation', 'information'):
        word_obj = Word(word)
        print(str(word_obj) + " " + str(word_obj.countSyllables()))


if __name__== "__main__":
    main()