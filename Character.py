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

from BasicText import BasicText


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

def main():
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
              + " isVowel? " + str(letter_obj.isVowel()))


if __name__== "__main__":
    main()