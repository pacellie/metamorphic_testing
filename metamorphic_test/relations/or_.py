def or_(rel1, rel2):
    """A relation which checks whether at least one of its subrelations is true."""
    def or_impl(x, y):
        return rel1(x, y) or rel2(x, y)
    or_impl.__name__ = f'{rel1.__name__} or {rel2.__name__}'
    return or_impl
