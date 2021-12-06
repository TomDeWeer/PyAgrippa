from typing import Generator

from PyAgrippa.Pieces.SlidingPiece import ISlidingPiece
from PyAgrippa.Squares.Square import ISquare


class IQueen(ISlidingPiece):
    def getDestinationSquaresPerRay(self, start: ISquare) -> Generator[Generator[ISquare, None, None], None, None]:
        return start.getQueenDestinationSquares()

    def evaluate(self):
        return self.getEvaluator().evaluateQueen(self)
