from typing import Generator

from chess import PieceType, QUEEN

from PyAgrippa.Evaluation.BoardEvaluator import BoardEvaluator
from PyAgrippa.Pieces.SlidingPiece import ISlidingPiece
from PyAgrippa.Squares.Square import ISquare


class IQueen(ISlidingPiece):
    def getPythonChessPieceType(self) -> PieceType:
        return QUEEN

    def getDestinationSquaresPerRay(self, start: ISquare) -> Generator[Generator[ISquare, None, None], None, None]:
        return start.getQueenDestinationSquares()

    def getIntermediateSquaresBetween(self, start: ISquare, end: ISquare) -> Generator[ISquare, None, None]:
        return start.getIntermediateQueenSquaresBetween(end)

    def evaluate(self, evaluator: BoardEvaluator):
        return evaluator.evaluateQueen(self)

    def evaluateAt(self, evaluator: BoardEvaluator, square: ISquare):
        return evaluator.evaluateQueenAt(self, square=square)
