#!/usr/bin/env python3

import logging
import sys
import os
import shlex
import argparse
import configparser

from texttools import Text

def main():
    settings_config = configparser.ConfigParser()
    settings_config.read('config' + os.sep + 'settings.ini')

    parser = make_parser(settings_config)

    args = parser.parse_args()

    set_logging_level(args.debug)

    logging.debug(str(args))

    if(args.infile.name == "<stdin>" ):
        inFilename=settings_config['folders']['InputFolder'] + os.sep + 'stdin.txt'
        with args.infile as f, open(inFilename, 'w') as w:
            for line in f:
                w.write(line);
    else:
        inFilename=args.infile.name

    text = Text(inFilename)

    output_lines = get_output(text, parser)

    with args.outfile as file:
        file.writelines([line + "\n" for line in output_lines])

def make_parser(config):
    main_parser = argparse.ArgumentParser()


    main_parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin)
    main_parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
                        default=sys.stdout)

    main_parser.add_argument("-d", "--debug",
                        help="displays logging debug messages.",
                        action="store_true")

    type_parent_parser = argparse.ArgumentParser(add_help=False)

    type_parent_parser.add_argument("-t", "--type", choices=['w', 'c', 's'],
                                    default=config['parser']['TypeOfElement'], type=str,
                                    help="""determine the type of text elements
                                    (words, characters, sentences) to analyze""" )

    show_parent_parser = argparse.ArgumentParser(add_help=False)

    subparsers = main_parser.add_subparsers(help="commands", dest="command")

    count_parser = subparsers.add_parser("count", help=
                                           """count occurrences of elements
                                           within the text""",
                                           parents=[type_parent_parser, show_parent_parser])

    count_parser.add_argument("-o", "--totalcount", action="store_true",
                              help="""count each element in a text and rank them
                                        by total count""")

    count_parser.add_argument("-c", "--count", metavar="ELEMENT", type=str,
                              help="""count the number of times ELEMENT appears
                              in the text.""")

    info_parser = subparsers.add_parser("info", help=
                                          """get general info about the text (just the Gunning-Fog Index for now)""")

    match_parser = subparsers.add_parser("match", help=
                                           """count the number of matches of a
                                           pattern within each one of the
                                           elements of the text""",
                                           parents=[type_parent_parser,
                                                     show_parent_parser])

    match_parser.add_argument("patterns", metavar="PATTERN1~PATTERN2~...",
                              type=str,
                              help="""patterns, separated by ~, to match within
                              the elements.""")


    poem_parser = subparsers.add_parser("poem", help=
                                              """generate randomized poems""",
                                              parents=[show_parent_parser])

    poem_group = poem_parser.add_mutually_exclusive_group()

    poem_group.add_argument("-l", "--syllables", nargs='+', metavar="N",
                            type=int,
                            help="""generate a poem by specifying the number of
                            syllables for each line in the poem.""")

    poem_group.add_argument("-p", "--preset", metavar="PRESET",
                            choices=['h', 's'],
                            help="""generate a poem by specifying a preset.""")

    poem_group.add_argument("-c", "--shortcut", metavar="N", type=int, nargs=2,
                            help="""generate a poem by specifying the number of
                            syllables per line and the number of lines.""")

    return main_parser

def set_logging_level(bool_option):
    if bool_option:
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    else:
        logging.basicConfig(stream=sys.stderr, level=logging.ERROR)

def get_output(text, parser):
    def expand_type(code):
        """Expands one letter element type code to full word"""
        if code == 'c':
            return "characters"
        elif code == 'w':
            return "words"
        elif code == 's':
            return "sentences"

        else:
            logging.error("No such element type cannot expand: " + code)
            sys.exit(1)

    def get_syllable_pattern(name):
        #Shakespeare Sonnet
        if name == 's':
            return get_repeat_syllable_pattern(10, 14)
        #Haiku
        elif name == 'h':
            return [7,5,7]

    def get_repeat_syllable_pattern(number_of_syllables, times_to_repeat):
        repeat_pattern = []
        for _ in range(0, times_to_repeat):
            repeat_pattern.append(number_of_syllables)

        return repeat_pattern

    commands = ['poem', 'count', 'match', 'info']

    args = parser.parse_args()

    if args.command == commands[1]:
        if args.count:
            (element_type, element_to_count) = (expand_type(args.type) , args.count)
            return [str(text.count_occurences(element_to_count, element_type))]

        elif args.totalcount:
            element_type = expand_type(args.type)
            ranked_elements = text.rank_by_total_count(element_type)
            return generate_ranked_list_output(ranked_elements)

    elif args.command == commands[2]:
        (element_type, elements_to_match) = (expand_type(args.type), args.patterns)
        match_seperator = "~"
        if match_seperator in elements_to_match:
            elements_to_match = elements_to_match.split(match_seperator)
        else:
            elements_to_match = [elements_to_match]
        print(element_type)
        ranked_elements = text.rank_by_number_of_matches( elements_to_match , element_type )
        return generate_ranked_list_output(ranked_elements)

    elif args.command == commands[0]:
        if args.syllables:
            syllables_pattern = args.syllables
        elif args.preset:
            syllables_pattern = get_syllable_pattern(args.preset)
        elif args.shortcut:
            syllables_pattern = get_repeat_syllable_pattern(args.shortcut[0], args.shortcut[1])

        output_lines = []
        poem = text.generate_poem(syllables_pattern)
        for line in poem:
            output_lines.append(line)
        return output_lines

    elif args.command == commands[3]:
        return [str(text.calculate_Gunning_Fog_Index())]

def generate_ranked_list_output(ranked_elements):
    output_lines = []
    for (element, count) in ranked_elements:
        if count != 0:
            output_lines.append(str(count) + ": " + str(element))
    return output_lines

if __name__== "__main__":
        main()
