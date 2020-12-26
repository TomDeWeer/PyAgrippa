from __future__ import annotations
from typing import TYPE_CHECKING

from Squares.SquareRepresentation import ISquareRepresentation, Square0x88Representation
if TYPE_CHECKING:
    from Boards.Board import IBoard, BoardSquareCenteredWithPieceSets
    from Pieces.Piece import PieceSCPS


class ISquare:
    """
    Interface for a square on a chess board (e.g. a4).
    """
    def __init__(self, representation: ISquareRepresentation = Square0x88Representation):
        self.representation = representation

    def getRank(self):
        """
        Returns an integer between 0 and 7 denoting the rank.
        """
        return self.representation.getRank()

    def getFile(self):
        """
        Returns an integer between 0 and 7 denoting the rank.
        """
        return self.representation.getFile()

    def liesOnBoard(self):
        return self.representation.onBoard()

    def isLightSquare(self) -> bool:
        return not self.isDarkSquare()

    def isDarkSquare(self) -> bool:
        return (self.getFile() + self.getRank()) % 2 == 0



class SquareSCPS(ISquare):
    """
    Squares used in SCPS boards.

    Has a link to the board and to the piece that stands on top of this square.
    """
    def __init__(self, board: BoardSquareCenteredWithPieceSets,
                 representation: ISquareRepresentation):
        """
        Used when creating an empty board only!
        """
        self.piece = None  # no pieces yet on the board
        self.board = board
        ISquare.__init__(self, representation=representation)

    def setPiece(self, piece: PieceSCPS):
        assert piece.getSquare() is self
        self.piece = piece

    def getBoard(self):
        return self.board

    def getPiece(self):
        return self.piece





