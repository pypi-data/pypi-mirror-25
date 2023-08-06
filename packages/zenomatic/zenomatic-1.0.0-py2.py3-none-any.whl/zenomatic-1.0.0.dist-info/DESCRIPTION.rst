===========
Zen-O-Matic
===========

Shows the Zen of Python in your Applications


:Author: Chris Maillefaud
:Version: 1.0.0
:Python Version: 2.7 and 3.6
:Date: October, 16, 2017

Install and Use
---------------
Install with pip: `pip install zenomatic`

Use

1. Run from command line:

Options:
random: show a random quote
seed <number>: show numbererd quote 
all: show all quotes

Example: `zenomatic random`

2. Run inside application:

`from zenomatic import get_quote()`


`ret, quote = get_quote(1)`

`if ret:`
    `print(quote)`

Avaliable commands
------------------
`get_quote(number)`
Get specific quote from 0 to 18

`get_quotes()`
Get all quotes 

`get_random_quote()`
Get a random quote

