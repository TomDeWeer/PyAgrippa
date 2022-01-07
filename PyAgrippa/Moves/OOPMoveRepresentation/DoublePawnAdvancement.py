from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Moves.OOPMoveRepresentation.Move import IMove
from PyAgrippa.Pieces.Pawn import IPawn
from PyAgrippa.Squares.Square import ISquare


class DoublePawnAdvancement(IMove):
    def __init__(self, board: IBoard,
                 start: ISquare,
                 end: ISquare,
                 movingPiece: IPawn,
                 enPassantSquare: ISquare,
                 ):
        IMove.__init__(self, board)
        assert self.getBoard().getPieceOn(start) is movingPiece
        self.start = start
        self.end = end
        self.movingPiece = movingPiece
        self.enPassantSquare = enPassantSquare

    def isDoublePawnAdvancement(self):
        return True

    def getStartingSquare(self):
        return self.start

    def getEndingSquare(self):
        return self.end

    def __str__(self):
        return f"{self.movingPiece} from {self.start} to {self.end}"

    def __eq__(self, other: IMove):
        if isinstance(other, DoublePawnAdvancement):
            return self.movingPiece == other.movingPiece
        else:
            return False

    def getMovingPiece(self):
        return self.movingPiece

    def apply(self):
        # apply atomic actions
        # 1. move the piece
        self.getBoard().movePieceSPC(piece=self.movingPiece, start=self.start, end=self.end)
        # 2. set the en passant square
        self.getBoard().setEnPassantSquare(self.enPassantSquare)
        #  todo: only set ep square if there are possible ep captures, i.e. if there are enemy pawns next to the
        #   destination square. This increases hashing performance & might increase pawn move generation speed.
        # 3. half move clock
        self.getBoard().resetHalfMoveClock()

    def undo(self):
        # atomic actions
        # 1. en passant
        self.getBoard().revertToPreviousEnPassantSquare()
        # 2. put the piece back
        self.getBoard().movePieceSPC(piece=self.movingPiece, start=self.end, end=self.start)
        # 3. half move clock
        self.getBoard().revertToPreviousHalfMoveClock()

    def applyCastlingRightChanges(self):
        return  # double pawn advancement will never change castling rights

    def undoCastlingRightChanges(self):
        return

