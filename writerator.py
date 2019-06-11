#!/usr/bin/env python3

import logging
import sys
import os

import click

from texttools import Text

ARG_TEXT = "ARG_TEXT"

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

def generate_ranked_list_output(ranked_elements):
    output_lines = []
    for (element, count) in ranked_elements:
        if count != 0:
            output_lines.append(str(count) + ": " + str(element))
    return output_lines

@click.group()
@click.argument('IN_FILE')
@click.option('-v', '--verbose', is_flag=True, help="Enable verbose logging.")
@click.pass_context
def cli(ctx, in_file, verbose):
    if ctx.obj is None:
        ctx.obj = {}

    logging_level = logging.DEBUG if verbose else logging.ERROR
    logging.basicConfig(stream=sys.stderr, level=logging_level)

    ctx.obj[ARG_TEXT] = Text(in_file)

@cli.command(help='Generate randomized poems.')
@click.option("-l", "--syllables", help="""generate a poem by specifying the number of syllables, as a string of space seperated numbers, for each line in the poem.""")
@click.option("-p", "--preset", type=click.Choice(['h', 's']), help="""generate a poem by specifying a preset.""")
@click.option("-c", "--shortcut", type=int, nargs=2, help="""generate a poem by specifying the number of syllables per line and the number of lines.""")
@click.pass_context
def poem(ctx, syllables, preset, shortcut):
    text = ctx.obj[ARG_TEXT]
    if syllables:
        syllables_pattern = [int(s) for s in syllables.split(" ")]
    elif preset:
        syllables_pattern = get_syllable_pattern(preset)
    elif shortcut:
        syllables_pattern = get_repeat_syllable_pattern(shortcut[0], shortcut[1])
    else:
        # Default to a Haiku.
        syllables_pattern = get_syllable_pattern('h')

    for l in text.generate_poem(syllables_pattern):
        print(l)

@cli.command(help="""get general info about the text (just the Gunning-Fog Index for now)""")
@click.pass_context
def info(ctx):
    text = ctx.obj[ARG_TEXT]
    print(str(text.calculate_Gunning_Fog_Index()))

@cli.command(help="""Count each occurrence, as defined by the -t option, of each element within the text.""")
@click.option("-c", "--count", help="""Count the number of times a specific element appears in the text.""")
@click.option("-t", "--type", "sequence_type", type=click.Choice(['w', 'c', 's']), default='w',
              help="""determine the type of text elements (words, characters, sentences) to analyze""" )
@click.pass_context
def count(ctx, count, sequence_type):
    text = ctx.obj[ARG_TEXT]
    ls = []
    if count:
        (element_type, element_to_count) = (expand_type(sequence_type) , count)
        ls = [str(text.count_occurences(element_to_count, element_type))]
    else:
        element_type = expand_type(sequence_type)
        ranked_elements = text.rank_by_total_count(element_type)
        ls = generate_ranked_list_output(ranked_elements)

    for l in ls:
        print(l)

@cli.command(help="""count the number of matches of a pattern (sequences of characters seperated by '~') within each one of the elements of the text""")
@click.argument("patterns")
@click.option("-t", "--type", "sequence_type", type=click.Choice(['w', 'c', 's']), default='w',
              help="""determine the type of text elements (words, characters, sentences) to analyze""" )
@click.pass_context
def match(ctx, patterns, sequence_type):
    text = ctx.obj[ARG_TEXT]
    (element_type, elements_to_match) = (expand_type(sequence_type), patterns)
    match_seperator = "~"
    if match_seperator in elements_to_match:
        elements_to_match = elements_to_match.split(match_seperator)
    else:
        elements_to_match = [elements_to_match]
    ranked_elements = text.rank_by_number_of_matches( elements_to_match , element_type )
    for l in generate_ranked_list_output(ranked_elements):
        print(l)
