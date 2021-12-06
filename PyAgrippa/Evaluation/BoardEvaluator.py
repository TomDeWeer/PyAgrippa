from __future__ import annotations
from typing import TYPE_CHECKING
from PyAgrippa.Moves.OOPMoveRepresentation.Move import IMove


if TYPE_CHECKING:
    from PyAgrippa.Pieces.Bishop import IBishop
    from PyAgrippa.Pieces.King import IKing
    from PyAgrippa.Pieces.Knight import IKnight
    from PyAgrippa.Pieces.Pawn import IPawn
    from PyAgrippa.Pieces.Queen import IQueen
    from PyAgrippa.Pieces.Rook import IRook
    from PyAgrippa.Boards.Board import IBoard


class BoardEvaluator:
    """
    Evaluates how good a given board is for the active player.


    This does not depend on the exact board class implementation. However, the
    efficiency depends on the board class implementation.
    """
    def __init__(self):
        pass

    def evaluate(self, board: IBoard):
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
