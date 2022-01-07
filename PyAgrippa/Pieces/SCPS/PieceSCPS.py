from __future__ import annotations
from typing import Any, TYPE_CHECKING

from PyAgrippa.Moves.MoveRepresentation import IMoveRepresentation
from PyAgrippa.Pieces.Piece import IPiece

if TYPE_CHECKING:
    from PyAgrippa.Boards.SCPSBoard import BoardSCPS
    from PyAgrippa.Squares.Square import SquareSCPS


class PieceSCPS(IPiece):
    """
    Pieces for usage with a Square Centered board representation using Piece Sets.

    Pieces with this board representation have a position.
    """

    def __init__(self, isWhite: bool, identifier: int):
        IPiece.__init__(self, isWhite=isWhite)
        self.square = None  # it's not on any square
        self.identifier = identifier

    def moveTo(self, square: SquareSCPS):
        self.square.empty()  # empty the old square
        self.square = square  # set the new square
        square.setPiece(self)

    def put(self, square: SquareSCPS):
        assert square.getPiece() is None
        self.square = square
        square.setPiece(self)

    def remove(self):
        self.square.empty()
        self.square = None

    def getSquare(self) -> SquareSCPS:
        return self.square

    def getIdentifier(self) -> Any:
        return self.identifier

    def getBoard(self) -> BoardSCPS:
        return self.square.getBoard() if self.square is not None else None

    def applyCastlingRightChangesDueToMove(self):
        """
        Apply changes to the castling rights that happen when the piece moves.
        :return:
        """
        raise NotImplementedError

    def castlingRightsChangeDueToMove(self):
        raise NotImplementedError

    def applyCastlingRightChangesDueToCapture(self):
        """
        Apply changes to the castling rights when this piece gets captured.
        :return:
        """
        raise NotImplementedError



