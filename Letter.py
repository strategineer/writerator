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
from functools import *

@total_ordering
class Letter(object):
    """Represents a letter."""
    consonants = ["bcdfghjklmnpqrstvxzwy"]
    
    def __init__(self, letter):
        """Initializes a Letter."""
        assert isinstance(letter, str)
        self.letter = letter
    
    def isVowel(self):
        """Determines if a Letter is a vowel."""
        return self.letter.lower() not in consonants
    
    def isConsonant(self):
        """Determines if a Letter is a consonant."""
        consonants = ["bcdfghjklmnpqrstvxzwy"]
        return self.letter.lower() in consonants
    
    def count(self, string):
        return self.letter.count(string)
    
    def __hash__(self):
        return hash(repr(self))
    
    def __eq__(self, other):
        if isinstance(other, Letter):
            return self.letter == other.letter
        else:
            return NotImplemented
    
    def __lt__(self, other):
        if isinstance(other, Letter):
            return self.letter < other.letter
        else:
            return NotImplemented

    def __str__(self):
        """Returns str form of Letter."""
        return self.letter

    def __repr__(self):
        return self.__str__()

if __name__== "__main__":
    main()