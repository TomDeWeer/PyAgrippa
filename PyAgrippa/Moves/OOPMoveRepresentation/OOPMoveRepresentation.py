from typing import Optional, Generator

from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Moves.MoveRepresentation import IMoveRepresentation, T
from PyAgrippa.Moves.OOPMoveRepresentation.Castling import Castling
from PyAgrippa.Moves.OOPMoveRepresentation.DoublePawnAdvancement import DoublePawnAdvancement
from PyAgrippa.Moves.OOPMoveRepresentation.EnPassant import EnPassant
from PyAgrippa.Moves.OOPMoveRepresentation.Move import IMove
from PyAgrippa.Moves.OOPMoveRepresentation.NormalMove import NormalMove
from PyAgrippa.Moves.OOPMoveRepresentation.Capture import CapturingMove
from PyAgrippa.Moves.OOPMoveRepresentation.Promotions import Promotion, PromotionToQueen, PromotionToKnight
from PyAgrippa.Pieces.King import IKing
from PyAgrippa.Pieces.Pawn import IPawn
from PyAgrippa.Pieces.Piece import IPiece
from PyAgrippa.Pieces.Rook import IRook
from PyAgrippa.Squares.Square import ISquare


class OOPMoveRepresentation(IMoveRepresentation):
    def isPieceCentered(self) -> bool:
        return True

    def isSquareCentered(self) -> bool:
        return True

    def toUCI(self, move: IMove) -> str:
        return move.toUCI()

    def generateMove(self,
                     board: IBoard,
                     piece: IPiece = None,
                     start: ISquare = None,
                     end: ISquare = None,
                     **kwargs) -> NormalMove:
        return NormalMove(board=board,
                          piece=piece,
                          start=start,
                          end=end)

    def generateCapture(self, board: IBoard, start: ISquare, end: ISquare, movingPiece: IPiece, capturedPiece: IPiece,
                        **kwargs) -> CapturingMove:
        return CapturingMove(start=start, end=end, movingPiece=movingPiece, capturedPiece=capturedPiece, board=board)

    def generatePromotions(self, board: IBoard,
                           start: ISquare,
                           promotionSquare: ISquare,
                           pawn: IPawn,
                           capturedPiece: Optional[IPiece],
                           ) -> Generator[Promotion, None, None]:
        """
        Generates all advancement promotion moves, i.e. promotions achieved by a pawn advancing without capturing.
        """
        # todo: promotion to bishops and rooks?
        yield PromotionToQueen(board=board, capturedPiece=capturedPiece,
                               start=start, promotionSquare=promotionSquare,
                               pawn=pawn)
        yield PromotionToKnight(board=board, capturedPiece=capturedPiece,
                                start=start, promotionSquare=promotionSquare,
                                pawn=pawn)

    def generateCastlingMove(self, board: IBoard, king: IKing, rook: IRook, kingStart: ISquare, kingEnd: ISquare, rookStart: ISquare,
                             rookEnd: ISquare, white: bool, kingSide: bool) -> Castling:
        return Castling(king=king, kingStart=kingStart, kingEnd=kingEnd, kingSide=kingSide, rook=rook,
                        rookStart=rookStart, rookEnd=rookEnd, board=board, white=white)

    def generateEnPassantMove(self,
                              board: IBoard,
                              start: ISquare,
                              end: ISquare,
                              pawn: IPawn,
                              capturedSquare: ISquare,
                              capturedPiece: IPawn
                              ) -> EnPassant:
        return EnPassant(board=board,
                         start=start,
                         end=end,
                         movingPiece=pawn,
                         capturedPiece=capturedPiece,
                         capturedSquare=capturedSquare)

    def generateDoublePawnAdvancement(self,
                                      board: IBoard,
                                      start: ISquare,
                                      end: ISquare,
                                      movingPiece: IPawn,
                                      enPassantSquare: ISquare,
                                      ):
        return DoublePawnAdvancement(
            board=board,
            start=start,
            end=end,
            movingPiece=movingPiece,
            enPassantSquare=enPassantSquare,
        )

    def isEnPassant(self, move: IMove):
        return move.isEnPassant()

    def isCastling(self, move: IMove):
        return move.isCastling()

    def isKingsideCastling(self, move: IMove):
        return move.isKingsideCastling()

    def isQueensideCastling(self, move: IMove):
        return move.isQueensideCastling()

    def isPureCaptureMove(self, move: IMove):
        return move.isPureCapturingMove()

    def isNormalMove(self, move: IMove):
        return move.isNormalMove()

    def isDoublePawnAdvancement(self, move: IMove):
        return move.isDoublePawnAdvancement()

    def isPromotionCapture(self, move: IMove):
        return move.isPromotionCapture()

    def isPromotionAdvance(self, move: IMove):
        return move.isPromotionAdvance()

    def whiteMove(self, move: IMove):
        return move.isWhiteMove()

    def getStartingSquare(self, move: IMove) -> ISquare:
        return move.getStartingSquare()

    def getEndingSquare(self, move: IMove) -> IMove:
        return move.getEndingSquare()

    def getPromotionSquare(self, move: IMove) -> ISquare:
        return move.getPromotionSquare()

    def getStartingSquareIdentifier(self, move: IMove):
        raise NotImplementedError

    def getEndingSquareIdentifier(self, move: IMove):
        raise NotImplementedError

    def getCapturedPiece(self, move: IMove) -> Optional[IPiece]:
        return move.getCapturedPiece()

    def getPromotedPiece(self, move: IMove) -> Optional[IPiece]:
        return move.getPromotedPiece()

    def getMovingPiece(self, move: IMove) -> IPiece:
        return move.getMovingPiece()

    def applyMove(self, move: IMove):
        move.applyCastlingRightChanges()  # MUST happen first!
        move.apply()
        move.getBoard().switchSideToMove()

    def undoMove(self, move: IMove):
        move.getBoard().switchSideToMove()
        move.undoCastlingRightChanges()
        move.undo()

    def toStr(self, move: IMove):
        return str(move)
