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
import sys
import re
from functools import *

@total_ordering
class Word(object):
    """Represents a Word."""
    
    def __init__(self, word):
        """Initializes a Word."""
        assert isinstance(word, str)
        self.word = word
    
    def countSyllables(self):
        """
            Counts the number of syllables for an English language Word.
            
            ~85% Accuracy apparantly
            COPYRIGHT Greg Fast, Dispenser (python port)

            Better Algorithm: http://pypi.python.org/pypi/PyHyphen/2.0.1
        """
        SubSyl = ('cial','tia','cius','cious','giu','ion','iou','sia$','.ely$',)
        AddSyl = ('ia','riet','dien','iu','io','ii','[aeiouym]bl$','[aeiou]{3}',
                  '^mc','ism$','([^aeiouy])\1l$', '[^l]lien','^coa[dglx].',
                  '[^gq]ua[^auieo]','dnt$',)

        word = self.word.lower()
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
            syl +=1	# 'x'
        
        # count vowel groupings
        syl += len(scrugg)
        
        return (syl or 1)	# got no vowels? ("the", "crwth")
    
    def isAdverb(self):
        """Determines whether word is an adverb."""
        if re.match(r"\w+ly", self.word):
            return True
        else:
            return False
    
    def count(self, string):
        return self.word.count(string)
    
    def __hash__(self):
        return hash(self.word)
    
    def __eq__(self, other):
        if isinstance(other, Word):
            return self.word == other.word
        else:
            return NotImplemented
    
    def __lt__(self, other):
        if isinstance(other, Word):
            return self.word < other.word
        else:
            return NotImplemented
    
    def __str__(self):
        """Returns str form of Word."""
        return self.word

    def __repr__(self):
        return self.__str__()

def main():
    for word in ('honour', 'decode', 'decoded', 'oiseau', 'mathematical',
                 'abe','hippopotamus', 'reincarnation', 'information'):
        word_obj = Word(word)
        print(str(word_obj) + " " + str(word_obj.countSyllables()))


if __name__== "__main__":
    main()