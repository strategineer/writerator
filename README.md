poet
============
poet is a command line tool that analyzes plain text files containing english language writing and uses the text to randomly generate poetry using Markov Chains.

## Using poet
`poet -f book.txt poem`: generates a poem (a haiku by default) using the words in _book.txt_.

`poet -f book.txt info`: prints the Gunning-Fog Index of _book.txt_ (a readability metric).

`poet -f book.txt count`: counts the number of occurrences of each word in _book.txt_ and displays them in descending order of count.

`poet -f book.txt count -t c`: counts the number of occurrences of each character in _book.txt_ and displays them in descending order of count.

`poet -f book.txt count -e the`: counts the number of occurrences of the word "the" in _book.txt_ and displays the total count.

`poet -f book.txt match e`: counts the number of occurrences of the character "e" in each word in _book.txt_ and displays them in descending order of count.


## Installing poet
Download the source code and run `pip install .` from within the folder containing the source code. This will install poet and its dependencies.

## TODO
- Add code/options for rhyming
- Fail gracefully when nothing is piped into poet
