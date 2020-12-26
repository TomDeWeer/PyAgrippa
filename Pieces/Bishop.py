from Pieces.Piece import PieceSCPS
from Pieces.SlidingPiece import ISlidingPiece, SlidingPieceSCPS


class IBishop(ISlidingPiece):
    pass


class BishopSCPS(SlidingPieceSCPS, IBishop):
    def __init__(self, isWhite: bool):
        SlidingPieceSCPS.__init__(self, isWhite=isWhite)
        IBishop.__init__(self, isWhite)
