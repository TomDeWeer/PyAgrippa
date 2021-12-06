from typing import List, Optional, Dict, Any, Tuple

from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Pieces.Bishop import IBishop
from PyAgrippa.Pieces.King import IKing
from PyAgrippa.Pieces.Knight import IKnight
from PyAgrippa.Pieces.Pawn import IPawn
from PyAgrippa.Pieces.Piece import IPiece
from PyAgrippa.Pieces.Queen import IQueen
from PyAgrippa.Pieces.Rook import IRook
from PyAgrippa.Pieces.SCPS.BishopSCPS import BishopSCPS
from PyAgrippa.Pieces.SCPS.KingSCPS import KingSCPS
from PyAgrippa.Pieces.SCPS.KnightSCPS import KnightSCPS
from PyAgrippa.Pieces.SCPS.PawnSCPS import PawnSCPS
from PyAgrippa.Pieces.SCPS.PieceSCPS import PieceSCPS
from PyAgrippa.Pieces.SCPS.QueenSCPS import QueenSCPS
from PyAgrippa.Pieces.SCPS.RookSCPS import RookSCPS
from PyAgrippa.Squares.Square import ISquare, SquareSCPS
from PyAgrippa.Squares.SquareRepresentor import ISquareRepresentor, Square0X88Representor


class BoardSCPS(IBoard):
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
    def __init__(self,
                 squareRepresentor: ISquareRepresentor = Square0X88Representor,
                 ):
        IBoard.__init__(self,  squareRepresentor=squareRepresentor)
        self.squares: Dict[Any, SquareSCPS] = {}
        self.squaresListOfLists = None
        self.initializeSquares()
        self.allPieces: List[PieceSCPS] = []
        self.whiteToMove = True
        self.enPassantSquares: List[Optional[SquareSCPS]] = []
        self.livingWhitePieceIdentifiers = set()
        self.livingBlackPieceIdentifiers = set()
        self.previous: List[List[bool]] = []
        self.castlingRights: Tuple[bool, bool, bool, bool] = (True, True, True, True)

    def isWhiteToMove(self):
        return self.whiteToMove

    def switchSideToMove(self):
        self.whiteToMove = not self.whiteToMove

    def setWhiteToMove(self):
        self.whiteToMove = True

    def setBlackToMove(self):
        self.whiteToMove = False

    def getLivingWhitePieces(self) -> List[PieceSCPS]:
        return [self.allPieces[index] for index in self.livingWhitePieceIdentifiers]

    def getLivingBlackPieces(self) -> List[PieceSCPS]:
        return [self.allPieces[index] for index in self.livingBlackPieceIdentifiers]

    def initializeSquares(self):
        # as a dict
        for file in range(8):
            for rank in range(8):
                square = SquareSCPS(board=self,
                                    representation=self.squareRepresentor.generateViaRankAndFile(rank=rank, file=file),)
                self.addSquare(square)
        # as a list of lists
        squaresListOfLists = [[None, ] * 8 for i in range(8)]
        for square in self.squares.values():
            squaresListOfLists[square.getRank()][square.getFile()] = square
        self.squaresListOfLists = squaresListOfLists

    def addSquare(self, square: SquareSCPS):
        assert square.getBoard() is self
        self.squares[self.getIdentifierOfSquare(square)] = square

    def getSquareAt(self, file, rank) -> ISquare:
        """
        Use this only for initialization.
        """
        return self.getSquares()[rank][file]

    def getSquares(self) -> List[List[SquareSCPS]]:
        return self.squaresListOfLists

    def containsPiece(self, piece: PieceSCPS):
        if piece.isWhite():
            return piece.getIdentifier() in self.livingWhitePieceIdentifiers
        else:
            return piece.getIdentifier() in self.livingBlackPieceIdentifiers

    def getNewPiece(self, isWhite: bool, pieceClass):
        identifier = len(self.allPieces)
        piece = pieceClass(isWhite=isWhite, identifier=identifier)
        self.allPieces.append(piece)
        return piece

    def getNewKing(self, isWhite: bool) -> KingSCPS:
        return self.getNewPiece(isWhite, KingSCPS)

    def getNewQueen(self, isWhite: bool) -> QueenSCPS:
        return self.getNewPiece(isWhite, QueenSCPS)

    def getNewRook(self, isWhite: bool) -> RookSCPS:
        return self.getNewPiece(isWhite, RookSCPS)

    def getNewBishop(self, isWhite: bool) -> BishopSCPS:
        return self.getNewPiece(isWhite, BishopSCPS)

    def getNewKnight(self, isWhite: bool) -> KnightSCPS:
        return self.getNewPiece(isWhite, KnightSCPS)

    def getNewPawn(self, isWhite: bool) -> PawnSCPS:
        pawn: PawnSCPS = self.getNewPiece(isWhite, PawnSCPS)
        promotedKnight = self.getNewKnight(isWhite)
        promotedQueen = self.getNewQueen(isWhite)
        pawn.setPromotedKnight(promotedKnight)
        pawn.setPromotedQueen(promotedQueen)
        return pawn

    def getPieceOn(self, square: SquareSCPS) -> Optional[PieceSCPS]:
        return square.getPiece()

    def getPieceViaIdentifier(self, pieceIdentifier) -> PieceSCPS:
        return self.allPieces[pieceIdentifier]

    def getSquareViaIdentifier(self, identifier) -> SquareSCPS:
        return self.squares[identifier]

    def getEnPassantSquare(self) -> Optional[SquareSCPS]:
        return self.enPassantSquares[-1]

    def isEnPassantSquare(self, square: SquareSCPS) -> bool:
        return self.getEnPassantSquare() is square

    def isEnPassantSquareViaIdentifier(self, squareIdentifier: Any) -> bool:
        return self.getIdentifierOfSquare(self.getEnPassantSquare()) == squareIdentifier

    def getIdentifierOfSquare(self, square: SquareSCPS):
        return square.getState()

    def setEnPassantSquare(self, square: Optional[SquareSCPS]):
        self.enPassantSquares.append(square)

    def getCurrentEnPassantPawnAndItsSquare(self) -> Tuple[IPawn, SquareSCPS]:
        enPassantSquare = self.getEnPassantSquare()
        assert enPassantSquare is not None
        square: SquareSCPS = enPassantSquare.getEnPassantCapturedPawnSquare()
        piece = square.getPiece()
        assert isinstance(piece, PawnSCPS)
        return piece, square

    def setEnPassantSquareViaIdentifier(self, squareIdentifier: Any):
        """
        The "None" that denotes a nonexisting ep square is dependent on the square representation (i think? TODO)
        """
        self.enPassantSquares.append(self.getSquareViaIdentifier(squareIdentifier))

    def revertToPreviousEnPassantSquare(self):
        """
        This means the board keeps a list of en passant squares. This is done to prevent storing this info inside the
        moves, which will surely be memory inefficient.
        """
        self.enPassantSquares.pop()

    # castling rights

    def getCastlingRights(self, white: bool,  king: bool):
        if white:
            if king:
                return self.castlingRights[0]
            else:
                return self.castlingRights[1]
        else:
            if king:
                return self.castlingRights[2]
            else:
                return self.castlingRights[3]

    def getAllCastlingRights(self) -> Tuple[bool, bool, bool, bool]:
        """
        Returns (kingside white, queenside white, kingside black, queenside black)
        """
        return self.castlingRights

    def getCastlingRightsOf(self, white: bool) -> Tuple[bool, bool]:
        """
        Returns (kingside rights, queenside rights)
        :param white:
        :return:
        """
        if white:
            return self.castlingRights[0:2]
        else:
            return self.castlingRights[2:]

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
        whiteKing, whiteQueen, blackKing, blackQueen = self.castlingRights
        if white:
            if king:
                whiteKing = value
            else:
                whiteQueen = value
        else:
            if king:
                blackKing = value
            else:
                blackQueen = value
        self.castlingRights = whiteKing, whiteQueen, blackKing, blackQueen

    def setCastlingRightsOf(self, white: bool, kingsideValue: bool, queensideValue: bool):
        whiteKing, whiteQueen, blackKing, blackQueen = self.castlingRights
        if white:
            whiteKing = kingsideValue
            whiteQueen = queensideValue
        else:
            blackKing = kingsideValue
            blackQueen = queensideValue
        self.castlingRights = whiteKing, whiteQueen, blackKing, blackQueen

    def setAllCastlingRights(self, rights: Tuple[bool, bool, bool, bool]):
        """
        :param rights: (kingside white, queenside white, kingside black, queenside black)
        :return:
        """
        self.castlingRights = rights

    def applyCastlingRightChangesDueToMoveOf(self, piece: PieceSCPS):
        """
        PC
        """
        piece.applyCastlingRightChangesDueToMove()


    def applyCastlingRightChangesDueToMoveFrom(self, square: SquareSCPS):
        """
        SC
        """
        square.getPiece().applyCastlingRightChangesDueToMove()


    def applyCastlingRightChangesDueToMoveByPieceFromSquare(self, piece: PieceSCPS, square: SquareSCPS):
        """
        SPC
        """
        piece.applyCastlingRightChangesDueToMove()

    def applyCastlingRightChangesDueToCaptureOf(self, piece: PieceSCPS):
        """
        PC
        """
        piece.applyCastlingRightChangesDueToCapture()

    def applyCastlingRightChangesDueToCaptureAt(self, square: SquareSCPS):
        """
        SC
        """
        square.getPiece().applyCastlingRightChangesDueToCapture()

    def applyCastlingRightChangesDueToCaptureOfPieceAtSquare(self, piece: PieceSCPS, square: SquareSCPS):
        """
        SPC
        """
        piece.applyCastlingRightChangesDueToCapture()

    def isAttacked(self, square: SquareSCPS, attackerIsWhite: bool):
        # implementation starts on the square and tries every piece type
        # todo: this can most likely be improved with an attack table for every piece
        # knights
        for knightSquare in square.getKnightOriginationSquares():
            possibleKnight = self.getPieceOn(knightSquare)
            if possibleKnight is None:
                continue
            if isinstance(possibleKnight, IKnight) and (possibleKnight.isWhite() == attackerIsWhite):
                return True
        # bishops (and queens)
        for raySquares in square.getBishopOriginationSquares():
            for originSquare in raySquares:
                possiblePiece = self.getPieceOn(originSquare)
                if possiblePiece is not None:
                    if isinstance(possiblePiece, IQueen) or isinstance(possiblePiece, IBishop):
                        if attackerIsWhite == possiblePiece.isWhite():
                            return True  # unobstructed bishop or queen
                        else:
                            break  # obstruction by own pieces, break off ray
                else:
                    continue
        # rooks (and queens)
        for raySquares in square.getRookOriginationSquares():
            for originSquare in raySquares:
                possiblePiece = self.getPieceOn(originSquare)
                if possiblePiece is not None:
                    if isinstance(possiblePiece, IQueen) or isinstance(possiblePiece, IRook):
                        if attackerIsWhite == possiblePiece.isWhite():
                            return True  # unobstructed rook or queen
                        else:
                            break  # obstruction by own pieces, break off ray
                else:
                    continue
        # pawns
        for pawnSquare in square.getPawnOriginationCaptureSquares(attackerIsWhite):
            possiblePawn = self.getPieceOn(pawnSquare)
            if possiblePawn is None:
                continue
            if isinstance(possiblePawn, IPawn) and (possiblePawn.isWhite() == attackerIsWhite):
                return True
        # kings
        for kingSquare in square.getKingOriginationSquares():
            possibleKing = self.getPieceOn(kingSquare)
            if possibleKing is None:
                continue
            if isinstance(possibleKing, IKing) and (possibleKing.isWhite() == attackerIsWhite):
                return True
        return False

    def getSquareOf(self, piece: IPiece) -> SquareSCPS:
        return piece.getSquare()

    # move utilities
    def movePieceSC(self, start: SquareSCPS, end: SquareSCPS):
        piece = start.getPiece()
        piece.moveTo(end)

    def movePiecePC(self, piece: PieceSCPS, end: SquareSCPS):
        piece.moveTo(end)

    def movePieceSPC(self, piece: PieceSCPS, start: SquareSCPS, end: SquareSCPS):
        piece.moveTo(end)

    def movePieceSCViaIdentifiers(self, startIdentifier: Any, endIdentifier: Any):
        # todo: should this implementation be in the base class?
        start = self.getSquareViaIdentifier(startIdentifier)
        end = self.getSquareViaIdentifier(endIdentifier)
        self.movePieceSC(start=start, end=end)

    def movePiecePCViaIdentifiers(self, pieceIdentifier: Any, endIdentifier: Any):
        piece = self.getPieceViaIdentifier(pieceIdentifier)
        end = self.getSquareViaIdentifier(endIdentifier)
        self.movePiecePC(piece=piece, end=end)

    def movePieceSPCViaIdentifiers(self, pieceIdentifier: Any, startIdentifier: Any, endIdentifier: Any):
        """todo: PC implementation ???"""
        piece = self.getPieceViaIdentifier(pieceIdentifier)
        end = self.getSquareViaIdentifier(endIdentifier)
        self.movePiecePC(piece=piece, end=end)

    def removePiece(self, piece: PieceSCPS):
        # 1. remove the identifier from the alive pieces set
        if piece.isWhite():
            self.livingWhitePieceIdentifiers.remove(piece.getIdentifier())
        else:
            self.livingBlackPieceIdentifiers.remove(piece.getIdentifier())
        # 2. set the piece square itself to None (which also empties the square)
        piece.remove()

    def removePieceViaIdentifier(self, pieceIdentifier: Any):
        try:
            self.livingWhitePieceIdentifiers.remove(pieceIdentifier)
        except KeyError:
            self.livingBlackPieceIdentifiers.remove(pieceIdentifier)
        piece = self.getPieceViaIdentifier(pieceIdentifier)
        piece.remove()

    def emptySquare(self, square: SquareSCPS):
        piece = square.getPiece()
        self.removePiece(piece)

    def emptySquareViaIdentifier(self, squareIdentifier: Any):
        square = self.getSquareViaIdentifier(squareIdentifier)
        self.emptySquare(square)

    def removePieceAndEmptySquare(self, square: SquareSCPS, piece: PieceSCPS):
        self.removePiece(piece)

    def removePieceAndEmptySquareViaIdentifiers(self, squareIdentifier: Any, pieceIdentifier: Any):
        self.removePiece(self.getPieceViaIdentifier(pieceIdentifier))

    def putPiece(self, piece: PieceSCPS, square: SquareSCPS):
        # change the piece and square objects
        piece.put(square)
        # add it to the living pieces list
        if piece.isWhite():
            self.livingWhitePieceIdentifiers.add(piece.getIdentifier())
        else:
            self.livingBlackPieceIdentifiers.add(piece.getIdentifier())

    def putPieceViaIdentifiers(self, pieceIdentifier: Any, squareIdentifier: Any):
        self.putPiece(
            square=self.getSquareViaIdentifier(squareIdentifier),
            piece=self.getPieceViaIdentifier(pieceIdentifier)
        )







