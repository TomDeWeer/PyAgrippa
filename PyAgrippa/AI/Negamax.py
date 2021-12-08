from typing import Tuple, Optional

from PyAgrippa.AI.AI import ChessMachine, IChessMachineResult
from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Evaluation.BoardEvaluator import BoardEvaluator
from PyAgrippa.Moves.MoveGenerator import MoveGenerator
from PyAgrippa.Moves.OOPMoveRepresentation.Move import IMove


class NegamaxResult(IChessMachineResult):
    def __init__(self, bestMove: IMove, score: float):
        self.score = score
        self.bestMove = bestMove

    def getBestMove(self):
        return self.bestMove

    def getEvaluation(self):
        return self.score


class Negamax(ChessMachine):
    def __init__(self, depth: int, moveGenerator: MoveGenerator, boardEvaluator: BoardEvaluator):
        self.depth = depth
        ChessMachine.__init__(self, moveGenerator=moveGenerator, boardEvaluator=boardEvaluator)

    def computeBestMove(self, board: IBoard) -> NegamaxResult:
        bestScore, bestMove = self.__getBestMove__(board, depth=self.depth)
        return NegamaxResult(bestMove=bestMove, score=bestScore)

    def __getBestMove__(self, board: IBoard, depth: int) -> Tuple[float, Optional[IMove]]:
        evaluator = self.getBoardEvaluator()
        if depth == 0:
            return evaluator.evaluate(board), None
        moveGenerator = self.getMoveGenerator()
        moveRepresentation = moveGenerator.getRepresentation()
        bestScore = float('-inf')
        bestMove = None
        for move in moveGenerator.generatePseudoLegalMoves(board=board):
            moveRepresentation.applyMove(move)
            score, _ = self.__getBestMove__(board, depth=depth-1)
            score *= -1
            moveRepresentation.undoMove(move)
            if score > bestScore:
                bestScore = score
                bestMove = move
        return bestScore, bestMove

