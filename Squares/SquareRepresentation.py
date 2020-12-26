class ISquareRepresentation:
    """
    Internal representation of a chess square.
    """

    def getRank(self):
        """
        Returns an integer between 0 and 7 denoting the rank.
        """
        raise NotImplementedError

    def getFile(self):
        """
        Returns an integer between 0 and 7 denoting the rank.
        """
        raise NotImplementedError

    def onBoard(self):
        raise NotImplementedError


class Square0x88Representation(ISquareRepresentation):
    def __init__(self, index):
        self.index = index

    def getRank(self):
        return self.index >> 4

    def getFile(self):
        return self.index & 7

    def onBoard(self):
        raise NotImplementedError




