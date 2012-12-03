#!/usr/bin/env python3

import argparse
import logging
import sys
import subprocess

from Text import Text

def main():
    #Runs Unit-Tests
    subprocess.call("python Text_test.py -q")
    
    parser = argparse.ArgumentParser(description="""scans through text files
                                     containing text written in human languages
                                     and computes information such as the most
                                     common words used, the Gunning-Fog Index,
                                     the word count and more. text-scanner""")
    
    #Required arguments
    parser.add_argument("file_in", help="filename of input file")
        
    parser.add_argument("type",
                       help="""chooses the sequence of characters to analyze.
                       Either: w for words, l for letters""",
                       choices=['w', 'l'])
    
    #Optional arguments
    
    parser.add_argument("-d", "--debug", help="displays logging debug messages",
                action="store_true")
    
    parser.add_argument("-r", "--rank", type=int, metavar="NUMBER",
                   help="""counts the total occurences of each word and ranks
                   them""")
        
    args = parser.parse_args()
    
    
    
    #Set logging level
    if args.debug:
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    else:
        logging.basicConfig(stream=sys.stderr, level=logging.ERROR)
    
    
    filename_in = args.file_in
    
    
    text = Text(filename_in)
    
    if args.rank:
        ranked_words = text.rank_by_occurences(args.type)

        for i in range(0, args.rank):
            print(ranked_words[i])
            print("\n")

if __name__== "__main__":
    main()