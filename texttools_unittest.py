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

import unittest

from texttools import Sentence, Word


class TestTextTools(unittest.TestCase):

    def setUp(self):
        self.word = Word("")
        self.sentence = Sentence("")
        
        
    def tearDown(self):
        del self.word
        del self.sentence

    def test_init(self):
        self.word =  Word("Bill .,")
        self.sentence = Sentence(" Bill is cool. ")
        self.assertEqual(self.word.text, "Bill")
        self.assertEqual(self.sentence.text, "Bill is cool.")
        
    def test_Word_count_syllables(self):
        self.word.text = "Bill"
        
        self.assertTrue(self.word.countSyllables() == 1)
        self.assertTrue(self.word.count("B") == 1)
        self.assertTrue(self.word.count("i") == 1)
        self.assertTrue(self.word.count("l") == 2)
        self.assertTrue(self.word.count("ll") == 1)
        
    def test_Word_istitle(self):
        self.word.text = "Bob"
        self.assertTrue(self.word.istitle())
        
        self.word.text = "appple"
        self.assertFalse(self.word.istitle())
        
if __name__ == '__main__':
    unittest.main()