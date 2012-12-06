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