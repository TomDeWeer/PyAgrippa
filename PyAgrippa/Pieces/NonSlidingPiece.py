from typing import Generator, Any

from PyAgrippa.Moves.MoveRepresentation import IMoveRepresentation
from PyAgrippa.Pieces.Piece import IPiece
from PyAgrippa.Squares.Square import ISquare


class INonSlidingPiece(IPiece):

    def getDestinationSquares(self, start: ISquare):
        raise NotImplementedError

    def __getAllPseudoLegalMoves__(self, moveRepresentation: IMoveRepresentation) -> Generator[Any, None, None]:
        board = self.getBoard()
        start = self.getSquare()
        for destinationSquare in self.getDestinationSquares(start=start):
            capturedPiece = board.getPieceOn(destinationSquare)
            if capturedPiece is not None:
                if self.isWhite() == capturedPiece.isWhite():
                    continue
                else:
                    yield moveRepresentation.generateCapture(board=board, start=start,
                                                             end=destinationSquare,
                                                             movingPiece=self,
                                                             capturedPiece=capturedPiece)
            else:
                yield moveRepresentation.generateMove(
                    board=board,
                    piece=self,
                    start=start,
                    end=destinationSquare)

    def __getAllPseudoLegalCaptures__(self, moveRepresentation: IMoveRepresentation) -> Generator[Any, None, None]:
        board = self.getBoard()
        start = self.getSquare()
        for destinationSquare in self.getDestinationSquares(start):
            capturedPiece = board.getPieceOn(destinationSquare)
            if capturedPiece is None:
                continue
            else:
                if self.isWhite() == capturedPiece.isWhite():
                    continue
                else:
                    yield moveRepresentation.generateCapture(board=board, start=start,
                                                             end=destinationSquare,
                                                             movingPiece=self,
                                                             capturedPiece=capturedPiece)

    def __getAllPseudoLegalNonCaptures__(self, moveRepresentation: IMoveRepresentation) -> Generator[Any, None, None]:
        board = self.getBoard()
        start = self.getSquare()
        for destinationSquare in self.getDestinationSquares(start):
            capturedPiece = board.getPieceOn(destinationSquare)
            if capturedPiece is None:
                yield moveRepresentation.generateMove(
                    board=board,
                    piece=self,
                    start=start,
                    end=destinationSquare)
            else:
                continue

    def isPseudoLegalMove(self, move: Any, representation: IMoveRepresentation):
        start = representation.getStartingSquare(move)
        end = representation.getEndingSquare(move)
        captured = representation.getCapturedPiece(move)
        return start == self.getSquare() and \
            end in self.getDestinationSquares(self.getSquare()) and \
            captured == self.getBoard().getPieceOn(end)
