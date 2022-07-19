import logging
import sys


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
# Add handler to stdout. Strangely just using basicConfig doesn't work
# May want to change the level to something else
# using an .ini config, or to put FileHandlers.
logger.addHandler(handler)
