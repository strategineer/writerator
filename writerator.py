import logging
import sys
import os

import click

from texttools import Text

ARG_TEXT = "ARG_TEXT"


def get_syllable_pattern(name):
    #Shakespeare Sonnet
    if name == 's':
        return get_repeat_syllable_pattern(10, 14)
    #Haiku
    elif name == 'h':
        return [7, 5, 7]


def get_repeat_syllable_pattern(number_of_syllables, times_to_repeat):
    repeat_pattern = []
    for _ in range(0, times_to_repeat):
        repeat_pattern.append(number_of_syllables)
    return repeat_pattern


def print_ranked_list_output(ranked_elements):
    for (element, count) in ranked_elements:
        if count != 0:
            print(str(count) + ": " + str(element))


class ElementParamType(click.ParamType):
    name = "element"

    def convert(self, value, param, ctx):
        """Expands one letter element type code to full word"""
        if value == 'c':
            return "characters"
        elif value == 'w':
            return "words"
        elif value == 's':
            return "sentences"
        else:
            self.fail(
                "Choices must be 'c' for characters 'w' for words 's' for sentences.",
                param, ctx)


ELEMENT_TYPE = ElementParamType()


@click.group()
@click.option('-f', '--file', type=click.Path(exists=True))
@click.option('-v', '--verbose', is_flag=True, help="Enable verbose logging.")
@click.pass_context
def cli(ctx, file, verbose):
    if ctx.obj is None:
        ctx.obj = {}

    logging_level = logging.DEBUG if verbose else logging.ERROR
    logging.basicConfig(stream=sys.stderr, level=logging_level)

    ctx.obj[ARG_TEXT] = Text(file)


@cli.command(help='Generate randomized poems.')
@click.option(
    "-l",
    "--syllables",
    help=
    """generate a poem by specifying the number of syllables, as a string of space seperated numbers, for each line in the poem."""
)
@click.option("-p",
              "--preset",
              type=click.Choice(['h', 's']),
              help="""generate a poem by specifying a preset.""")
@click.option(
    "-c",
    "--shortcut",
    type=int,
    nargs=2,
    help=
    """generate a poem by specifying the number of syllables per line and the number of lines."""
)
@click.pass_context
def poem(ctx, syllables, preset, shortcut):
    text = ctx.obj[ARG_TEXT]
    if syllables:
        syllables_pattern = [int(s) for s in syllables.split(" ")]
    elif preset:
        syllables_pattern = get_syllable_pattern(preset)
    elif shortcut:
        syllables_pattern = get_repeat_syllable_pattern(shortcut[0],
                                                        shortcut[1])
    else:
        # Default to a Haiku.
        syllables_pattern = get_syllable_pattern('h')

    text.generate_poem(syllables_pattern)


@cli.command(
    help=
    """get general info about the text (just the Gunning-Fog Index for now)""")
@click.pass_context
def info(ctx):
    text = ctx.obj[ARG_TEXT]
    print(str(text.calculate_Gunning_Fog_Index()))


@cli.command(
    help=
    """Count each occurrence, as defined by the -t option, of each element within the text."""
)
@click.option(
    "-e",
    "--element",
    help="""Count the number of times a specific element appears in the text."""
)
@click.option(
    "-t",
    "--type",
    "element_type",
    type=ELEMENT_TYPE,
    default='w',
    help=
    """determine the type of text elements (words, characters, sentences) to analyze"""
)
@click.pass_context
def count(ctx, element, element_type):
    text = ctx.obj[ARG_TEXT]
    if element:
        print(str(text.count_occurrences(element, element_type)))
    else:
        ranked_elements = text.rank_by_total_count(element_type)
        print_ranked_list_output(ranked_elements)


@cli.command(
    help=
    """Count the number of matches of a pattern (sequences of characters separated by '~') within each one of the elements of the text.
    eg. You can count the occurrences of the letter 'e' in each word in the text and all words with at least one occurrence ordered by number of occurrences.
    """
)
@click.argument("patterns")
@click.option(
    "-t",
    "--type",
    "element_type",
    type=ELEMENT_TYPE,
    default='w',
    help=
    """determine the type of text elements (words, characters, sentences) to analyze"""
)
@click.pass_context
def match(ctx, patterns, element_type):
    text = ctx.obj[ARG_TEXT]
    match_separator = "~"
    if match_separator in patterns:
        patterns = patterns.split(match_separator)
    else:
        patterns = [patterns]
    ranked_elements = text.rank_by_number_of_matches(patterns, element_type)
    print_ranked_list_output(ranked_elements)
