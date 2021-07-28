"""Main classes."""


class MainClass1:
    """Parent dummy class 1."""

    pass


class MainClass2:
    """Parent dummy class 2."""

    pass


class MainClass3:
    """Parent dummy class 3."""

    pass


class MainClass4:
    """Parent dummy class 4."""

    pass


class MainClass5:
    """Parent dummy class 5."""

    pass


class MainClass6:
    """Parent dummy class 6."""

    pass


class MainClass7:
    """Parent dummy class 7."""

    pass


"""Child classes."""


class ChildClass1(MainClass1, MainClass2, MainClass3):
    """Represent many-to-one."""

    pass


class ChildClass2(MainClass1):
    """Represent one-to-many."""

    pass


class ChildClass3(MainClass1):
    """Represent one-to-many."""

    pass


class ChildClass4(MainClass1):
    """Represent one-to-many."""

    pass


class ChildClass5(MainClass4):
    """Represent one-to-one."""

    pass


class ChildClass6(MainClass5, MainClass6, MainClass7):
    """Represent many-to-many."""

    pass


class ChildClass7(MainClass5, MainClass6, MainClass7):
    """Represent many-to-many."""

    pass


class ChildClass8(MainClass5, MainClass6, MainClass7):
    """Represent many-to-many."""

    pass
