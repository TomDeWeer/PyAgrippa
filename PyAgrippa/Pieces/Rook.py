from typing import Generator

from chess import PieceType, ROOK

from PyAgrippa.Evaluation.BoardEvaluator import BoardEvaluator
from PyAgrippa.Pieces.SlidingPiece import ISlidingPiece
from PyAgrippa.Squares.Square import ISquare


class IRook(ISlidingPiece):
    def getPythonChessPieceType(self) -> PieceType:
        return ROOK

    def getDestinationSquaresPerRay(self, start: ISquare) -> Generator[Generator[ISquare, None, None], None, None]:
        return start.getRookDestinationSquares()

    def getIntermediateSquaresBetween(self, start: ISquare, end: ISquare) -> Generator[ISquare, None, None]:
        return start.getIntermediateRooksSquaresBetween(end)

    def evaluate(self, evaluator: BoardEvaluator):
        return evaluator.evaluateRook(self)

    def evaluateAt(self, evaluator: BoardEvaluator, square: ISquare):
        return evaluator.evaluateRookAt(self, square=square)
