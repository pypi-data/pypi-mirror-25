"""Zen-O-Matic.

Get the Zen of Python on your applications.

Usage:
zeonmatic all
zeonmatic random
zeonmatic seed <number>

Options:
--help      	Show this help
<number>    	Show zen from seed number (0-18)
"""
import sys
from . import __version__
from docopt import docopt
from .quotes import get_quote, get_random_quote, get_quotes
from .utils import console


def start():
    """Function: start.

    Summary: Run selected command and shows data from
    Quotes API or docopt help

    Returns
    -------
        Integer: exit code for command line
    """
    arguments = docopt(
        __doc__,
        version="Zen-O-Matic v. {}".format(__version__))

    if arguments['seed']:
        ret, msg = get_quote(arguments['<number>'])

    if arguments['random']:
        ret, msg = get_random_quote()

    if arguments['all']:
        ret, msg = get_quotes()

    if msg is not None:
        console(msg, format_type='error' if not ret else "quote")

    sys.exit(not ret)


if __name__ == "__main__":
    start()
