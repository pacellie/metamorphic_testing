from typing import Callable

Transform = Callable
"""
The general type of a transformation. Since it can have an arbitrary number
of arbitrary inputs and an arbitrary output, 'Callable' seems most appropriate.
"""
