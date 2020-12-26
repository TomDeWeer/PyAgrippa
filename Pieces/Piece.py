from __future__ import annotations
from typing import TYPE_CHECKING



if TYPE_CHECKING:
    from Boards.Board import IBoard
    from Squares.Square import SquareSCPS


class IPiece:
    def __init__(self, isWhite: bool):
        self.board = None
        self.white = isWhite

    def isWhite(self):
        return self.white

    def isBlack(self):
        return not self.isWhite()


class PieceSCPS(IPiece):
    """
    Pieces for usage with a Square Centered board representation using Piece Sets.

    Pieces with this board representation have a position.
    """

    def __init__(self, isWhite: bool):
        IPiece.__init__(self, isWhite=isWhite)
        self.square = None  # it's not on any square

    def moveTo(self, square: SquareSCPS):
        self.square = square
        square.setPiece(self)

    def getSquare(self):
        return self.square

    def getBoard(self):
        return self.square.getBoard() if self.square is not None else None






