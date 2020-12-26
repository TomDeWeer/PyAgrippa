from Pieces.Piece import PieceSCPS
from Pieces.SlidingPiece import ISlidingPiece, SlidingPieceSCPS


class IQueen(ISlidingPiece):
    pass


class QueenSCPS(SlidingPieceSCPS, IQueen):
    def __init__(self, isWhite: bool):
        SlidingPieceSCPS.__init__(self, isWhite=isWhite)
        IQueen.__init__(self, isWhite)
