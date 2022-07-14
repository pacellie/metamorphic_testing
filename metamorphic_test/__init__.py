from .decorator import transformation, relation, metamorphic, randomized, system
from .generator import randint
from .relations import approximately, equality
from .transforms import identity

import logging
import sys

# normally setting up the logging config in the beginning of main function is the best
# idea, but we don't have it, so https://realpython.com/python-logging-source-code/
# indicates that making it at __init__ is the next best option
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
# Add handler to stdout. Strangely just using basicConfig doesn't work
# May want to change the level to something else
# using an .ini config, or to put FileHandlers.
logger.addHandler(handler)

__version__ = '0.1.0'
__all__ = [
    'transformation',
    'relation',
    'metamorphic',
    'system',
    'randomized',
    'randint',
    'approximately',
    'equality',
    'identity',
]
