from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Moves.OOPMoveRepresentation.Move import IMove
from PyAgrippa.Pieces.King import IKing
from PyAgrippa.Pieces.Rook import IRook
from PyAgrippa.Squares.Square import ISquare


class Castling(IMove):
    def __init__(self, board: IBoard,
                 king: IKing,
                 kingStart: ISquare,
                 kingEnd: ISquare,
                 rook: IRook,
                 rookStart: ISquare,
                 rookEnd: ISquare,
                 kingSide: bool,
                 white: bool
                 ):
        IMove.__init__(self, board=board)
        assert self.getBoard().getPieceOn(kingStart) is king
        assert self.getBoard().getPieceOn(rookStart) is rook
        assert white == king.isWhite() and white == rook.isWhite()
        self.king = king
        self.kingStart = kingStart
        self.kingEnd = kingEnd
        self.rook = rook
        self.rookStart = rookStart
        self.rookEnd = rookEnd
        self.kingSide = kingSide
        self.previousCastlingRights = None
        self.white = white

    def getMovingPiece(self):
        return self.king

    def apply(self):
        # apply atomic actions
        # 1. move the king
        self.getBoard().movePieceSPC(piece=self.king, start=self.kingStart, end=self.kingEnd)
        # 2. move the rook
        self.getBoard().movePieceSPC(piece=self.rook, start=self.rookStart, end=self.rookEnd)
        # 3. en passant
        self.getBoard().setEnPassantSquare(None)

    def undo(self):
        # atomic actions
        # 1. en passant
        self.getBoard().revertToPreviousEnPassantSquare()
        # 1. move the rook back
        self.getBoard().movePieceSPC(piece=self.rook, start=self.rookEnd, end=self.rookStart)
        # 2. move the king back
        self.getBoard().movePieceSPC(piece=self.king, start=self.kingEnd, end=self.kingStart)

    def applyCastlingRightChanges(self):
        self.previousCastlingRights = self.getBoard().getAllCastlingRights()  # todo: this is not memory efficient at ALL
        self.getBoard().setCastlingRightsOf(white=self.white, kingsideValue=False, queensideValue=False)

    def undoCastlingRightChanges(self):
        self.getBoard().setAllCastlingRights(self.previousCastlingRights)



