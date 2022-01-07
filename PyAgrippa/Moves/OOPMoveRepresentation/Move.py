from __future__ import annotations
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from PyAgrippa.Boards.Board import IBoard
    from PyAgrippa.Pieces.Piece import IPiece


class IMove:
    """
    Piece and Square Centric.
    """
    def __init__(self, board: IBoard):
        self.board = board

    def __eq__(self, other: IMove):
        raise NotImplementedError

    def toUCI(self) -> str:
        return f"{self.getStartingSquare()}{self.getEndingSquare()}"

    def getBoard(self):
        return self.board

    def apply(self):
        """
        Applies everything BUT castle rights
        :return:
        """
        raise NotImplementedError

    def undo(self):
        """
        Undoes the apply()
        :return:
        """
        raise NotImplementedError

    def applyCastlingRightChanges(self):
        raise NotImplementedError

    def undoCastlingRightChanges(self):
        raise NotImplementedError

    def getCapturedPiece(self) -> Optional[IPiece]:
        return None

    def getPromotedPiece(self) -> Optional[IPiece]:
        return None

    def getMovingPiece(self) -> IPiece:
        raise NotImplementedError

    def isWhiteMove(self):
        return self.getMovingPiece().isWhite()

    def isCastling(self):
        return False

    def isEnPassant(self):
        return False

    def isKingsideCastling(self):
        return False

    def isQueensideCastling(self):
        return False

    def isPureCapturingMove(self):
        return False

    def isNormalMove(self):
        return False

    def getStartingSquare(self):
        raise NotImplementedError

    def getEndingSquare(self):
        raise NotImplementedError

    def isDoublePawnAdvancement(self):
        return False

    def isPromotionCapture(self):
        return False

    def isPromotionAdvance(self):
        return False

    def getPromotionSquare(self):
        raise NotImplementedError




