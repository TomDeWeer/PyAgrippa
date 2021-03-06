from Boards.Board import IBoard
from Pieces.Piece import IPiece
from Squares.Square import ISquare


class IMove:
    """
    Piece and Square Centric.
    """
    def __init__(self, board: IBoard):
        self.board = board

    def getBoard(self):
        return self.board

    def apply(self):
        """
        Applies everything BUT castle rights
        :return:
        """
        raise NotImplementedError

    def undo(self):
        """
        Undoes the apply()
        :return:
        """
        raise NotImplementedError

    def applyCastlingRightChanges(self):
        raise NotImplementedError

    def undoCastlingRightChanges(self):
        raise NotImplementedError


class NormalMove(IMove):
    def __init__(self, board: IBoard, start: ISquare, end: ISquare, piece: IPiece):
        IMove.__init__(self, board)
        assert self.getBoard().getPieceOn(start) == piece  # todo: run with -O flag for maximum efficiency
        assert self.getBoard().getPieceOn(end) is None
        self.start = start
        self.end = end
        self.piece = piece
        self.previousCastlingRights = None

    def apply(self):
        self.getBoard().movePieceSPC(piece=self.piece, start=self.start, end=self.end)
        self.getBoard().setEnPassantSquare(None)

    def undo(self):
        self.getBoard().movePieceSPC(piece=self.piece, start=self.end, end=self.start)
        self.getBoard().revertToPreviousEnPassantSquare()

    def applyCastlingRightChanges(self):
        self.previousCastlingRights = self.getBoard().getCastlingRightsOf(white=self.piece.isWhite())
        self.getBoard().applyCastlingRightChangesDueToMoveByPieceFromSquare(piece=self.piece, square=self.start)

    def undoCastlingRightChanges(self):
        kingside, queenside = self.previousCastlingRights
        self.getBoard().setCastlingRightsOf(white=self.piece.isWhite(), kingsideValue=kingside, queensideValue=queenside)


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

    def apply(self):
        # apply atomic actions
        # 1. remove the captured piece
        self.getBoard().removePieceAndEmptySquare(piece=self.capturedPiece, square=self.end)
        # 2. move the capturing piece
        self.getBoard().movePieceSPC(piece=self.movingPiece, start=self.start, end=self.end)
        # 3. en passant
        self.getBoard().setEnPassantSquare(None)

    def undo(self):
        # atomic actions
        # 1. en passant
        self.getBoard().revertToPreviousEnPassantSquare()
        # 2. put the moving piece back
        self.getBoard().movePieceSPC(piece=self.movingPiece, start=self.end, end=self.start)
        # 3. put the captured piece back
        self.getBoard().putPiece(piece=self.capturedPiece, square=self.end)

    def applyCastlingRightChanges(self):
        self.previousCastlingRights = self.getBoard().getAllCastlingRights()  # todo: this is not memory efficient at ALL
        self.getBoard().applyCastlingRightChangesDueToMoveByPieceFromSquare(piece=self.movingPiece, square=self.start)
        self.getBoard().applyCastlingRightChangesDueToCaptureOfPieceAtSquare(piece=self.capturedPiece, square=self.end)

    def undoCastlingRightChanges(self):
        self.getBoard().setAllCastlingRights(self.previousCastlingRights)


