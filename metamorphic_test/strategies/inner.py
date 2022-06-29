import hypothesis.strategies as st


def inner(
    *args: st.SearchStrategy,
    **kwargs: st.SearchStrategy
) -> st.SearchStrategy:
    """
    Use this strategy to pass parameters to the inner transformation.
    Example:
    @given(inner=inner(st.floats(), a=st.integers()))
    @transform(OuterTransform()(InnerTransform()))
    ...

    will pass a positional float and an integer keyword-parameter "a"
    to the InnerTransform instead of the outer one.
    """
    def build_inner_dict(*args, **kwargs):
        return dict(
            args=args,
            kwargs=kwargs
        )
    return st.builds(build_inner_dict, *args, **kwargs)
