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


@total_ordering
class BasicText(object):
    """Represents a BasicText used for inheritance."""

    def __init__(self, text):
        """Initializes a BasicText."""
        assert isinstance(text, str)
        self.text = text
    
    def isspace(self):
        """Determines if a BasicText contains only whitespace"""
        return self.text.isspace()
    
    def istitle(self):
        """
            Determines if a BasicText is a Title, i.e. each word
            has first letter capitalized.
        """
        return self.text.istitle()
        
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

class Phrase(BasicText):
    """Represents a Phrase."""
    
    def __init__(self, text):
        """Initializes a Phrase."""
        super( Phrase, self ).__init__(text + ".")
  
class Word(BasicText):
    """Represents a Word."""
    
    def __init__(self, text):
        """Initializes a Word."""
        super( Word, self ).__init__(text)
        
    def countSyllables(self):
        """
            Counts the number of syllables for an English language Word.
            
            ~85% Accuracy apparently, but works on all words. Not only words in
            the dictionnary
            
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

class Character(BasicText):
    """Represents a Character."""
    consonants = "bcdfghjklmnpqrstvwxyz"
    vowels = "aeiou"
    punctuation = ";,.\"'"
    
    def __init__(self, text):
        """Initializes a Character."""
        super( Character, self ).__init__(text)

    def isVowel(self):
        """Determines if a Character is a vowel."""
        return self.text.lower() in Character.vowels
    
    def isConsonant(self):
        """Determines if a Character is a consonant."""
        return self.text.lower() in Character.consonants
    
    def isPunctuation(self):
        """Determines if a Character is punctuation."""
        return self.text in Character.punctuation

class Text(BasicText):
    """Represents a human language text."""
    
    # Represents the kinds of elements contained within texts, namely words (w),
    # characters(c), phrases(p)
    _types_of_elements = ['w', 'c', 'p']
    
    @staticmethod
    def _clean_input_elements(elements, element_type):
        """
            Cleans a list of elements by removing unnecessary punctuation,
            whitespace from each element, removing the empty strings from the
            list and returns the result.
        """
        if element_type == Text._types_of_elements[0]:
            elements = [x.strip("\"!(),. ") for x in elements]
        
        elif element_type == Text._types_of_elements[1]:
            pass
        
        elif element_type == Text._types_of_elements[2]:
            elements = [x.strip() for x in elements]
        
        else:
            logging.error("No such element type, cannot clean elements.")
            sys.exit(0)
        
        elements = list(filter(None, elements))
        
        assert "" not in elements
        return elements
    
    @staticmethod
    def get_text_from_txt_file(filename_in):
        """Rips the text from a plain text file and returns it as a str."""
        if os.path.isfile(filename_in):
            with io.open(filename_in, 'r') as file:
                lines = file.readlines()
            
            lines = [x.strip() for x in lines]
            return " ".join(lines)

        else:
            logging.error("No such filename cannot get text: " + filename_in)
            sys.exit(0)
    
    def __init__(self, filename):
        """Initializes a Text."""
        super( Text, self ).__init__(Text.get_text_from_txt_file(filename))
    
    def generate_poetry(self, number_of_lines, syllables_per_line):
        pass
    
    def generate_haiku(self, number_to_generate):
        unique_words = list(set(self._parse_words()))
        
        haikus = []
        for i in range(0, int(number_to_generate)):
            new_haiku_lines = []
            
            for line_number in range(0, 3):
                if line_number == 0 or line_number == 2:
                    syllables_needed = 7
                elif line_number == 1:
                    syllables_needed = 5
                
                number_of_tries = 0
                is_done = False
                random_words = []
                while not is_done:
                    random_words.append(random.choice(unique_words))
                    
                    syllable_count = sum([word.countSyllables() for word in random_words])
                    if syllable_count == syllables_needed:
                        new_haiku_lines.append(" ".join([str(word) for word in random_words]).capitalize())
                        is_done = True
                    
                    elif syllable_count < syllables_needed:
                        pass
                    
                    elif syllable_count > syllables_needed:
                        random_words = []
                        number_of_tries += 1
                        
            logging.debug("Number of tries:" + str(number_of_tries))
        
            haikus.append(new_haiku_lines)
            
        return haikus
            
        
    def count_words(self):
        """Counts the number of words in a Text."""
        return len(self._parse_words(cast_as_objects=False))
    
    def count_phrases(self):
        """Counts the number of Phrases in a Text."""
        return len(self._parse_phrases(cast_as_objects=False))
    
    def count_characters(self):
        """Counts the number of characters in a Text."""
        return len(self._parse_characters(cast_as_objects=False))
    
    def calculate_Gunning_Fog_Index(self):
        """Calculates and returns the text's Gunning-Fog index."""
        words = self._parse_words()
        complex_words = [word for word in words if word.countSyllables() >= 3 and not word.istitle()]
        
        number_of_words = len(words)
        number_of_complex_words = len(complex_words)
        number_of_sentences = self.count_phrases()
        
        return (0.4) * ( (number_of_words / number_of_sentences) 
                         + 100 * (number_of_complex_words / number_of_words) )


    def make_occurences_Counter(self, element_type):
        """Returns a Counter with the elements decided by kind, either
         words, characters or phrases as keys from within a Text."""
        elements = self._parse_elements(element_type)    
        return Counter( [str(x) for x in elements] )
        
    def count_occurences(self, element_to_count, element_type):
        """Return the total number of times an element appears in a Text."""
        occurences = self.make_occurences_Counter(element_type)
            
        if element_to_count in occurences:
            return occurences[element_to_count]
        else:
            return 0
        
    def rank_by_number_of_matches(self, matches_to_check, element_type):
        """
            Returns a list of tuples containing the number of matches found in
            each element [words (w), characters (c) or phrases (p)] of the Text and
            the str form of the element.
            
            The list is sorted by number of matches in decreasing order.
        """
        assert isinstance(matches_to_check, list)
        
        if element_type in Text._types_of_elements:
            elements = self._parse_elements(element_type)
            set_of_elements = set(elements)
            
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
            logging.error("try: " + str(Text._types_of_elements))
            sys.exit(0)

    def rank_by_total_count(self, element_type):
        """
            Returns a list of tuples containing the number of occurrences of each
            element [words (w), characters (c) or phrases (p)] found in the Text and
            the str form of the elements.
            
            The list is sorted by number of occurences in decreasing order.
        """
        if element_type in Text._types_of_elements:
            occurences = self.make_occurences_Counter(element_type)
            
            return occurences.most_common()
        
        else:
            logging.error("No such type available cannot rank by occurrences: "
                          + element_type)
            logging.error("try: " + str(Text._types_of_elements))
            sys.exit(0)

    def find_all_adverbs(self):
        """Finds all the adverbs in the text."""
        words = self.split_text_by_element(Text._types_of_elements[0])
        adverbs = []
        
        for word in words:
            word_obj = Word(word)
            if word_obj.isAdverb():
                adverbs.append(word)
        
        return adverbs


    def _parse_phrases(self, cast_as_objects=True):
        """Parses a Text and returns a generator containing the phrases as Phrases"""
        phrases = self.text.split(".")
            
        phrases = Text._clean_input_elements(phrases, 'p')
        
        if cast_as_objects:
            return [Phrase(phrase) for phrase in phrases]
        else:
            return phrases
    
    def _parse_words(self, cast_as_objects=True):
        """Parses a Text and returns a generator containing the words as Words"""
        words = self.text.split(" ")
        
        words = Text._clean_input_elements(words, 'w')
        
        if cast_as_objects:
            return [Word(word) for word in words]
        else:
            return words
    
    def _parse_characters(self, cast_as_objects=True):
        """Parses a Text and returns a generator containing the characters as Characters"""
        characters = list(self.text)
        
        characters = Text._clean_input_elements(characters, 'c')
        
        if cast_as_objects:
            return [Character(character) for character in characters]
        else:
            return characters
    
    def _parse_elements(self, element_type):
        """
            Splits the text by element and returns a list
            
            i.e. "Bill. Is. Cool." => Words (w) => ["Bill.", "Is.", "Cool."]
            "Bill. Is. cool." => Characters (c) => ["B", "i", "l", "l", "I", "s", ...]
            "Bill. Is very. cool." => Phrases (p) => ["Bill", "Is very", "Cool"]
        """
        if element_type in Text._types_of_elements:
            if element_type == Text._types_of_elements[0]:
                return self._parse_words()
            
            elif element_type == Text._types_of_elements[2]:
                return self._parse_phrases()

            elif element_type == Text._types_of_elements[1]:
                return self._parse_characters()
        
        else:
            logging.error("No such type available cannot split: " + element_type)
            logging.error("try: " + str(Text._types_of_elements))
            sys.exit(0)


def main():
    for word in ('honour', 'decode', 'decoded', 'oiseau', 'mathematical',
                 'abe','hippopotamus', 'reincarnation', 'information'):
        word_obj = Word(word)
        print(str(word_obj) + " " + str(word_obj.countSyllables()))
    
    for char in list("abcdefghijklmnopqrstuvwxyz"):
        char_obj = Character(char)
        print(str(char_obj))
        if char_obj.isConsonant():
            print(" ... is consonant. ")
        
        elif char_obj.isConsonant():
            print(" ... is consonant. ")
            
        elif char_obj.isConsonant():
            print(" ... is consonant. ")
        print(str(char_obj) + ": isConsonant? " + str(char_obj.isConsonant())
              + " isVowel? " + str(char_obj.isVowel()))


if __name__== "__main__":
    main()