from Boards.Board import IBoard
from Moves.OOPMoveRepresentation.Move import IMove
from Pieces.Pawn import IPawn
from Squares.Square import ISquare


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

    def apply(self):
        # apply atomic actions
        # 1. remove the captured piece
        self.getBoard().removePieceAndEmptySquare(piece=self.capturedPiece, square=self.capturedSquare)
        # 2. move the capturing piece
        self.getBoard().movePieceSPC(piece=self.movingPiece, start=self.start, end=self.end)
        # 3. en passant
        self.getBoard().setEnPassantSquare(None)

    def undo(self):
        # atomic actions
        # 1. en passant
        self.getBoard().revertToPreviousEnPassantSquare()
        # 2. put the capturing piece back
        self.getBoard().movePieceSPC(piece=self.movingPiece, start=self.end, end=self.start)
        # 3. put the captured piece back
        self.getBoard().putPiece(piece=self.capturedPiece, square=self.capturedSquare)

    def applyCastlingRightChanges(self):
        return # en passant will never change castling rights

    def undoCastlingRightChanges(self):
        return

