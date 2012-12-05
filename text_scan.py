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
    
    parser.add_argument("option",  nargs='+',
                        help="""
                        
                        choose which operation to perform on file_in.
                        type = w or l or p => (words, letters, phrases)
                        
                        option choices:
                        t type number_to_display:
                        ranks each element by the times they occur in the
                        text as a whole.
                        
                        c type element:
                        count the number of times element appears in the
                        text.
                        
                        m type match number_to_display:
                        ranks the elements by the amount of times each
                        MATCH appears in the element.
                        ATTENTION: Seperate matches using ~ 
                        """,
                        )
    operations = ['t', 'c', 'm']
    element_types = ['w', 'l', 'p']
    
    match_seperator = "~"
    
    #Optional arguments
    parser.add_argument("-d", "--debug", help="displays logging debug messages.",
                action="store_true")
    
    parser.add_argument("-o", "--output",
                        help="""writes output to a .txt file""",
                        action="store_true")
    
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
    
    operation_type = str(args.option[0])
    
    
    #CLEAN UP THIS MEGA IF STATEMENT, CUT UP INTO MANY METHODS
    
    
    
    if operation_type in operations:
        if operation_type == 'c':
            assert len(args.option) == 3
            element_type = str(args.option[1])
            
            element_to_count = str(args.option[2])
            
            output_lines.append(text.count_occurences(element_to_count, element_type))
        
        elif (operation_type == 't') or (operation_type == 'm'):
            if operation_type == 't':
                assert len(args.option) == 3
                element_type = str(args.option[1])
                
                number_to_display = int(args.option[2])
                
                ranked_elements = text.rank_by_total_count(element_type)
                
            elif operation_type == 'm':
                assert len(args.option) == 4
                element_type = str(args.option[1])
                
                elements_to_match = str(args.option[2])
                number_to_display = int(args.option[3])
                
                if match_seperator in elements_to_match:
                    elements_to_match = elements_to_match.split(match_seperator)
                else:
                    elements_to_match = [elements_to_match]
                
                ranked_elements = text.rank_by_number_of_matches( elements_to_match , element_type )

            if len(ranked_elements) < number_to_display:
                last_index = len(ranked_elements)
            else:
                last_index = number_to_display
            
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