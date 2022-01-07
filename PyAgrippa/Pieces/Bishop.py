from typing import Generator

from chess import PieceType, BISHOP

from PyAgrippa.Evaluation.BoardEvaluator import BoardEvaluator
from PyAgrippa.Pieces.SlidingPiece import ISlidingPiece
from PyAgrippa.Squares.Square import ISquare


class IBishop(ISlidingPiece):
    def getPythonChessPieceType(self) -> PieceType:
        return BISHOP

    def getDestinationSquaresPerRay(self, start: ISquare) -> Generator[Generator[ISquare, None, None], None, None]:
        return start.getBishopDestinationSquares()

    def getIntermediateSquaresBetween(self, start: ISquare, end: ISquare) -> Generator[ISquare, None, None]:
        return start.getIntermediateBishopSquaresBetween(end)

    def evaluate(self, evaluator: BoardEvaluator):
        return evaluator.evaluateBishop(self)

    def evaluateAt(self, evaluator: BoardEvaluator, square: ISquare):
        return evaluator.evaluateBishopAt(self, square=square)