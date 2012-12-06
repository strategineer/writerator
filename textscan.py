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

import io
import logging
import sys

import argparse
import textwrap
import cProfile
import pstats

from texttools import Text


def main():
    parser = make_parser()
    
    args = parser.parse_args()
    
    set_logging_level(args.debug)
    
    (filename_in, filename_out) = get_filenames(args.file_in)
    
    text = Text(filename_in)
    output_lines = get_output(text, args.option)
    
    if args.output:
        output_to_file(filename_out, output_lines)
    else:
        output_to_console(output_lines)


def make_parser():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent(
                                     """
                                        option choices:
                                        ******************************************************************
                                        p NUMBER_TO_SHOW N1 N2 ...              (poem by pattern)
                                        p NUMBER_TO_SHOW PRESET                 (poem by preset)
                                        p NUMBER_TO_SHOW SYLLABLES x LINES      (poem by shortcut pattern)
                                        
                                        p: generates poems
                                        
                                        NUMBER_TO_SHOW: number of poems to output
                                        N1, N2, ...: number of syllables for each line
                                        
                                        PRESET choices: 'h' for haiku or 's' for Shakespearing Sonnet
                                        
                                        SYLLABLES: number of syllables per line
                                        LINES: number of lines
                                        
                                        ******************************************************************
                                        t TYPE NUMBER_TO_SHOW
                                        
                                        t: counts each element in a text and ranks them 
                                        by total count
                                        TYPE: w for word, c for character, p for phrase
                                        
                                        ******************************************************************
                                        c TYPE ELEMENT
                                        
                                        c: counts the number of times ELEMENT appears in the
                                        text.
                                        TYPE: w for word, c for character, p for phrase
                                        
                                        ******************************************************************
                                        m TYPE PATTERN1~PATTERN2~... NUMBER_TO_SHOW
                                        
                                        m: ranks the elements by the amount of times each
                                        PATTERN appears in the element.
                                        ATTENTION: Separate PATTERNs using ~
                                        NUMBER_TO_SHOW: number of ranked elements to output
                                        
                                        ******************************************************************
                                        r TEST
                                        
                                        r: calculates various readability tests.
                                        TEST choices: g for the Gunning-Fog Index
                                        ******************************************************************
                                        """))
    
    #Required arguments
    parser.add_argument("file_in", help="filename of input file")
    
    parser.add_argument("option",  nargs='+', help="""options detailed above""")
    
    #Optional arguments
    parser.add_argument("-d", "--debug", 
                        help="displays logging debug messages.",
                        action="store_true")
    
    parser.add_argument("-o", "--output",
                        help="""writes output to a .txt file""",
                        action="store_true")
    
    return parser

def set_logging_level(bool_option):
    if bool_option:
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
        
    else:
        logging.basicConfig(stream=sys.stderr, level=logging.ERROR)

def get_filenames(filename_in):
    
    (name, extension) = filename_in.split(".")
    filename_out = name + "_out" + "." + extension
    
    return (filename_in, filename_out)

def get_output(text, options):
    operation_type = options[0]
    operations = ['t', 'c', 'm', 'r', 'p']
    
    if operation_type in operations:
        if operation_type == 'c':
            (element_type, element_to_count) = get_args(operation_type, options)
            
            return get_count_output(text, element_type, element_to_count)
            
        elif operation_type == 'r':
            test = get_args(operation_type, options)
            return get_readability_test_output(text, test)
        
        elif operation_type == 'p':
            (number_to_generate, syllables_pattern) = get_args(operation_type, options)
            
            return get_poem_output(text, syllables_pattern, number_to_generate)
            
        elif (operation_type == 't') or (operation_type == 'm'):
            if operation_type == 't':
                (element_type, number_to_display) = get_args(operation_type,
                                                             options)
                
                return get_totalcount_output(text, element_type, number_to_display)
                
            elif operation_type == 'm':
                (element_type,
                 elements_to_match,
                 number_to_display) = get_args(operation_type, options)
                
                return get_match_output(text, element_type, elements_to_match, 
                                        number_to_display)
        
    else:
        logging.error("No such operation type: " + operation_type)
        sys.exit(0)

def get_args(operation_type, args):
    if operation_type == 'c':
        assert len(args) == 3
        return (args[1], args[2])
    
    elif operation_type == 'p':
        assert len(args) >= 2
        
        def get_repeat_syllable_pattern(number_of_syllables, times_to_repeat):
            assert isinstance(number_of_syllables, int) and isinstance(times_to_repeat, int)
            repeat_pattern = []
            for i in range(0, times_to_repeat):
                repeat_pattern.append(number_of_syllables)
            
            return repeat_pattern
        
        #Multiplicator
        if len(args) == 5 and args[3] == 'x':
            return (args[1], get_repeat_syllable_pattern(int(args[2]), int(args[4])))
        
        #Shakespeare Sonnet
        if args[2] == 's':
            return (args[1], get_repeat_syllable_pattern(10, 14))
        #Haiku
        elif args[2] == 'h':
            return (args[1], [7,5,7])
        
        else:
            return (args[1], args[2:])
    
    elif operation_type == 'r':
        assert len(args) == 2
        return args[1]
    
    elif operation_type == 't':
        assert len(args) == 3
        return (args[1], int(args[2]))
    
    elif operation_type ==  'm':
        assert len(args) == 4
        return (args[1], args[2], int(args[3]))

def get_readability_test_output(text, test):
    if test == 'g':
        return get_Gunning_output(text)
    
def get_totalcount_output(text, element_type, number_to_display):
    ranked_elements = text.rank_by_total_count(element_type)

    return generate_ranked_list_output(ranked_elements, number_to_display)

def get_count_output(text, element_type, element_to_count):
    output = []
    
    output.append(text.count_occurences(element_to_count, element_type))
    return output

def get_match_output(text, element_type, elements_to_match, number_to_display):
    match_seperator = "~"
    
    if match_seperator in elements_to_match:
        elements_to_match = elements_to_match.split(match_seperator)
    else:
        elements_to_match = [elements_to_match]
                
    ranked_elements = text.rank_by_number_of_matches( elements_to_match , element_type )
    
    return generate_ranked_list_output(ranked_elements, number_to_display)

def get_last_index_for_output(ranked_elements, number_to_display):
    if len(ranked_elements) < number_to_display:
        return len(ranked_elements)
    else:
        return number_to_display

def generate_ranked_list_output(rank_list, number_to_show):
    
    last_index = get_last_index_for_output(rank_list, number_to_show)
    
    output_lines = []
    for i in range(0, last_index):
        (element, count) = rank_list[i]
        
        if count != 0:
            output_lines.append(str(count) + ": " + str(element) + "\n")
    
    return output_lines

def get_Gunning_output(text):
    return [text.calculate_Gunning_Fog_Index()]

def get_poem_output(text, syllables_pattern, number_to_generate):
    output_lines = []
    
    poems = text.generate_poems(syllables_pattern, number_to_generate)
    for poem in poems:
        for line in poem:
            output_lines.append(line + "\n")
        
        output_lines.append("\n")
    
    return output_lines


def output_to_console(output_lines):
    for line in output_lines:
        print(line)

def output_to_file(filename, output_lines):
    with io.open(filename, 'w') as file:
        file.writelines(output_lines)

if __name__== "__main__":
        main()
               
#        cProfile.run("main()", "main_stats.prof")
#        
#        p = pstats.Stats('main_stats.prof')
#        p.strip_dirs().sort_stats('time').print_stats(5)