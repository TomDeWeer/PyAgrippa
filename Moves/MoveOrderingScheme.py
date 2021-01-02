from abc import ABC


class IMoveOrderingScheme:
    """
    Should allow for the following ordering schemes:

    - captures
    - hash moves from previous searches
    - PV from left tree
    - ...
    """
    pass


class DefaultMoveOrderingScheme(IMoveOrderingScheme, ABC):
    pass


class CapturesFirstOrderingScheme(IMoveOrderingScheme, ABC):
    pass


