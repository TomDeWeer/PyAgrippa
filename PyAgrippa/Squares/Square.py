from __future__ import annotations

from typing import TYPE_CHECKING, Generator, Optional, Tuple

import chess

from PyAgrippa.Squares.SquareRepresentation import ISquareRepresentation, Square0x88Representation
from PyAgrippa.Tools.caching import cachedMethod

if TYPE_CHECKING:
    from PyAgrippa.Boards.Board import IBoard, BoardSCPS
    from PyAgrippa.Pieces.Piece import PieceSCPS


class ISquare:
    """
    Interface for a square on a chess board (e.g. a4).
    """

    def __init__(self, board: IBoard, representation: ISquareRepresentation = Square0x88Representation):
        self.representation = representation
        self.board = board

    def toPythonChess(self):
        return chess.square(file_index=self.getFile(), rank_index=self.getRank())

    def __str__(self):
        return f"{'abcdefgh'[self.getFile()]}{self.getRank()+1}"

    def getBoard(self) -> IBoard:
        return self.board

    def getRank(self):
        """
        Returns an integer between 0 and 7 denoting the rank.
        """
        return self.representation.getRank()

    def getFile(self):
        """
        Returns an integer between 0 and 7 denoting the rank.
        """
        return self.representation.getFile()

    def getState(self):
        return self.representation.getState()

    def liesOnBoard(self):
        return self.representation.onBoard()

    def isLightSquare(self) -> bool:
        return not self.isDarkSquare()

    def isDarkSquare(self) -> bool:
        return (self.getFile() + self.getRank()) % 2 == 0

    # Destination square generators. "Off board" checking occurs here but it is not checked if a piece already occupies
    # the destination square. The destination squares object are not returned. Instead, their internal identifier is
    # returned (e.g. (0,0) instead of the ISquare object of a1).
    # @cachedMethod
    def getKnightDestinationSquares(self) -> Generator[ISquare]:
        for identifier in self.representation.getKnightDestinationSquares():
            yield self.getBoard().getSquareViaIdentifier(identifier)

    # @cachedMethod
    def getKingDestinationSquares(self):
        for identifier in self.representation.getKingDestinationSquares():
            yield self.getBoard().getSquareViaIdentifier(identifier)

    def getRaySquareGenerators(self, raySquareIdentifiers) -> Generator[Generator[ISquare]]:
        def rayGen(someRay):
            for identifier in someRay:
                yield self.getBoard().getSquareViaIdentifier(identifier)

        for ray in raySquareIdentifiers:
            yield rayGen(ray)

    def getIntermediateRaySquareGenerator(self, identifierGenerator) -> Generator[ISquare]:
        for identifier in identifierGenerator:
            yield self.getBoard().getSquareViaIdentifier(identifier)

    # @cachedMethod
    def getRookDestinationSquares(self) -> Generator[Generator[ISquare]]:
        """
        Returns a generator containing an entry for every ray. An entry is a generator that follows the ray until it hits
        the end of the board.
        """
        return self.getRaySquareGenerators(self.representation.getRookDestinationSquares())

    # @cachedMethod
    def getQueenDestinationSquares(self) -> Generator[Generator[ISquare]]:
        return self.getRaySquareGenerators(self.representation.getQueenDestinationSquares())

    def getBishopDestinationSquares(self) -> Generator[Generator[ISquare]]:
        return self.getRaySquareGenerators(self.representation.getBishopDestinationSquares())

    def getIntermediateRooksSquaresBetween(self, end: ISquare) -> Generator[ISquare, None, None]:
        return self.getIntermediateRaySquareGenerator(identifierGenerator=self.representation.getIntermediateRookSquareGenerator(end.representation))

    def getIntermediateBishopSquaresBetween(self, end: ISquare) -> Generator[ISquare, None, None]:
        return self.getIntermediateRaySquareGenerator(identifierGenerator=self.representation.getIntermediateBishopSquareGenerator(end.representation))

    def getIntermediateQueenSquaresBetween(self, end: ISquare) -> Generator[ISquare, None, None]:
        return self.getIntermediateRaySquareGenerator(identifierGenerator=self.representation.getIntermediateQueenSquareGenerator(end.representation))

    def getPawnAdvancementSquare(self, isWhite: bool) -> Tuple[ISquare, bool]:
        """
        Returns the advancement square and a boolean denoting if it's a promotion square or not.
        """
        identifier, isPromotion = self.representation.getPawnAdvancementSquare(isWhite)
        return self.getBoard().getSquareViaIdentifier(identifier), isPromotion

    def getPawnCaptureSquares(self, isWhite: bool) -> Generator[ISquare, bool]:
        for identifier, isPromotion in self.representation.getPawnCaptureSquares(isWhite):
            yield self.getBoard().getSquareViaIdentifier(identifier), isPromotion

    # @cachedMethod
    def getEnPassantCapturedPawnSquare(self) -> ISquare:
        """
        Assuming self is an en passant square, returns the square the doubly pushed pawn is on.
        :return:
        """
        return self.getBoard().getSquareViaIdentifier(self.representation.getEnPassantCapturedPawnSquare())

    # @cachedMethod
    def getDoublePawnAdvancementDestinationAndEnPassantSquare(self, isWhite: bool) -> Tuple[Optional[ISquare], Optional[ISquare]]:
        identifier, identifierEP = self.representation.getDoublePawnAdvancementDestinationAndEnPassantSquare(isWhite)
        if identifier is None:
            return None, None
        else:
            return self.getBoard().getSquareViaIdentifier(identifier), \
                   self.getBoard().getSquareViaIdentifier(identifierEP)

    def isQueensideRookSquare(self, isWhite: bool):
        return self.representation.isQueensideRookSquare(isWhite)

    def isKingsideRookSquare(self, isWhite: bool):
        return self.representation.isKingsideRookSquare(isWhite)

    # Original square generators, i.e. the inverse of destination squares. Given a square, returns the starting square
    # a certain piece must have in order to be able to reach that square BY CAPTURE.
    # Most of the time, this is the same as calling the destination square generator of that square.

    def getKnightOriginationSquares(self) -> Generator[ISquare]:
        return self.getKnightDestinationSquares()

    def getKingOriginationSquares(self):
        return self.getKingDestinationSquares()

    def getRookOriginationSquares(self) -> Generator[Generator[ISquare]]:
        return self.getRookDestinationSquares()

    def getQueenOriginationSquares(self) -> Generator[Generator[ISquare]]:
        return self.getQueenDestinationSquares()

    def getBishopOriginationSquares(self) -> Generator[Generator[ISquare]]:
        return self.getBishopDestinationSquares()

    def getPawnOriginationCaptureSquares(self, isWhite: bool) -> Generator[ISquare, bool]:
        """
        :param isWhite: True if the pawn is white.
        :return:
        """
        return self.getPawnCaptureSquares(isWhite)

    def getKingAndRookCastlingSquares(self, kingside: bool, white: bool) -> Tuple[ISquare, ISquare]:
        kingSquareID, rookSquareID = \
            self.representation.getKingAndRookCastlingSquares(white=white, kingside=kingside)
        return self.getBoard().getSquareViaIdentifier(kingSquareID), self.getBoard().getSquareViaIdentifier(
            rookSquareID)


class SquareSCPS(ISquare):
    """
    Squares used in SCPS boards.

    Has a link to the board and to the piece that stands on top of this square.
    """

    def __init__(self, board: BoardSCPS,
                 representation: ISquareRepresentation,
                 ):
        """
        Used when creating an empty board only!
        """
        self.piece = None  # no pieces yet on the board
        ISquare.__init__(self, representation=representation, board=board)

    def __eq__(self, other: ISquare):
        if isinstance(other, ISquare):
            return self.getRank() == other.getRank() and self.getFile() == other.getFile()
        else:
            return False

    def __hash__(self):
        return hash(self.representation)

    def empty(self):
        self.piece = None

    def setPiece(self, piece: PieceSCPS):
        assert piece.getSquare() is self
        self.piece = piece

    def getPiece(self) -> Optional[PieceSCPS]:
        return self.piece


SQUARES_TUPLES = [
    A1, B1, C1, D1, E1, F1, G1, H1,
    A2, B2, C2, D2, E2, F2, G2, H2,
    A3, B3, C3, D3, E3, F3, G3, H3,
    A4, B4, C4, D4, E4, F4, G4, H4,
    A5, B5, C5, D5, E5, F5, G5, H5,
    A6, B6, C6, D6, E6, F6, G6, H6,
    A7, B7, C7, D7, E7, F7, G7, H7,
    A8, B8, C8, D8, E8, F8, G8, H8,
] = [(i, j) for j in range(8) for i in range(8)]
