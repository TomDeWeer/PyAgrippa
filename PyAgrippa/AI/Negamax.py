from typing import Tuple, Optional

from PyAgrippa.AI.AI import ChessMachine
from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Evaluation.BoardEvaluator import BoardEvaluator
from PyAgrippa.Moves.MoveGenerator import MoveGenerator
from PyAgrippa.Moves.OOPMoveRepresentation.Move import IMove


class Negamax(ChessMachine):
    def __init__(self, depth: int, moveGenerator: MoveGenerator, boardEvaluator: BoardEvaluator):
        self.depth = depth
        ChessMachine.__init__(self, moveGenerator=moveGenerator, boardEvaluator=boardEvaluator)

    def getBestMove(self, board: IBoard) -> IMove:
        bestScore, bestMove = self.__getBestMove__(board, depth=self.depth)
        return bestMove

    def __getBestMove__(self, board: IBoard, depth: int) -> Tuple[float, Optional[IMove]]:
        evaluator = self.getBoardEvaluator()
        if depth == 0:
            return evaluator.evaluate(board), None
        moveGenerator = self.getMoveGenerator()
        moveRepresentation = moveGenerator.getRepresentation()
        bestScore = float('inf')
        bestMove = None
        for move in moveGenerator.generatePseudoLegalMoves(board=board):
            moveRepresentation.applyMove(move)
            score, _ = self.__getBestMove__(board, depth=depth-1)
            moveRepresentation.undoMove(move)
            if score < bestScore:
                bestScore = score
                bestMove = move
        return bestScore, bestMove

