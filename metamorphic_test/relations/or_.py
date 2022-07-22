from metamorphic_test.rel import Relation, A

def or_(rel1: Relation, rel2: Relation) -> Relation:
    """A relation which checks whether at least one of its subrelations is true."""
    def or_impl(x: A, y: A) -> bool:
        return rel1(x, y) or rel2(x, y)
    or_impl.__name__ = f'{rel1.__name__} or {rel2.__name__}'
    return or_impl
