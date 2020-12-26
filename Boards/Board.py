from collections import Set
from typing import List, Optional

from Pieces.Bishop import IBishop, BishopSCPS
from Pieces.King import IKing, KingSCPS
from Pieces.Knight import IKnight, KnightSCPS
from Pieces.Pawn import IPawn, PawnSCPS
from Pieces.Piece import IPiece, PieceSCPS
from Pieces.Queen import IQueen, QueenSCPS
from Pieces.Rook import IRook, RookSCPS
from Squares.Square import ISquare, SquareSCPS
from Squares.SquareRepresentor import ISquareRepresentor, Square0x88Representor


class IBoard:
    """
    Interface to the Boards class, representing a chess board. Due to the use of a an abstract interface, the exact
    implementation is left unspecified. This is done to allow easy extension to tougher implementations such as bitboards
    later.
    """

    def __init__(self, squareRepresentor: ISquareRepresentor):
        self.squareRepresentor = squareRepresentor

    def initializePiece(self, piece: IPiece, square: ISquare):
        """
        Used during initialization of the board (and only then!).
        """
        raise NotImplementedError

    def makeMove(self):
        raise NotImplementedError

    def unmakeMove(self):
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

    def getSquare(self, file, rank) -> ISquare:
        """
        Use this only for initialization.
        """
        raise NotImplementedError

    @classmethod
    def initialSetup(cls, squareRepresentor: ISquareRepresentor = Square0x88Representor()):
        board = cls(squareRepresentor=squareRepresentor)
        # pawns
        for file in range(8):
            board.initializePiece(piece=cls.getNewPawn(isWhite=True),
                                  square=board.getSquare(file=file, rank=1))
            board.initializePiece(piece=cls.getNewPawn(isWhite=False),
                                  square=board.getSquare(file=file, rank=6))
        # rooks
        board.initializePiece(piece=cls.getNewRook(isWhite=True),
                              square=board.getSquare(file=0, rank=0))
        board.initializePiece(piece=cls.getNewRook(isWhite=True),
                              square=board.getSquare(file=7, rank=0))
        board.initializePiece(piece=cls.getNewRook(isWhite=False),
                              square=board.getSquare(file=0, rank=7))
        board.initializePiece(piece=cls.getNewRook(isWhite=False),
                              square=board.getSquare(file=7, rank=7))
        # knights
        board.initializePiece(piece=cls.getNewKnight(isWhite=True),
                              square=board.getSquare(file=1, rank=0))
        board.initializePiece(piece=cls.getNewKnight(isWhite=True),
                              square=board.getSquare(file=6, rank=0))
        board.initializePiece(piece=cls.getNewKnight(isWhite=False),
                              square=board.getSquare(file=1, rank=7))
        board.initializePiece(piece=cls.getNewKnight(isWhite=False),
                              square=board.getSquare(file=6, rank=7))
        # bishops
        board.initializePiece(piece=cls.getNewBishop(isWhite=True),
                              square=board.getSquare(file=2, rank=0))
        board.initializePiece(piece=cls.getNewBishop(isWhite=True),
                              square=board.getSquare(file=5, rank=0))
        board.initializePiece(piece=cls.getNewBishop(isWhite=False),
                              square=board.getSquare(file=2, rank=7))
        board.initializePiece(piece=cls.getNewBishop(isWhite=False),
                              square=board.getSquare(file=5, rank=7))
        # queens
        board.initializePiece(piece=cls.getNewQueen(isWhite=True),
                              square=board.getSquare(file=3, rank=0))
        board.initializePiece(piece=cls.getNewQueen(isWhite=False),
                              square=board.getSquare(file=3, rank=7))
        # kings
        board.initializePiece(piece=cls.getNewKing(isWhite=True),
                              square=board.getSquare(file=4, rank=0))
        board.initializePiece(piece=cls.getNewKing(isWhite=False),
                              square=board.getSquare(file=4, rank=7))
        return board

    def getMoves(self):
        raise NotImplementedError

    # The following methods must be provided by every board class BUT are not guaranteed to be fast! EXTERNAL USERS ARE
    # THUS ADVISED NOT TO USE THESE METHODS WHEN EFFICIENCY IS KEY
    #
    # Depending on the board representation, some methods are fast and some are not. What is guaranteed is that the
    # other methods, such as getMoves, use only the efficient methods and are thus efficient as well.

    def getSquares(self) -> List[List[ISquare]]:
        """
        Every sublist contains squares on the same rank, ordered by file from a to h. The sublists correspond to a rank
        and are ordered from 1 to 8.
        """
        raise NotImplementedError

    def getPieces(self) -> List[IPiece]:
        raise NotImplementedError

    def getPieceOn(self, square: ISquare) -> Optional[IPiece]:
        raise NotImplementedError

    def getSquareOf(self, piece: IPiece) -> ISquare:
        raise NotImplementedError


class BoardSquareCenteredWithPieceSets(IBoard):
    """
    Keeps track of squares with corresponding pieces on it (square centric) but also two piece sets (hybrid).
    
    In order to keep track of this representation without writing 'SquareCenteredWithPieceSets' everytime, it is 
    abbreviated as SCPS.
    
    Object linkage:
    the board has
    - a link to black and to white pieces (the ones that are still on the board)
    - a link to its squares
    the pieces have
    - a link to the square they're on (None if they're off the board)
    the squares have
    - a link to the board
    - a link to the piece they're on

    It's thus fully connected (except for piece to board). This is done to prevent looping over pieces in order to check
    if a square is occupied. Other implementations might use looping or use fixed indexing to check this.
    """

    def __init__(self, squareRepresentor: ISquareRepresentor = Square0x88Representor):
        IBoard.__init__(self, squareRepresentor=squareRepresentor)
        self.squares: List[List[SquareSCPS]] = [[None,]*8 for i in range(8)]
        self.initializeSquares()
        self.whitePieces = set()
        self.blackPieces = set()

    def initializeSquares(self):
        for file in range(8):
            for rank in range(8):
                square = SquareSCPS(board=self,
                                    representation=self.squareRepresentor.generateViaRankAndFile(rank=rank, file=file))
                self.addSquare(square, file, rank)

    def addSquare(self, square: SquareSCPS, file: int, rank: int):
        assert square.getBoard() is self
        self.squares[rank][file] = square

    def getSquare(self, file, rank) -> ISquare:
        """
        Use this only for initialization.
        """
        return self.squares[rank][file]

    def getSquares(self) -> List[List[SquareSCPS]]:
        return self.squares

    def initializePiece(self, piece: PieceSCPS, square: SquareSCPS):
        # connection between piece and board
        if piece.isWhite():
            self.whitePieces.add(piece)
        else:
            self.blackPieces.add(piece)
        # connection between piece and square
        piece.moveTo(square)

    def containsPiece(self, piece: IPiece):
        if piece.isWhite():
            return piece in self.whitePieces
        else:
            return piece in self.blackPieces

    @classmethod
    def getNewKing(cls, isWhite: bool) -> KingSCPS:
        return KingSCPS(isWhite)

    @classmethod
    def getNewQueen(cls, isWhite: bool) -> QueenSCPS:
        return QueenSCPS(isWhite)

    @classmethod
    def getNewRook(cls, isWhite: bool) -> RookSCPS:
        return RookSCPS(isWhite)

    @classmethod
    def getNewBishop(cls, isWhite: bool) -> BishopSCPS:
        return BishopSCPS(isWhite)

    @classmethod
    def getNewKnight(cls, isWhite: bool) -> KnightSCPS:
        return KnightSCPS(isWhite)

    @classmethod
    def getNewPawn(cls, isWhite: bool) -> PawnSCPS:
        return PawnSCPS(isWhite)

    def getMoves(self):
        pass

    def getPieceOn(self, square: SquareSCPS) -> Optional[PieceSCPS]:
        return square.getPiece()
