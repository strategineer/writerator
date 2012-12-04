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


class Phrase(BasicText):
    """Represents a Phrase."""
    
    def __init__(self, text):
        """Initializes a Phrase."""
        super( Phrase, self ).__init__(text)


def main():
    test = Phrase("Bill is cool.")
    print(test)

if __name__== "__main__":
    main()