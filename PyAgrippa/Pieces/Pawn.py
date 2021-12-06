from __future__ import annotations

from typing import Generator, Any, TYPE_CHECKING

from PyAgrippa.Moves.MoveRepresentation import IMoveRepresentation
from PyAgrippa.Pieces.Piece import IPiece

if TYPE_CHECKING:
    from PyAgrippa.Pieces.Knight import IKnight
    from PyAgrippa.Pieces.Queen import IQueen


class IPawn(IPiece):

    def getPromotedKnight(self) -> IKnight:
        """
        Returns an IKnight that's off the board (board.getSquareOf(knight) is None).
        """
        raise NotImplementedError

    def getPromotedQueen(self) -> IQueen:
        """
        Returns an IQueen that's off the board (board.getSquareOf(knight) is None).
        """
        raise NotImplementedError

    def getAllPseudoLegalMoves(self, moveRepresentation: IMoveRepresentation) -> Generator[Any, None, None]:
        # advance & promotion advance & double advance
        yield from self.generateAdvanceMoves(moveRepresentation)
        # captures & promotion captures & en passant captures
        yield from self.generateCaptures(moveRepresentation)

    def generateCaptures(self, moveRepresentation):
        start = self.getSquare()
        board = self.getBoard()
        for captureSquare, isPromotionSquare in start.getPawnCaptureSquares(self.isWhite()):
            capturedPiece = board.getPieceOn(captureSquare)
            if capturedPiece is not None and not (self.isWhite() is capturedPiece.isWhite()):
                if isPromotionSquare:
                    for promotion in moveRepresentation.generatePromotions(
                            board=board,
                            start=start,
                            promotionSquare=captureSquare,
                            pawn=self,
                            capturedPiece=capturedPiece):
                        yield promotion
                else:
                    yield moveRepresentation.generateCapture(
                        board=board,
                        movingPiece=self,
                        start=start,
                        end=captureSquare,
                        capturedPiece=capturedPiece
                    )
            elif capturedPiece is None:  # check if it's an en passant square
                # todo: actually it's a bit slow to check for every pawn no?
                if board.isEnPassantSquare(captureSquare):
                    capturedPawn, capturedPawnSquare = board.getCurrentEnPassantPawnAndItsSquare()
                    moveRepresentation.generateEnPassantMove(board=board,
                                                             pawn=self,
                                                             capturedSquare=capturedPawnSquare,
                                                             capturedPiece=capturedPawn,
                                                             start=start,
                                                             end=captureSquare)

    def generateAdvanceMoves(self, moveRepresentation):
        start = self.getSquare()
        board = self.getBoard()
        singleAdvancementSquare, isPromotionSquare = start.getPawnAdvancementSquare(self.isWhite())
        if board.getPieceOn(singleAdvancementSquare) is None:
            if isPromotionSquare:
                for promotion in moveRepresentation.generatePromotions(board=board,
                                                                       start=start,
                                                                       promotionSquare=singleAdvancementSquare,
                                                                       pawn=self,
                                                                       capturedPiece=None):
                    yield promotion
            else:
                yield moveRepresentation.generateMove(board=board,
                                                      piece=self,
                                                      start=start,
                                                      end=singleAdvancementSquare,
                                                      )
                # also check double jump here
                doubleAdvancementDestination, enPassantSquare = \
                    start.getDoublePawnAdvancementDestinationAndEnPassantSquare(isWhite=self.isWhite())
                if doubleAdvancementDestination is not None:
                    if board.getPieceOn(doubleAdvancementDestination) is None:
                        yield moveRepresentation.generateDoublePawnAdvancement(
                            board=board,
                            movingPiece=self,
                            start=start,
                            end=doubleAdvancementDestination,
                            enPassantSquare=enPassantSquare)
                        # todo: only set en passant square when there is an enemy pawn that can use it

    def evaluate(self):
        return self.getEvaluator().evaluatePawn(self)
