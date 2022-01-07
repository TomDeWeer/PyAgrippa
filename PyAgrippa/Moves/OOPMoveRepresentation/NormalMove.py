from __future__ import annotations

from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Moves.OOPMoveRepresentation.Move import IMove
from PyAgrippa.Pieces.Piece import IPiece
from PyAgrippa.Squares.Square import ISquare


class NormalMove(IMove):
    def __init__(self, board: IBoard, start: ISquare, end: ISquare, piece: IPiece):
        IMove.__init__(self, board)
        assert self.getBoard().getPieceOn(start) == piece  # todo: run with -O flag for maximum efficiency
        assert self.getBoard().getPieceOn(end) is None
        self.start = start
        self.end = end
        self.piece = piece
        self.previousCastlingRights = None

    def isNormalMove(self):
        return True

    def getStartingSquare(self):
        return self.start

    def getEndingSquare(self):
        return self.end

    def __str__(self):
        return f"{self.piece} from {self.start} to {self.end}"

    def __eq__(self, other: IMove):
        if isinstance(other, NormalMove):
            return self.start == other.start and self.end == other.end and self.piece == other.piece \
                and self.previousCastlingRights == other.previousCastlingRights
        else:
            return False

    def apply(self):
        self.getBoard().movePieceSPC(piece=self.piece, start=self.start, end=self.end)
        self.getBoard().setEnPassantSquare(None)
        # 3. half move clock
        if self.getBoard().moveByPieceFromSquareChangesCastlingRights(piece=self.piece, square=self.start):  # move loses castling rights because of initial king or rook move
            self.getBoard().revertToPreviousHalfMoveClock()
        else:
            self.getBoard().incrementHalfMoveClock()

    def undo(self):
        self.getBoard().movePieceSPC(piece=self.piece, start=self.end, end=self.start)
        self.getBoard().revertToPreviousEnPassantSquare()
        # 3. half move clock
        self.getBoard().revertToPreviousHalfMoveClock()

    def getMovingPiece(self):
        return self.piece

    def applyCastlingRightChanges(self):
        assert self.previousCastlingRights is None

        self.previousCastlingRights = self.getBoard().getCastlingRightsOf(white=self.piece.isWhite())
        self.getBoard().applyCastlingRightChangesDueToMoveByPieceFromSquare(piece=self.piece, square=self.start)

    def undoCastlingRightChanges(self):
        kingside, queenside = self.previousCastlingRights
        self.getBoard().setCastlingRightsOf(white=self.piece.isWhite(), kingsideValue=kingside, queensideValue=queenside)
        self.previousCastlingRights = None
