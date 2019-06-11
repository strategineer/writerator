poet
============
poet is a command line tool that analyzes plain text files containing english language writing and uses the text to randomly generate poetry using Markov Chains.

## Using poet
`poet book.txt poem`: generates a poem (a haiku by default) using the words in _book.txt_.

`poet book.txt info`: prints the Gunning-Fog Index of _book.txt_ (a readability metric).

`poet book.txt count`: counts the number of occurrences of each word in _book.txt_ and displays them in descending order of count.

`poet book.txt count -t c`: counts the number of occurrences of each character in _book.txt_ and displays them in descending order of count.

`poet book.txt count -e the`: counts the number of occurrences of the word "the" in _book.txt_ and displays the total count.

`poet book.txt match e`: counts the number of occurrences of the character "e" in each word in _book.txt_ and displays them in descending order of count.


## Installing poet
Download the source code and run `pip install .` from within the folder containing the source code. This will install poet and its dependencies.

## TODO
- Add code/options for rhyming
- Add option for enabling/disabling the cache (datastore.py)
    - Implement a feature to allow piping text input into the CLI instead of using a required parameter (caching must not be used if stdin is the input)
