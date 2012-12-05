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

import argparse
import logging
import sys
import subprocess
import io

import cProfile
import pstats

from Text import Text

def main():
    #Runs Unit-Tests
    #subprocess.call("python Text_test.py -q")
    
    parser = argparse.ArgumentParser(description="""scans through text files
                                     containing text written in human languages
                                     and computes information such as the most
                                     common words used, the Gunning-Fog Index,
                                     the word count and more.""")
    
    #Required arguments
    parser.add_argument("file_in", help="filename of input file")
        
    parser.add_argument("type",
                       help="""chooses the element of characters to analyze.
                       Either: w for words, l for letters and p for phrases.""",
                       choices=['w', 'l', 'p'])
    
    parser.add_argument("number_to_display", type=int,
                        help="""chooses the number of elements to display."""
                        )
    
    
    #Optional arguments
    parser.add_argument("-d", "--debug", help="displays logging debug messages.",
                action="store_true")
    
    parser.add_argument("-o", "--output",
                        help="""writes output to a .txt file""",
                        action="store_true")
    
    group = parser.add_mutually_exclusive_group()
    
    group.add_argument("-t", "--totalcount",
                   help="""ranks each element by the times they occur in the
                   text as a whole.""", action="store_true")
    
    group.add_argument("-c", "--count", type=str, metavar="ELEMENT",
                       help="""count the number of times ELEMENT appears in the
                       text.""")
        
    group.add_argument("-m", "--matches", type=str, metavar="\"MATCH~MATCH~...\"",
                       help="""ranks the elements by the amount of times each
                       MATCH appears in the element. ATTENTION: Seperate matches
                       using ~ """)
    
    match_seperator = "~"
    
    args = parser.parse_args()
    
    
    
    #Set logging level
    if args.debug:
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stderr, level=logging.ERROR)
    
    
    filename_in = args.file_in
    
    (name, extension) = filename_in.split(".")
    filename_out = name + "_out" + "." + extension
    
    text = Text(filename_in)
    
    output_lines = []
    if args.count:
        output_lines.append(text.count_occurences(args.count, args.type))
        
    elif args.totalcount or args.matches:
        if args.totalcount:
            ranked_elements = text.rank_by_total_count(args.type)
        
        elif args.matches:
            if match_seperator in args.matches:
                args.matches = args.matches.split(match_seperator)
            else:
                args.matches = [args.matches]
            
            ranked_elements = text.rank_by_number_of_matches(args.matches, args.type)
        
        if len(ranked_elements) < args.number_to_display:
            last_index = len(ranked_elements)
        else:
            last_index = args.number_to_display
        
        for i in range(0, last_index):
            (element, count) = ranked_elements[i]
            
            if count != 0:
                output_lines.append(str(count) + ": " + str(element) + "\n")
    
    if args.output:
        with io.open(filename_out, 'w') as file:
            file.writelines(output_lines)
    else:
        for line in output_lines:
            print(line)



if __name__== "__main__":
    #main()
    
    cProfile.run("main()", "main_stats.prof")
    
    p = pstats.Stats('main_stats.prof')
    p.strip_dirs().sort_stats('time').print_stats(5)