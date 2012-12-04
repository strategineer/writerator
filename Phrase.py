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
class Phrase(object):
    """Represents a Phrase."""

    def __init__(self, phrase):
        """Initializes a Phrase."""
        assert isinstance(phrase, str)
        self.phrase = phrase
    
    def count(self, string):
        return self.phrase.count(string)
    
    def __hash__(self):
        return hash(repr(self))
    
    def __eq__(self, other):
        if isinstance(other, Phrase):
            return self.phrase == other.phrase
        else:
            return NotImplemented
    
    def __lt__(self, other):
        if isinstance(other, Phrase):
            return self.phrase < other.phrase
        else:
            return NotImplemented
        
    def __str__(self):
        """Returns str form of Phrase"""
        return self.phrase

    def __repr__(self):
        return self.__str__()

def main():
    test = Phrase("Bill is cool.")
    print(test)

if __name__== "__main__":
    main()