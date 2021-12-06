from typing import Generator

from PyAgrippa.Pieces.SlidingPiece import ISlidingPiece
from PyAgrippa.Squares.Square import ISquare


class IRook(ISlidingPiece):
    def getDestinationSquaresPerRay(self, start: ISquare) -> Generator[Generator[ISquare, None, None], None, None]:
        return start.getRookDestinationSquares()

    def evaluate(self):
        return self.getEvaluator().evaluateRook(self)

