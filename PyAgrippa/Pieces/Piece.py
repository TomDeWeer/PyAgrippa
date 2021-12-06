from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generator

from PyAgrippa.Evaluation.BoardEvaluator import BoardEvaluator
from PyAgrippa.GUI.GUILayout import IGUILayout
from PyAgrippa.Moves.MoveRepresentation import IMoveRepresentation

if TYPE_CHECKING:
    from PyAgrippa.Boards.Board import IBoard


class IPiece:
    def __init__(self, isWhite: bool):
        self.board = None
        self.white = isWhite

    def __str__(self):
        return f"{'White' if self.isWhite() else 'Black'} {str(self.__class__.__name__)}"

    def isWhite(self):
        return self.white

    def isBlack(self):
        return not self.isWhite()

    def getImage(self, layout: IGUILayout):
        raise NotImplementedError

    def getBoard(self) -> IBoard:
        raise NotImplementedError

    def getSquare(self):
        return self.getBoard().getSquareOf(self)

    def getIdentifier(self) -> Any:
        """
        An identifier to communicate about pieces in a more efficient way (most of the time an integer). If a piece does
        not have an identifier, this just returns the piece itself.
        """
        raise NotImplementedError

    def getAllPseudoLegalMoves(self, moveRepresentation: IMoveRepresentation) -> Generator[Any, None, None]:
        raise NotImplementedError

    def evaluate(self, evaluator: BoardEvaluator):
        raise NotImplementedError

