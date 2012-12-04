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


class Letter(BasicText):
    """Represents a Letter."""
    consonants = ["bcdfghjklmnpqrstvxzwy"]
    
    def __init__(self, text):
        """Initializes a Letter."""
        super( Letter, self ).__init__(text)
        
    def isVowel(self):
        """Determines if a Letter is a vowel."""
        return self.text.lower() not in consonants
    
    def isConsonant(self):
        """Determines if a Letter is a consonant."""
        return self.text.lower() in consonants