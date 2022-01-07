from typing import Any

from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Evaluation.BoardEvaluator import BoardEvaluator
from PyAgrippa.Moves.MoveGeneration.AbstractMoveGenerator import AbstractMoveGenerator
from PyAgrippa.Moves.MoveRepresentation import IMoveRepresentation


class IChessMachineResult:
    def getBestMove(self) -> Any:
        raise NotImplementedError

    def getEvaluation(self):
        raise NotImplementedError

    def getPrincipalVariation(self):
        raise NotImplementedError


class ChessMachine:
    def __init__(self, moveRepresentation: IMoveRepresentation):
        self.moveRepresentation = moveRepresentation
        self.name = None

    def setName(self, name: str):
        self.name = name

    def __str__(self):
        if self.name is None:
            return repr(self)
        else:
            return self.name

    def getMoveRepresentation(self):
        return self.moveRepresentation

    def getOrderingScheme(self, depth):
        pass

    def computeBestMove(self, board: IBoard) -> IChessMachineResult:
        raise NotImplementedError

