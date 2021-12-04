from __future__ import annotations
from typing import TYPE_CHECKING
from Boards.Board import IBoard
from Moves.OOPMoveRepresentation.Move import IMove


if TYPE_CHECKING:
    from Pieces.Bishop import IBishop
    from Pieces.King import IKing
    from Pieces.Knight import IKnight
    from Pieces.Pawn import IPawn
    from Pieces.Queen import IQueen
    from Pieces.Rook import IRook


class BoardEvaluator:
    """
    Evaluates how good a given board is for the active player.


    This does not depend on the exact board class implementation. However, the
    efficiency depends on the board class implementation.
    """
    def __init__(self, board: IBoard):
        self.board = board
        board.setEvaluator(self)

    def getBoard(self):
        return self.board

    def evaluate(self):
        raise NotImplementedError

    def evaluatePawn(self, pawn: IPawn):
        raise NotImplementedError

    def evaluateKnight(self, knight: IKnight):
        raise NotImplementedError

    def evaluateBishop(self, bishop: IBishop):
        raise NotImplementedError

    def evaluateRook(self, rook: IRook):
        raise NotImplementedError

    def evaluateQueen(self, queen: IQueen):
        raise NotImplementedError

    def evaluateKing(self, king: IKing):
        raise NotImplementedError

    def supportsIncrementalCalculation(self) -> bool:
        raise NotImplementedError

    def initializeIncremental(self, board: IBoard):
        raise NotImplementedError

    def get(self):
        raise NotImplementedError

    def update(self, move: IMove):
        raise NotImplementedError

    def undo(self, move: IMove):
        raise NotImplementedError
