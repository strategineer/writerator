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
    batch_config = configparser.ConfigParser()
    batch_config.read('config' + os.sep + 'batch.ini')

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

    output_lines = get_output(text, parser, batch_config)

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

    show_parent_parser.add_argument("-s", "--show", metavar="N", type=int,
                                    default=int(config['parser']['NumberToShow']),
                                    help="""choose the number of results to
                                    show (if applicable)""")


    subparsers = main_parser.add_subparsers(help="commands", dest="command")

    batch_parser = subparsers.add_parser("batch",
                                         help="""run many commands, at once,
                                         specified in the batch .ini file.""")
    batch_parser.add_argument("-r", "--run", metavar="NAME",
                              help="""Run the specified batch command grouping.""")

    batch_parser.add_argument("-l", "--list", action="store_true",
                              help="""List the names of the available batch
                              command groupings.""")

    batch_parser.add_argument("-c", "--showcommand", action="store_false",
                              help="""Chooses to either show or not show the
                               commands before their output when running a
                                command grouping. Defaults to show.""")


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
                                          """get general info about the text""")

    info_parser.add_argument("-g", "--general", action="store_true",
                             help="""generate a general info printout about the
                             text.""")

    info_parser.add_argument("-t", "--test", choices=["g"],
                             help="""test the readability of the text using
                             various readability tests. g for Gunning-Fog Index""")

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

def get_output(text, parser, batch_config, args_list=[]):
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

    commands = ['poem', 'count', 'match', 'info', 'batch']

    if args_list:
        args = parser.parse_args(args_list)
    else:
        args = parser.parse_args()

    if args.command == commands[1]:
        if args.count:
            (element_type, element_to_count) = (expand_type(args.type) , args.count)
            return [str(text.count_occurences(element_to_count, element_type))]

        elif args.totalcount:
            (element_type, number_to_display) = (expand_type(args.type), args.show)
            ranked_elements = text.rank_by_total_count(element_type)
            return generate_ranked_list_output(ranked_elements, number_to_display)

    elif args.command == commands[2]:
        (element_type, elements_to_match,
         number_to_display) = (expand_type(args.type), args.patterns , args.show)
        match_seperator = "~"
        if match_seperator in elements_to_match:
            elements_to_match = elements_to_match.split(match_seperator)
        else:
            elements_to_match = [elements_to_match]
        print(element_type)
        ranked_elements = text.rank_by_number_of_matches( elements_to_match , element_type )
        return generate_ranked_list_output(ranked_elements, number_to_display)

    elif args.command == commands[0]:
        if args.syllables:
            (syllables_pattern, number_to_generate) = (args.syllables, args.show)
        elif args.preset:
            (syllables_pattern, number_to_generate) = (get_syllable_pattern(args.preset), args.show)
        elif args.shortcut:
            (syllables_pattern, number_to_generate) = (get_repeat_syllable_pattern(args.shortcut[0], args.shortcut[1]), args.show)
        else:
            logging.error("More args are required.")
            sys.exit(1)
        output_lines = []
        poems = text.generate_poems(syllables_pattern, number_to_generate)
        poem_count = 0
        for poem in poems:
            poem_count += 1
            for line in poem:
                output_lines.append(line)
            if poem_count != len(poems):
                output_lines.append("")
        return output_lines

    elif args.command == commands[3]:
        if args.general:
            logging.error("info -g not implemented")
            sys.exit(1)

        elif args.test == 'g':
            return [str(text.calculate_Gunning_Fog_Index())]

    elif args.command == commands[4]:
        module_name = sys.argv[0]
        if args.run:
            if args.run in batch_config:
                output_lines = []
                batch_args_list = []
                for test_name in batch_config[args.run]:
                    batch_args_list.append(config[args.run][test_name])

                batch_args_count = 0
                for batch_args in batch_args_list:
                    batch_args_count += 1

                    args_string = args.file_in + " " + batch_args

                    args_list = shlex.split(args_string)

                    if "batch" not in args_list:

                        new_output_lines = get_output(text, parser, batch_config, args_list)

                        if args.showcommand:
                            output_lines.append("python " + module_name +  " " + args_string)

                        for line in new_output_lines:
                            output_lines.append(line)

                        if batch_args_count != len(batch_args_list):
                            output_lines.append("")

                    else:
                        logging.error("Cannot run batch commands with batch "
                        + "command groupings.")
                        logging.error("Please remove offending command from batch.ini")
                        sys.exit(1)

                return output_lines

            else:
                logging.error("No such batch grouping : " + args.run )
                sys.exit(1)

        elif args.list:
            output_lines = []
            for command_grouping in batch_config:
                if command_grouping != "DEFAULT":
                    output_lines.append(command_grouping)

            return output_lines

def generate_ranked_list_output(ranked_elements, number_to_display):
    last_index = len(ranked_elements) if len(ranked_elements) < number_to_display else number_to_display
    output_lines = []
    for i in range(0, last_index):
        (element, count) = ranked_elements[i]
        if count != 0:
            output_lines.append(str(count) + ": " + str(element))
    return output_lines

if __name__== "__main__":
        main()
