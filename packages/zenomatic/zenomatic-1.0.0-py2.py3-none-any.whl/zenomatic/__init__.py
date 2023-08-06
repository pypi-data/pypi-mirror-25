"""Module Initialization.

Start colorama library and puts quotes on namespace.
"""
from colorama import init
from zenomatic.quotes import get_quote, get_quotes, get_random_quote

init()

__version__ = "1.0.0"
