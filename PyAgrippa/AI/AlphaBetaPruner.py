from typing import Tuple, Optional

from PyAgrippa.AI.AI import ChessMachine, IChessMachineResult
from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Evaluation.BoardEvaluator import BoardEvaluator
from PyAgrippa.Moves.MoveGenerator import MoveGenerator
from PyAgrippa.Moves.OOPMoveRepresentation.Move import IMove


class AlphaBetaResult(IChessMachineResult):
    def __init__(self, bestMove: IMove, score: float):
        self.score = score
        self.bestMove = bestMove

    def getBestMove(self):
        return self.bestMove

    def getEvaluation(self):
        return self.score


class AlphaBetaPruner(ChessMachine):
    def __init__(self, depth: int, moveGenerator: MoveGenerator, boardEvaluator: BoardEvaluator, useIncremental=True):
        self.depth = depth
        self.useIncremental = useIncremental
        ChessMachine.__init__(self, moveGenerator=moveGenerator, boardEvaluator=boardEvaluator)

    def computeBestMove(self, board: IBoard) -> AlphaBetaResult:
        if self.getBoardEvaluator().supportsIncrementalCalculation() and self.useIncremental:
            self.getBoardEvaluator().initializeIncremental(board=board, moveRepresentation=self.getMoveGenerator().getRepresentation())
            bestScore, bestMove = self.__getBestMove_incremental__(board, depth=self.depth,
                                                                   ownBestSoFar=float('-inf'),
                                                                   otherBestSoFar=float('inf'))
        else:
            bestScore, bestMove = self.__getBestMove__(board, depth=self.depth,
                                                       ownBestSoFar=float('-inf'),
                                                       otherBestSoFar=float('inf'))
        return AlphaBetaResult(bestMove=bestMove, score=bestScore)

    def __getBestMove__(self, board: IBoard, depth: int, ownBestSoFar: float, otherBestSoFar: float) -> Tuple[
        float, Optional[IMove]]:
        """
        Scores must be interpreted (in a certain function call) as follows:
        * the current active player wants to maximize it
        * they are relative to the current active player
        """
        evaluator = self.getBoardEvaluator()
        if depth == 0:
            return evaluator.evaluate(board), None
        moveGenerator = self.getMoveGenerator()
        moveRepresentation = moveGenerator.getRepresentation()
        bestMove = None
        for move in moveGenerator.generatePseudoLegalMoves(board=board):
            moveRepresentation.applyMove(move)
            score, _ = self.__getBestMove__(board, depth=depth - 1, ownBestSoFar=-otherBestSoFar,
                                            otherBestSoFar=-ownBestSoFar)
            score *= -1  # now score is relative to active player here
            moveRepresentation.undoMove(move)
            if score >= otherBestSoFar:  # fail-hard beta cutoff
                return score, move
            if score > ownBestSoFar:
                ownBestSoFar = score
                bestMove = move
        return ownBestSoFar, bestMove

    def __getBestMove_incremental__(self, board: IBoard, depth: int, ownBestSoFar: float, otherBestSoFar: float) \
            -> Tuple[float, Optional[IMove]]:
        """
        """
        evaluator = self.getBoardEvaluator()
        moveGenerator = self.getMoveGenerator()
        moveRepresentation = moveGenerator.getRepresentation()
        bestMove = None
        for move in moveGenerator.generatePseudoLegalMoves(board=board):
            if depth == 1:  # don't go until depth=0, applying last move is not necessary
                evaluator.applyMove(move)
                score = evaluator.getScore()
                evaluator.undoLast()
            else:
                evaluator.applyMove(move)
                moveRepresentation.applyMove(move)
                score, _ = self.__getBestMove_incremental__(board, depth=depth - 1, ownBestSoFar=-otherBestSoFar,
                                                            otherBestSoFar=-ownBestSoFar)
                moveRepresentation.undoMove(move)
                evaluator.undoLast()
            score *= -1
            if score >= otherBestSoFar:  # fail-hard beta cutoff
                return score, move
            if score > ownBestSoFar:
                ownBestSoFar = score
                bestMove = move

        return ownBestSoFar, bestMove
