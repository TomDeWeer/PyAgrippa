from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Evaluation.BoardEvaluator import BoardEvaluator
from PyAgrippa.Moves.MoveGenerator import MoveGenerator


class IChessMachineResult:
    def getBestMove(self):
        raise NotImplementedError

    def getEvaluation(self):
        raise NotImplementedError

    def getPrincipalVariation(self):
        raise NotImplementedError


class ChessMachine:
    def __init__(self, moveGenerator: MoveGenerator, boardEvaluator: BoardEvaluator):
        self.moveGenerator = moveGenerator
        self.boardEvaluator = boardEvaluator

    def getBoardEvaluator(self):
        return self.boardEvaluator

    def getMoveGenerator(self):
        return self.moveGenerator

    def getOrderingScheme(self, depth):
        pass

    def computeBestMove(self, board: IBoard) -> IChessMachineResult:
        raise NotImplementedError

