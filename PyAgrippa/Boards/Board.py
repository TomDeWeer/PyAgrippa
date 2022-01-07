from __future__ import annotations
from typing import List, Optional, Any, Tuple, TYPE_CHECKING

import chess as python_chess

from PyAgrippa.Games.Outcome import Outcome
from PyAgrippa.Moves.MoveRepresentation import IMoveRepresentation
from PyAgrippa.Pieces.Bishop import IBishop
from PyAgrippa.Pieces.King import IKing
from PyAgrippa.Pieces.Knight import IKnight
from PyAgrippa.Pieces.Pawn import IPawn
from PyAgrippa.Pieces.Piece import IPiece
from PyAgrippa.Pieces.Queen import IQueen
from PyAgrippa.Pieces.Rook import IRook
from PyAgrippa.Squares.Square import ISquare
from PyAgrippa.Squares.SquareRepresentor import ISquareRepresentor

if TYPE_CHECKING:
    from PyAgrippa.Evaluation.BoardEvaluator import BoardEvaluator


class IBoard:
    """
    Interface to the Boards class, representing a chess board. Due to the use of an abstract interface, the exact
    implementation is left unspecified. This is done to allow easy extension to tougher implementations such as bitboards
    later.
    """

    def __init__(self,
                 squareRepresentor: ISquareRepresentor,
                 ):
        self.squareRepresentor = squareRepresentor

    def __hash__(self):
        raise NotImplementedError

    def implementsHashing(self):
        try:
            hash(self)
            return True
        except NotImplementedError:
            return False

    def getSquareRepresentor(self):
        return self.squareRepresentor

    def isWhiteToMove(self):
        raise NotImplementedError

    def switchSideToMove(self):
        raise NotImplementedError

    def setWhiteToMove(self):
        raise NotImplementedError

    def setBlackToMove(self):
        raise NotImplementedError

    def getHalfMoveClock(self):
        raise NotImplementedError

    def incrementHalfMoveClock(self):
        raise NotImplementedError

    def resetHalfMoveClock(self):
        raise NotImplementedError

    def setHalfMoveClock(self, clock: int):
        raise NotImplementedError

    def revertToPreviousHalfMoveClock(self):
        raise NotImplementedError

    def containsPiece(self, piece: IPiece):
        raise NotImplementedError

    @classmethod
    def getNewKing(cls, isWhite: bool) -> IKing:
        raise NotImplementedError

    @classmethod
    def getNewQueen(cls, isWhite: bool) -> IQueen:
        raise NotImplementedError

    @classmethod
    def getNewRook(cls, isWhite: bool) -> IRook:
        raise NotImplementedError

    @classmethod
    def getNewBishop(cls, isWhite: bool) -> IBishop:
        raise NotImplementedError

    @classmethod
    def getNewKnight(cls, isWhite: bool) -> IKnight:
        raise NotImplementedError

    @classmethod
    def getNewPawn(cls, isWhite: bool) -> IPawn:
        raise NotImplementedError

    def getInitialRookSquare(self, white: bool, king: bool):
        if white:
            if king:
                return self.getSquareAt(file=7, rank=0)
            else:
                return self.getSquareAt(file=0, rank=0)
        else:
            if king:
                return self.getSquareAt(file=7, rank=7)
            else:
                return self.getSquareAt(file=0, rank=7)

    def setInitialSetup(self):
        # pawns
        for file in range(8):
            self.putPiece(piece=self.getNewPawn(isWhite=True),
                          square=self.getSquareAt(file=file, rank=1))
            self.putPiece(piece=self.getNewPawn(isWhite=False),
                          square=self.getSquareAt(file=file, rank=6))
        # rooks
        self.putPiece(piece=self.getNewRook(isWhite=True),
                      square=self.getSquareAt(file=0, rank=0))
        self.putPiece(piece=self.getNewRook(isWhite=True),
                      square=self.getSquareAt(file=7, rank=0))
        self.putPiece(piece=self.getNewRook(isWhite=False),
                      square=self.getSquareAt(file=0, rank=7))
        self.putPiece(piece=self.getNewRook(isWhite=False),
                      square=self.getSquareAt(file=7, rank=7))
        # knights
        self.putPiece(piece=self.getNewKnight(isWhite=True),
                      square=self.getSquareAt(file=1, rank=0))
        self.putPiece(piece=self.getNewKnight(isWhite=True),
                      square=self.getSquareAt(file=6, rank=0))
        self.putPiece(piece=self.getNewKnight(isWhite=False),
                      square=self.getSquareAt(file=1, rank=7))
        self.putPiece(piece=self.getNewKnight(isWhite=False),
                      square=self.getSquareAt(file=6, rank=7))
        # bishops
        self.putPiece(piece=self.getNewBishop(isWhite=True),
                      square=self.getSquareAt(file=2, rank=0))
        self.putPiece(piece=self.getNewBishop(isWhite=True),
                      square=self.getSquareAt(file=5, rank=0))
        self.putPiece(piece=self.getNewBishop(isWhite=False),
                      square=self.getSquareAt(file=2, rank=7))
        self.putPiece(piece=self.getNewBishop(isWhite=False),
                      square=self.getSquareAt(file=5, rank=7))
        # queens
        self.putPiece(piece=self.getNewQueen(isWhite=True),
                      square=self.getSquareAt(file=3, rank=0))
        self.putPiece(piece=self.getNewQueen(isWhite=False),
                      square=self.getSquareAt(file=3, rank=7))
        # kings
        self.putPiece(piece=self.getNewKing(isWhite=True),
                      square=self.getSquareAt(file=4, rank=0))
        self.putPiece(piece=self.getNewKing(isWhite=False),
                      square=self.getSquareAt(file=4, rank=7))
        # booleans
        self.setWhiteToMove()
        self.setEnPassantSquare(None)
        self.setAllCastlingRights((True, True, True, True))
        return self

    @classmethod
    def fromFEN(cls, fen: str, squareRepresentor: ISquareRepresentor) -> IBoard:
        pychessBoard = python_chess.Board(fen)
        nativeBoard = cls(squareRepresentor=squareRepresentor)
        # pieces
        for file in range(8):
            for rank in range(8):
                nativeSquare = nativeBoard.getSquareAt(file=file, rank=rank)
                pychessPiece = pychessBoard.piece_at(python_chess.square(file_index=file, rank_index=rank))
                if pychessPiece is not None:
                    white = True if pychessPiece.color is python_chess.WHITE else False
                    if python_chess.piece_name(pychessPiece.piece_type) == 'pawn':
                        nativePiece = nativeBoard.getNewPawn(isWhite=white)
                    elif python_chess.piece_name(pychessPiece.piece_type) == 'knight':
                        nativePiece = nativeBoard.getNewKnight(isWhite=white)
                    elif python_chess.piece_name(pychessPiece.piece_type) == 'bishop':
                        nativePiece = nativeBoard.getNewBishop(isWhite=white)
                    elif python_chess.piece_name(pychessPiece.piece_type) == 'rook':
                        nativePiece = nativeBoard.getNewRook(isWhite=white)
                    elif python_chess.piece_name(pychessPiece.piece_type) == 'queen':
                        nativePiece = nativeBoard.getNewQueen(isWhite=white)
                    elif python_chess.piece_name(pychessPiece.piece_type) == 'king':
                        nativePiece = nativeBoard.getNewKing(isWhite=white)
                    else:
                        raise NotImplementedError
                    nativeBoard.putPiece(piece=nativePiece,
                                         square=nativeSquare)
        # side to move
        if pychessBoard.turn is python_chess.WHITE:
            nativeBoard.setWhiteToMove()
        else:
            nativeBoard.setBlackToMove()
        # castling rights
        for white in [True, False]:
            color = python_chess.WHITE if white else python_chess.BLACK
            nativeBoard.setCastlingRightsOf(white=white,
                                            kingsideValue=pychessBoard.has_kingside_castling_rights(color=color),
                                            queensideValue=pychessBoard.has_queenside_castling_rights(color=color))
        # en passant
        if pychessBoard.ep_square is None:
            nativeBoard.setEnPassantSquare(None)
        else:
            ep_file = python_chess.square_file(pychessBoard.ep_square)
            ep_rank = python_chess.square_rank(pychessBoard.ep_square)
            nativeBoard.setEnPassantSquare(square=nativeBoard.getSquareAt(file=ep_file, rank=ep_rank))
        # half move clock
        nativeBoard.setHalfMoveClock(clock=pychessBoard.halfmove_clock)
        return nativeBoard

    def toPythonChessBoard(self) -> python_chess.Board:
        pyboard = python_chess.Board()
        pyboard.clear()
        for piece in self.getAllLivingPieces():
            square = piece.getSquare()
            pySquare = square.toPythonChess()
            pyPieceType = piece.getPythonChessPieceType()
            pyPiece = python_chess.Piece(color=piece.isWhite(), piece_type=pyPieceType)
            pyboard.set_piece_at(square=pySquare, piece=pyPiece)
        castlingFEN = f"{'K' if self.getCastlingRights(white=True, king=True) else ''}" \
                        f"{'Q' if self.getCastlingRights(white=True, king=False) else ''}" \
                        f"{'k' if self.getCastlingRights(white=False, king=True) else ''}" \
                        f"{'q' if self.getCastlingRights(white=False, king=False) else ''}"
        if len(castlingFEN) == 0:
            castlingFEN = "-"
        pyboard.set_castling_fen(castling_fen=castlingFEN)
        pyboard.ep_square = self.getEnPassantSquare().toPythonChess() if self.getEnPassantSquare() is not None else None
        pyboard.halfmove_clock = self.getHalfMoveClock()
        pyboard.turn = self.isWhiteToMove()
        return pyboard

    def toFEN(self):
        pychessBoard = self.toPythonChessBoard()
        return pychessBoard.fen()

    def getLivingWhitePieces(self) -> List[IPiece]:
        raise NotImplementedError

    def getLivingBlackPieces(self) -> List[IPiece]:
        raise NotImplementedError

    def getActivePieces(self):
        if self.isWhiteToMove():
            return self.getLivingWhitePieces()
        else:
            return self.getLivingBlackPieces()

    def getInactivePieces(self):
        if self.isWhiteToMove():
            return self.getLivingBlackPieces()
        else:
            return self.getLivingWhitePieces()

    def getAllLivingPieces(self):
        return self.getLivingBlackPieces() + self.getLivingWhitePieces()

    def checkValidity(self):
        raise NotImplementedError

    def getSquareAt(self, file: int, rank: int) -> ISquare:
        raise NotImplementedError

    def getSquareViaStr(self, square: str):
        rank = '12345678'.index(square[1])
        file = 'abcdefgh'.index(square[0])
        return self.getSquareAt(rank=rank, file=file)

    def getIdentifierOfSquare(self, square: ISquare):
        raise NotImplementedError

    def getSquares(self) -> List[List[ISquare]]:
        """
        Every sublist contains squares on the same rank, ordered by file from a to h. The sublists correspond to a rank
        and are ordered from 1 to 8.
        """
        raise NotImplementedError

    def getPieceOn(self, square: ISquare) -> Optional[IPiece]:
        raise NotImplementedError

    def getPieceViaIdentifier(self, pieceIdentifier) -> IPiece:
        raise NotImplementedError

    def getSquareOf(self, piece: IPiece) -> ISquare:
        raise NotImplementedError

    def getSquareViaIdentifier(self, identifier) -> ISquare:
        raise NotImplementedError

    # en passant square utilities
    def getEnPassantSquare(self) -> Optional[ISquare]:
        raise NotImplementedError

    def isEnPassantSquare(self, square: ISquare) -> bool:
        raise NotImplementedError

    def isEnPassantSquareViaIdentifier(self, squareIdentifier: Any) -> bool:
        raise NotImplementedError

    def getCurrentEnPassantPawnAndItsSquare(self) -> Tuple[IPawn, ISquare]:
        raise NotImplementedError

    # castling

    def getCastlingRights(self, white: bool, king: bool):
        raise NotImplementedError

    def getAllCastlingRights(self) -> Tuple[bool, bool, bool, bool]:
        """
        Returns (kingside white, queenside white, kingside black, queenside black)
        """
        raise NotImplementedError

    def getCastlingRightsOf(self, white: bool) -> Tuple[bool, bool]:
        """
        Returns (kingside rights, queenside rights)
        :param white:
        :return:
        """
        raise NotImplementedError

    # Move utilities
    # All moves can be applied as a set of atomic actions. These are defined here. Moves are applied by calling \
    # 'move.apply(board)', thereby optimally using polymorphism when 'move' is an object. However, these moves then
    # apply themselves to the board by calling these atomic actions.
    # The following atomic actions are enough to specify every move:
    # - move a piece from one square to another (empty) square
    def movePieceSC(self, start: ISquare, end: ISquare):
        """
        SC = Square Centric
        End square should be empty.
        """
        raise NotImplementedError

    def movePiecePC(self, piece: IPiece, end: ISquare):
        """
        PC = Piece Centric
        """
        raise NotImplementedError

    def movePieceSPC(self, piece: IPiece, start: ISquare, end: ISquare):
        """
        SPC = "Square and Piece Centric"
        """
        raise NotImplementedError

    def movePieceSCViaIdentifiers(self, startIdentifier: Any, endIdentifier: Any):
        raise NotImplementedError

    def movePiecePCViaIdentifiers(self, pieceIdentifier: Any, endIdentifier: Any):
        raise NotImplementedError

    def movePieceSPCViaIdentifiers(self, pieceIdentifier: Any, startIdentifier: Any, endIdentifier: Any):
        raise NotImplementedError

    # - take a piece off the board
    def removePiece(self, piece: IPiece):
        """
        PC
        """
        raise NotImplementedError

    def removePieceViaIdentifier(self, pieceIdentifier: Any):
        """
        PC
        """
        raise NotImplementedError

    def emptySquare(self, square: ISquare):
        """
        SC
        """
        raise NotImplementedError

    def emptySquareViaIdentifier(self, squareIdentifier: Any):
        """
        SC
        """
        raise NotImplementedError

    def removePieceAndEmptySquare(self, square: ISquare, piece: IPiece):
        """
        SPC
        """
        raise NotImplementedError

    def removePieceAndEmptySquareViaIdentifiers(self, squareIdentifier: Any, pieceIdentifier: Any):
        """
        SPC
        """
        raise NotImplementedError

    # - put a piece on the board (moving a piece but the start square is None)
    def putPiece(self, piece: IPiece, square: ISquare):
        """
        PC
        """
        raise NotImplementedError

    def putPieceViaIdentifiers(self, pieceIdentifier: Any, squareIdentifier: Any):
        raise NotImplementedError

    # - change castling rights
    def setCastlingRights(self, white: bool, king: bool, value: bool):
        """
        Castle rights are True if:
        - the king has not moved
        - the corresponding rook has not moved
        - the corresponding rook has not been taken

        There are four castling rights: white and black can each castle both king- and queenside.

        white: castling right for white (if False it's for black)
        king: kingside castling right if True, queenside if False
        value: True if the rights are granted, False if they are not
        """
        raise NotImplementedError

    def applyCastlingRightChangesDueToMoveOf(self, piece: IPiece):
        """
        PC
        """
        raise NotImplementedError

    def applyCastlingRightChangesDueToMoveFrom(self, square: ISquare):
        """
        SC
        """
        raise NotImplementedError

    def applyCastlingRightChangesDueToMoveByPieceFromSquare(self, piece: IPiece, square: ISquare):
        """
        SPC
        """
        raise NotImplementedError

    def moveByPieceFromSquareChangesCastlingRights(self, piece: IPiece, square: ISquare) -> bool:
        raise NotImplementedError

    def setCastlingRightsOf(self, white: bool, kingsideValue: bool, queensideValue: bool):
        raise NotImplementedError

    def applyCastlingRightChangesDueToCaptureOf(self, piece: IPiece):
        """
        PC
        """
        raise NotImplementedError

    def applyCastlingRightChangesDueToCaptureAt(self, square: ISquare):
        """
        SC
        """
        raise NotImplementedError

    def applyCastlingRightChangesDueToCaptureOfPieceAtSquare(self, piece: IPiece, square: ISquare):
        """
        SPC
        """
        raise NotImplementedError

    def setAllCastlingRights(self, rights: Tuple[bool, bool, bool, bool]):
        """
        :param rights: (kingside white, queenside white, kingside black, queenside black)
        :return:
        """
        raise NotImplementedError

    # - set en passant square
    def setEnPassantSquare(self, square: Optional[ISquare]):
        """
        If it's None then there is no en passant square.
        """
        raise NotImplementedError

    def setEnPassantSquareViaIdentifier(self, squareIdentifier: Any):
        """
        The "None" that denotes a nonexisting ep square is dependent on the square representation (i think? TODO)
        """
        raise NotImplementedError

    def revertToPreviousEnPassantSquare(self):
        """
        This means the board keeps a list of en passant squares. This is done to prevent storing this info inside the
        moves, which will surely be memory inefficient.
        :return:
        """
        raise NotImplementedError

    def isAttacked(self, square: ISquare, attackerIsWhite: bool):
        """
        Bitboards can be very fast here! # todo: if this becomes a bottleneck, implement bitboards
        """
        raise NotImplementedError

    def isGameOver(self) -> bool:
        return self.getOutcome() is not Outcome.UNDECIDED

    def getOutcome(self) -> Outcome:   # todo: this actually belongs to the Game class...
        raise NotImplementedError

    def activePlayerCanClaimDraw(self):
        raise NotImplementedError

    def kingTaken(self):
        raise NotImplementedError

    def whiteKingTaken(self):
        raise NotImplementedError

    def blackKingTaken(self):
        raise NotImplementedError

    def isLegalMove(self, move: Any, representation: IMoveRepresentation):
        raise NotImplementedError

    def isPseudoLegalMove(self, move: Any, representation: IMoveRepresentation):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError


