from Squares.SquareRepresentation import Square0x88Representation


class ISquareRepresentor:
    """
    Internal representation of a chess square.
    """

    @classmethod
    def generateViaRankAndFile(cls, rank, file):
        raise NotImplementedError


class Square0x88Representor(ISquareRepresentor):
    """
    An integer represents the position of a square using a 'ghost board'.

    See http://mediocrechess.blogspot.com/2006/12/0x88-representation.html).
    """

    @classmethod
    def generateViaRankAndFile(cls, rank, file):
        index = 16 * rank + file
        return Square0x88Representation(index)
