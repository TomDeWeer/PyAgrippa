from typing import Optional

from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Moves.OOPMoveRepresentation.Move import IMove
from PyAgrippa.Pieces.Pawn import IPawn
from PyAgrippa.Pieces.Piece import IPiece
from PyAgrippa.Squares.Square import ISquare


class EnPassant(IMove):
    def __init__(self, board: IBoard,
                 start: ISquare,
                 end: ISquare,
                 movingPiece: IPawn,
                 capturedSquare: ISquare,
                 capturedPiece: IPawn):
        IMove.__init__(self, board)
        assert self.getBoard().getPieceOn(start) is movingPiece
        assert self.getBoard().getPieceOn(capturedSquare) is capturedPiece
        assert capturedPiece.isWhite() is not movingPiece.isWhite()
        self.start = start
        self.end = end
        self.capturedSquare = capturedSquare
        self.movingPiece = movingPiece
        self.capturedPiece = capturedPiece

    def getStartingSquare(self):
        return self.start

    def getEndingSquare(self):
        return self.end

    def isEnPassant(self):
        return True

    def __str__(self):
        return f"En passant: {self.movingPiece} from {self.start} to {self.end}," \
               f" capturing {self.capturedPiece} at {self.capturedSquare}."

    def __eq__(self, other: IMove):
        if isinstance(other, EnPassant):
            return (self.start == other.start) and (self.end == other.end) and (self.movingPiece == other.movingPiece)
        else:
            return False

    def getMovingPiece(self):
        return self.movingPiece

    def getCapturedPiece(self) -> Optional[IPiece]:
        return self.capturedPiece

    def apply(self):
        # apply atomic actions
        # 1. remove the captured piece
        self.getBoard().removePieceAndEmptySquare(piece=self.capturedPiece, square=self.capturedSquare)
        # 2. move the capturing piece
        self.getBoard().movePieceSPC(piece=self.movingPiece, start=self.start, end=self.end)
        # 3. en passant
        self.getBoard().setEnPassantSquare(None)
        # 4. half move clock
        self.getBoard().resetHalfMoveClock()

    def undo(self):
        # atomic actions
        # 1. en passant
        self.getBoard().revertToPreviousEnPassantSquare()
        # 2. put the capturing piece back
        self.getBoard().movePieceSPC(piece=self.movingPiece, start=self.end, end=self.start)
        # 3. put the captured piece back
        self.getBoard().putPiece(piece=self.capturedPiece, square=self.capturedSquare)
        # 4. half move clock
        self.getBoard().revertToPreviousHalfMoveClock()

    def applyCastlingRightChanges(self):
        return # en passant will never change castling rights

    def undoCastlingRightChanges(self):
        return

