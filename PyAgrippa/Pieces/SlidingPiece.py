from typing import Generator, Any

from PyAgrippa.Moves.MoveRepresentation import IMoveRepresentation
from PyAgrippa.Pieces.Piece import IPiece
from PyAgrippa.Squares.Square import ISquare


class ISlidingPiece(IPiece):
    def getDestinationSquaresPerRay(self, start: ISquare) -> Generator[Generator[ISquare, None, None], None, None]:
        raise NotImplementedError

    def getIntermediateSquaresBetween(self, start: ISquare, end: ISquare) -> Generator[ISquare, None, None]:
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

    def getAllPseudoLegalCaptures(self, moveRepresentation: IMoveRepresentation) -> Generator[Any, None, None]:
        board = self.getBoard()
        start = self.getSquare()
        for raySquares in self.getDestinationSquaresPerRay(start=start):
            for destinationSquare in raySquares:
                capturedPiece = board.getPieceOn(destinationSquare)
                if capturedPiece is None:
                    continue
                else:
                    if self.isWhite() == capturedPiece.isWhite():
                        break  # own piece found, stop this ray
                    else:
                        yield moveRepresentation.generateCapture(board=board, start=start,
                                                                 end=destinationSquare,
                                                                 movingPiece=self,
                                                                 capturedPiece=capturedPiece)
                        break  # enemy piece found, stop this ray

    def getAllPseudoLegalNonCaptures(self, moveRepresentation: IMoveRepresentation) -> Generator[Any, None, None]:
        board = self.getBoard()
        start = self.getSquare()
        for raySquares in self.getDestinationSquaresPerRay(start=start):
            for destinationSquare in raySquares:
                capturedPiece = board.getPieceOn(destinationSquare)
                if capturedPiece is not None:
                    break
                yield moveRepresentation.generateMove(board=board,
                                                      piece=self,
                                                      start=start,
                                                      end=destinationSquare)

    def isPseudoLegalMove(self, move: Any, representation: IMoveRepresentation):
        if representation.isPureCaptureMove(move) or representation.isNormalMove(move):
            start = self.getSquare()
            end = representation.getEndingSquare(move)
            # check if start is ok
            if start != representation.getStartingSquare(move):
                return False
            # check if capture is ok (None if normal move)
            captured = self.getBoard().getPieceOn(end)
            if representation.isPureCaptureMove(move):
                if captured != representation.getCapturedPiece(move):
                    return False
                if captured is None:
                    raise NotImplementedError
            if representation.isNormalMove(move) and captured is not None:
                return False
            # check if there are no pieces in between
            try:
                for betweenSquare in self.getIntermediateSquaresBetween(start=start, end=end):
                    if self.getBoard().getPieceOn(betweenSquare) is not None:
                        return False
            except ValueError:
                raise NotImplementedError("doesn't lie on a ray, but that's impossible if the moving pieces are the same + the move generation is correct")
            return True
        else:
            raise NotImplementedError("This should not be possible")