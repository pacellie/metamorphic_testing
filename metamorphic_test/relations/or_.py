from metamorphic_test.rel import Relation, A


def or_(rel1: Relation, rel2: Relation) -> Relation:
    """
    Construct a new relation which checks if at least one of the given
    relations holds.

    Parameters:
    -----------
    rel1 : Relation
        The first relation to consider.
    rel2 : Relation
        The second relation to consider.

    Returns
    -------
    out : Relation
        A new relation checking semantically 'rel1 or rel2'.

    Examples:
    ---------
    is_less_than_or_equal = or_(equality, is_less_than)
    """
    def or_impl(x: A, y: A) -> bool:
        return rel1(x, y) or rel2(x, y)
    or_impl.__name__ = f'{rel1.__name__} or {rel2.__name__}'
    return or_impl
