from typing import Generator, Any

from PyAgrippa.Moves.MoveRepresentation import IMoveRepresentation
from PyAgrippa.Pieces.Piece import IPiece
from PyAgrippa.Squares.Square import ISquare


class ISlidingPiece(IPiece):
    def getDestinationSquaresPerRay(self, start: ISquare) -> Generator[Generator[ISquare, None, None], None, None]:
        raise NotImplementedError

    def getAllPseudoLegalMoves(self, moveRepresentation: IMoveRepresentation) -> Generator[Any, None, None]:
        board = self.getBoard()
        start = self.getSquare()
        for raySquares in self.getDestinationSquaresPerRay(start=start):
            for destinationSquare in raySquares:
                capturedPiece = board.getPieceOn(destinationSquare)
                if capturedPiece is not None:
                    if self.isWhite() == capturedPiece.isWhite():
                        break  # own piece found, stop this ray
                    else:
                        yield moveRepresentation.generateCapture(board=board, start=start,
                                                                 end=destinationSquare,
                                                                 movingPiece=self,
                                                                 capturedPiece=capturedPiece)
                        break  # enemy piece found, stop this ray
                yield moveRepresentation.generateMove(board=board,
                                                      piece=self,
                                                      start=start,
                                                      end=destinationSquare)
