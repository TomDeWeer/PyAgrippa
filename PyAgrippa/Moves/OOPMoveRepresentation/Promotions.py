#  Promotions are restricted to knights and queens, although technically bishops and rooks are also legal. This is because
#  underpromotion to bishops and rooks is especially rare.
from typing import Optional

from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Moves.OOPMoveRepresentation.Move import IMove
from PyAgrippa.Pieces.Pawn import IPawn
from PyAgrippa.Pieces.Piece import IPiece
from PyAgrippa.Squares.Square import ISquare


class Promotion(IMove):
    def __init__(self,
                 board: IBoard,
                 start: ISquare,
                 promotionSquare: ISquare,
                 pawn: IPawn,
                 capturedPiece: Optional[IPiece],
                 ):
        assert board.getPieceOn(start) == pawn
        assert board.getPieceOn(promotionSquare) == capturedPiece
        IMove.__init__(self, board=board)
        self.promotionSquare = promotionSquare
        self.start = start
        self.pawn = pawn
        self.capturedPiece = capturedPiece
        self.previousCastlingRights = None

    def apply(self):
        # four atomic actions
        # 1. remove the captured piece
        if self.capturedPiece is not None:
            self.getBoard().removePieceAndEmptySquare(square=self.promotionSquare, piece=self.capturedPiece)
        # 2. remove the pawn
        self.getBoard().removePieceAndEmptySquare(square=self.start, piece=self.pawn)
        # 3. place the promoted piece
        self.placePromotedPiece()
        # 4. en passant
        self.getBoard().setEnPassantSquare(None)

    def placePromotedPiece(self):
        self.getBoard().putPiece(piece=self.getPromotedPiece(), square=self.promotionSquare)

    def removePromotedPiece(self):
        self.getBoard().removePieceAndEmptySquare(piece=self.getPromotedPiece(), square=self.promotionSquare)

    def getPromotedPiece(self) -> IPiece:
        raise NotImplementedError

    def undo(self):
        # four atomic actions
        # 1. en passant
        self.getBoard().revertToPreviousEnPassantSquare()
        # 2. remove the promoted piece
        self.removePromotedPiece()
        # 3. place the pawn
        self.getBoard().putPiece(piece=self.pawn, square=self.start)
        # 4. place the captured piece
        if self.capturedPiece is not None:
            self.getBoard().putPiece(piece=self.capturedPiece, square=self.promotionSquare)

    def applyCastlingRightChanges(self):
        self.previousCastlingRights = self.getBoard().getAllCastlingRights()
        if self.capturedPiece is not None:
            self.getBoard().applyCastlingRightChangesDueToCaptureOfPieceAtSquare(piece=self.capturedPiece,
                                                                                 square=self.promotionSquare)

    def undoCastlingRightChanges(self):
        self.getBoard().setAllCastlingRights(self.previousCastlingRights)


class PromotionToKnight(Promotion):
    def __init__(self,
                 board: IBoard,
                 start: ISquare,
                 promotionSquare,
                 pawn: IPawn,
                 capturedPiece: Optional[IPiece]):
        Promotion.__init__(self, board=board,
                           start=start,
                           promotionSquare=promotionSquare,
                           pawn=pawn,
                           capturedPiece=capturedPiece)
        self.promotedPiece = pawn.getPromotedKnight()

    def getPromotedPiece(self) -> IPiece:
        return self.promotedPiece


class PromotionToQueen(Promotion):
    def __init__(self,
                 board: IBoard,
                 start: ISquare,
                 promotionSquare,
                 pawn: IPawn,
                 capturedPiece: Optional[IPiece]):
        Promotion.__init__(self, board=board,
                           start=start,
                           promotionSquare=promotionSquare,
                           pawn=pawn,
                           capturedPiece=capturedPiece)
        self.promotedPiece = pawn.getPromotedQueen()

    def getPromotedPiece(self) -> IPiece:
        return self.promotedPiece
