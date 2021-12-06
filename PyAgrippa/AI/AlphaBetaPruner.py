from typing import Tuple, Optional

from PyAgrippa.AI.AI import ChessMachine
from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Evaluation.BoardEvaluator import BoardEvaluator
from PyAgrippa.Moves.MoveGenerator import MoveGenerator
from PyAgrippa.Moves.OOPMoveRepresentation.Move import IMove


class AlphaBetaPruner(ChessMachine):
    def __init__(self, depth: int, moveGenerator: MoveGenerator, boardEvaluator: BoardEvaluator):
        self.depth = depth
        ChessMachine.__init__(self, moveGenerator=moveGenerator, boardEvaluator=boardEvaluator)

    def getBestMove(self, board: IBoard) -> IMove:
        bestScore, bestMove = self.__getBestMove__(board, depth=self.depth,
                                                   bestSoFar=float('inf'),
                                                   worstSoFar=float('-inf'))
        return bestMove

    def __getBestMove__(self, board: IBoard, depth: int, bestSoFar: float, worstSoFar: float) -> Tuple[float, Optional[IMove]]:
        evaluator = self.getBoardEvaluator()
        if depth == 0:
            return evaluator.evaluate(board), None
        moveGenerator = self.getMoveGenerator()
        moveRepresentation = moveGenerator.getRepresentation()
        bestMove = None
        for move in moveGenerator.generatePseudoLegalMoves(board=board):
            moveRepresentation.applyMove(move)
            score, _ = self.__getBestMove__(board, depth=depth-1, bestSoFar=-worstSoFar, worstSoFar=-bestSoFar)
            score *= -1   # now score is relative to active player here
            moveRepresentation.undoMove(move)
            if score >= worstSoFar:  # fail-hard beta cutoff
                return score, move
            if score > bestSoFar:
                bestSoFar = score
                bestMove = move

        return bestSoFar, bestMove

