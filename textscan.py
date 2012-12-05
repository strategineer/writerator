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
import textwrap

import cProfile
import pstats

import texttools

def main():
    #Runs Unit-Tests
    #subprocess.call("python Text_test.py -q")
    
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent(
                                     """
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
                                        """))
    
    #Required arguments
    parser.add_argument("file_in", help="filename of input file")
    
    parser.add_argument("option",  nargs='+',
                        help="""
                        type = w or c or p => (words, characters, phrases)
                        """
                        )
    operations = ['t', 'c', 'm']
    element_types = ['w', 'l', 'p']
    
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
    
    text = texttools.Text(filename_in)
    
    output_lines = []
    operation_type = args.option[0]
    if operation_type in operations:
        if operation_type == 'c':
            (element_type, element_to_count) = get_args(operation_type, args.option)
            
            output_lines = get_count_output(text, element_type, element_to_count)
            
        elif (operation_type == 't') or (operation_type == 'm'):
            if operation_type == 't':
                (element_type, number_to_display) = get_args(operation_type,
                                                             args.option)
                
                output_lines = get_totalcount_output(text, element_type,
                                                     number_to_display)
                
            elif operation_type == 'm':
                (element_type,
                 elements_to_match,
                 number_to_display) = get_args(operation_type, args.option)
                
                output_lines = get_match_output(text, element_type,
                                                elements_to_match,
                                                number_to_display)
        
        else:
            logging.error("No such operation type: " + operation_type)
            sys.exit(0)
    
    if args.output:
        output_to_file(filename_out, output_lines)
    
    else:
        output_to_console(output_lines)


def get_last_index_for_output(ranked_elements, number_to_display):
    if len(ranked_elements) < number_to_display:
        return len(ranked_elements)
    else:
        return number_to_display

def get_totalcount_output(text, element_type, number_to_display):
    ranked_elements = text.rank_by_total_count(element_type)
    
    last_index = get_last_index_for_output(ranked_elements, number_to_display)
    
    output_lines = []
    for i in range(0, last_index):
        (element, count) = ranked_elements[i]
        
        if count != 0:
            output_lines.append(str(count) + ": " + str(element) + "\n")
    
    return output_lines

def get_match_output(text, element_type, elements_to_match, number_to_display):
    match_seperator = "~"
    
    if match_seperator in elements_to_match:
        elements_to_match = elements_to_match.split(match_seperator)
    else:
        elements_to_match = [elements_to_match]
                
    ranked_elements = text.rank_by_number_of_matches( elements_to_match , element_type )
    
    last_index = get_last_index_for_output(ranked_elements, number_to_display)
    
    output_lines = []
    for i in range(0, last_index):
        (element, count) = ranked_elements[i]
        
        if count != 0:
            output_lines.append(str(count) + ": " + str(element) + "\n")
    
    return output_lines

def get_count_output(text, element_type, element_to_count):
    output = []
    
    output.append(text.count_occurences(element_to_count, element_type))
    return output

def output_to_console(output_lines):
    for line in output_lines:
        print(line)

def output_to_file(filename, output_lines):
    with io.open(filename, 'w') as file:
        file.writelines(output_lines)

def get_args(operation_type, args):
    if operation_type == 'c':
        assert len(args) == 3
        return (args[1], args[2])
    
    elif operation_type == 't':
        assert len(args) == 3
        return (args[1], int(args[2]))
    
    elif operation_type ==  'm':
        assert len(args) == 4
        return (args[1], args[2], int(args[3]))


if __name__== "__main__":
    #main()
    
    cProfile.run("main()", "main_stats.prof")
    
    p = pstats.Stats('main_stats.prof')
    p.strip_dirs().sort_stats('time').print_stats(5)