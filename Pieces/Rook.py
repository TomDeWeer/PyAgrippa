from Pieces.Piece import PieceSCPS
from Pieces.SlidingPiece import ISlidingPiece, SlidingPieceSCPS


class IRook(ISlidingPiece):
    pass


class RookSCPS(SlidingPieceSCPS, IRook):
    def __init__(self, isWhite: bool):
        SlidingPieceSCPS.__init__(self, isWhite=isWhite)
        IRook.__init__(self, isWhite)
