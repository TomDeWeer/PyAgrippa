from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Evaluation.BoardEvaluator import BoardEvaluator
from PyAgrippa.Moves.MoveGenerator import MoveGenerator


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

    def getBestMove(self, board: IBoard):
        raise NotImplementedError
