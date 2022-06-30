import functools

import hypothesis.strategies as st

floats_without_weird = functools.partial(st.floats, allow_nan=False, allow_infinity=False)