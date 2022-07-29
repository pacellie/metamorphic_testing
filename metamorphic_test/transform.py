from typing import Callable

# The general type of a transformation. Since it can have an arbitrary number
# of arbitrary inputs and an arbitrary output, 'Callable' seems most appropriate.
Transform = Callable
