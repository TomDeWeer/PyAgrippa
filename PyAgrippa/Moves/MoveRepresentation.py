from __future__ import annotations

from typing import Generic, TypeVar, Generator, Optional, TYPE_CHECKING

T = TypeVar('T')  # type of the move # a move can be anything! a list of positions, an object, an integer...

if TYPE_CHECKING:
    from PyAgrippa.Boards.Board import IBoard
    from PyAgrippa.Pieces.Pawn import IPawn
    from PyAgrippa.Pieces.Piece import IPiece
    from PyAgrippa.Squares.Square import ISquare
    from PyAgrippa.Pieces.King import IKing
    from PyAgrippa.Pieces.Rook import IRook


class IMoveRepresentation(Generic[T]):
    """
    Interface to various move representations.
    """

    # def isPieceCentered(self) -> bool:
    #     """
    #     Returns True if the representation is piece centered (meaning pieces must be supplied in order to generate
    #     moves)
    #     """
    #     raise NotImplementedError
    #
    # def isSquareCentered(self) -> bool:
    #     """
    #     Returns True if the representation is square centered (meaning square must be supplied in order to generate
    #     moves)
    #     """
    #     raise NotImplementedError

    def toUCI(self, move: T) -> str:
        raise NotImplementedError

    def generateMove(self, board: IBoard,
                     piece: IPiece = None,
                     start: ISquare = None,
                     end: ISquare = None,
                     **kwargs) -> T:
        raise NotImplementedError

    def generateCapture(self, board: IBoard,
                        start: ISquare,
                        end: ISquare,
                        movingPiece: IPiece,
                        capturedPiece: IPiece,
                        **kwargs
                        ):
        raise NotImplementedError

    def generatePromotions(self, board: IBoard,
                           start: ISquare,
                           promotionSquare: ISquare,
                           pawn: IPawn,
                           capturedPiece: Optional[IPiece],
                           ) -> Generator[T]:
        """
        Generates all advancement promotion moves, i.e. promotions achieved by a pawn advancing without capturing.
        :return:
        """
        raise NotImplementedError

    def generateCastlingMove(self, board: IBoard, king: IKing, rook: IRook, kingStart: ISquare, kingEnd: ISquare, rookStart: ISquare,
                             rookEnd: ISquare, white: bool, kingSide: bool) -> T:
        raise NotImplementedError

    def generateEnPassantMove(self,
                              board: IBoard,
                              start: ISquare,
                              end: ISquare,
                              pawn: IPawn,
                              capturedSquare: ISquare,
                              capturedPiece: IPawn
                              ) -> T:
        raise NotImplementedError

    def generateDoublePawnAdvancement(self,
                                      board: IBoard,
                                      start: ISquare,
                                      end: ISquare,
                                      movingPiece: IPawn,
                                      enPassantSquare: ISquare,
                                      ):
        # todo: computing all of this is probably unnecessary for a minimal representation
        #  i therefore should have a flag specifying what needs to be computed on beforehand (and sequentially stored
        #  in the move representation) and what needs to be computed only when the move is applied.
        raise NotImplementedError

    def isEnPassant(self, move: T):
        raise NotImplementedError

    def isCastling(self, move: T):
        raise NotImplementedError

    def isKingsideCastling(self, move):
        raise NotImplementedError

    def isQueensideCastling(self, move):
        raise NotImplementedError

    def isPureCaptureMove(self, move: T):
        raise NotImplementedError

    def isNormalMove(self, move: T):
        raise NotImplementedError

    def isDoublePawnAdvancement(self, move: T):
        raise NotImplementedError

    def isPromotionCapture(self, move: T):
        raise NotImplementedError

    def isPromotionAdvance(self, move: T):
        raise NotImplementedError

    def whiteMove(self, move: T):
        raise NotImplementedError

    def blackMove(self, move: T):
        return not self.whiteMove(move=move)

    def getStartingSquare(self, move: T) -> ISquare:
        raise NotImplementedError

    def getEndingSquare(self, move: T) -> ISquare:
        raise NotImplementedError

    def getPromotionSquare(self, move: T) -> ISquare:
        raise NotImplementedError

    def getStartingSquareIdentifier(self, move: T):
        raise NotImplementedError

    def getEndingSquareIdentifier(self, move: T):
        raise NotImplementedError

    def getCapturedPiece(self, move: T) -> Optional[IPiece]:
        raise NotImplementedError

    def getPromotedPiece(self, move: T) -> Optional[IPiece]:
        raise NotImplementedError

    def getMovingPiece(self, move: T) -> IPiece:
        raise NotImplementedError

    def applyMove(self, move: T):  # todo: it's maybe not logical that a representation applies a move
        raise NotImplementedError

    def undoMove(self, move: T): # todo: shouldnt the board also be applied in general?
        raise NotImplementedError

    def toStr(self, move: T):
        raise NotImplementedError




