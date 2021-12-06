from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Evaluation.BoardEvaluator import BoardEvaluator
from PyAgrippa.Moves.MoveGenerator import MoveGenerator


class AI:
    def __init__(self, moveGenerator: MoveGenerator):
        self.moveGenerator = moveGenerator

    def getMoveGenerator(self):
        return self.moveGenerator

    def getOrderingScheme(self, depth):
        pass

    def getBestMove(self, board: IBoard):
        raise NotImplementedError
