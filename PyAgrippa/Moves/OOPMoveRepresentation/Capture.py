from __future__ import annotations

from typing import Optional

from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Moves.OOPMoveRepresentation.Move import IMove
from PyAgrippa.Pieces.Piece import IPiece
from PyAgrippa.Squares.Square import ISquare


class CapturingMove(IMove):
    """
    Pure capturing move (no en passant or promotion capture)
    """
    def __init__(self, board: IBoard, start: ISquare, end: ISquare, movingPiece: IPiece, capturedPiece: IPiece):
        IMove.__init__(self, board)
        assert self.getBoard().getPieceOn(start) is movingPiece
        assert self.getBoard().getPieceOn(end) is capturedPiece
        assert capturedPiece.isWhite() is not movingPiece.isWhite()
        self.start = start
        self.end = end
        self.movingPiece = movingPiece
        self.capturedPiece = capturedPiece
        self.previousCastlingRights = None

    def getStartingSquare(self):
        return self.start

    def getEndingSquare(self):
        return self.end

    def isPureCapturingMove(self):
        return True

    def __str__(self):
        return f"{self.movingPiece} from {self.start} to {self.end}, capturing {self.capturedPiece}"

    def __eq__(self, other: IMove):
        if isinstance(other, CapturingMove):
            return self.start == other.start and self.end == other.end and self.movingPiece == other.movingPiece \
                    and self.capturedPiece == other.capturedPiece and self.previousCastlingRights == other.previousCastlingRights
        else:
            return False

    def getCapturedPiece(self) -> Optional[IPiece]:
        return self.capturedPiece

    def getMovingPiece(self):
        return self.movingPiece

    def apply(self):
        # apply atomic actions
        # 1. remove the captured piece
        self.getBoard().removePieceAndEmptySquare(piece=self.capturedPiece, square=self.end)
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
        # 2. put the moving piece back
        self.getBoard().movePieceSPC(piece=self.movingPiece, start=self.end, end=self.start)
        # 3. put the captured piece back
        self.getBoard().putPiece(piece=self.capturedPiece, square=self.end)
        # 4. half move clock
        self.getBoard().revertToPreviousHalfMoveClock()

    def applyCastlingRightChanges(self):
        assert self.previousCastlingRights is None
        self.previousCastlingRights = self.getBoard().getAllCastlingRights()  # todo: this is not memory efficient at ALL
        self.getBoard().applyCastlingRightChangesDueToMoveByPieceFromSquare(piece=self.movingPiece, square=self.start)
        self.getBoard().applyCastlingRightChangesDueToCaptureOfPieceAtSquare(piece=self.capturedPiece, square=self.end)

    def undoCastlingRightChanges(self):
        self.getBoard().setAllCastlingRights(self.previousCastlingRights)
        self.previousCastlingRights = None
