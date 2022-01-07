from __future__ import annotations

from typing import Generator, Any, TYPE_CHECKING

from chess import PAWN, PieceType

from PyAgrippa.Evaluation.BoardEvaluator import BoardEvaluator
from PyAgrippa.Moves.MoveRepresentation import IMoveRepresentation
from PyAgrippa.Pieces.Piece import IPiece

if TYPE_CHECKING:
    from PyAgrippa.Pieces.Knight import IKnight
    from PyAgrippa.Pieces.Queen import IQueen


class IPawn(IPiece):

    def getPythonChessPieceType(self) -> PieceType:
        return PAWN

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

    def isPseudoLegalMove(self, move: Any, representation: IMoveRepresentation):
        if representation.isNormalMove(move) or representation.isPromotionAdvance(move):
            start = representation.getStartingSquare(move)
            end = representation.getEndingSquare(move)
            singleAdvancementSquare, _ = start.getPawnAdvancementSquare(self.isWhite())
            captured = representation.getCapturedPiece(move)
            return start == self.getSquare() and \
                   end == singleAdvancementSquare and \
                   captured == self.getBoard().getPieceOn(end)
        elif representation.isPureCaptureMove(move) or representation.isPromotionCapture(move):
            start = representation.getStartingSquare(move)
            if start != self.getSquare():
                return False
            end = representation.getEndingSquare(move)
            captureSquares = list(start.getPawnCaptureSquares(self.isWhite()))
            captureSquares = [c[0] for c in captureSquares]
            if end not in captureSquares:
                return False
            captured = representation.getCapturedPiece(move)
            if captured != self.getBoard().getPieceOn(end):
                return False
            return True
        elif representation.isDoublePawnAdvancement(move):
            start = representation.getStartingSquare(move)
            if start != self.getSquare():
                return False
            singleAdvancementSquare, _ = start.getPawnAdvancementSquare(self.isWhite())
            # if representation.getEndingSquare(move) != doubleAdvancementDestination:
            #     return False  will always be ok if properly generated
            if self.getBoard().getPieceOn(singleAdvancementSquare) is not None:
                return False
            doubleAdvancementDestination, enPassantSquare = \
                start.getDoublePawnAdvancementDestinationAndEnPassantSquare(isWhite=self.isWhite())
            if self.getBoard().getPieceOn(doubleAdvancementDestination) is not None:
                return False
            return True
        elif representation.isEnPassant(move):
            start = representation.getStartingSquare(move)
            board = self.getBoard()
            if start != self.getSquare():
                return False
            end = representation.getEndingSquare(move)
            enPassantPawn, enPassantSquare = board.getCurrentEnPassantPawnAndItsSquare()
            if end != enPassantSquare or representation.getCapturedPiece(move) != enPassantPawn:
                return False
            return True

    def getAllPseudoLegalCaptures(self, moveRepresentation: IMoveRepresentation) -> Generator[Any, None, None]:
        yield from self.generateCaptures(moveRepresentation)

    def getAllPseudoLegalNonCaptures(self, moveRepresentation: IMoveRepresentation) -> Generator[Any, None, None]:
        yield from self.generateAdvanceMoves(moveRepresentation)

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
                capturedPiece = board.getPieceOn(singleAdvancementSquare)
                if capturedPiece is None:
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

    def evaluate(self, evaluator: BoardEvaluator):
        return evaluator.evaluatePawn(self)

    def evaluateAt(self, evaluator: BoardEvaluator, square: ISquare):
        return evaluator.evaluatePawnAt(self, square=square)