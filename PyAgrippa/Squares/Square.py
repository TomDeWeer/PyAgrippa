from __future__ import annotations

from typing import TYPE_CHECKING, Generator, Optional, Tuple

from PyAgrippa.Squares.SquareRepresentation import ISquareRepresentation, Square0x88Representation

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
    def getKnightDestinationSquares(self) -> Generator[ISquare]:
        for identifier in self.representation.getKnightDestinationSquares():
            yield self.getBoard().getSquareViaIdentifier(identifier)

    def getKingDestinationSquares(self):
        for identifier in self.representation.getKingDestinationSquares():
            yield self.getBoard().getSquareViaIdentifier(identifier)

    def getRaySquareGenerators(self, raySquareIdentifiers) -> Generator[Generator[ISquare]]:
        def rayGen(someRay):
            for identifier in someRay:
                yield self.getBoard().getSquareViaIdentifier(identifier)

        for ray in raySquareIdentifiers:
            yield rayGen(ray)

    def getRookDestinationSquares(self) -> Generator[Generator[ISquare]]:
        """
        Returns a generator containing an entry for every ray. An entry is a generator that follows the ray until it hits
        the end of the board.
        """
        return self.getRaySquareGenerators(self.representation.getRookDestinationSquares())

    def getQueenDestinationSquares(self) -> Generator[Generator[ISquare]]:
        return self.getRaySquareGenerators(self.representation.getQueenDestinationSquares())

    def getBishopDestinationSquares(self) -> Generator[Generator[ISquare]]:
        return self.getRaySquareGenerators(self.representation.getBishopDestinationSquares())

    def getPawnAdvancementSquare(self, isWhite: bool) -> Tuple[ISquare, bool]:
        """
        Returns the advancement square and a boolean denoting if it's a promotion square or not.
        """
        identifier, isPromotion = self.representation.getPawnAdvancementSquare(isWhite)
        return self.getBoard().getSquareViaIdentifier(identifier), isPromotion

    def getPawnCaptureSquares(self, isWhite: bool) -> Generator[ISquare, bool]:
        for identifier, isPromotion in self.representation.getPawnCaptureSquares(isWhite):
            yield self.getBoard().getSquareViaIdentifier(identifier), isPromotion

    def getEnPassantCapturedPawnSquare(self) -> ISquare:
        """
        Assuming self is an en passant square, returns the square the doubly pushed pawn is on.
        :return:
        """
        return self.getBoard().getSquareViaIdentifier(self.representation.getEnPassantCapturedPawnSquare())

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

    def empty(self):
        self.piece = None

    def setPiece(self, piece: PieceSCPS):
        assert piece.getSquare() is self
        self.piece = piece

    def getPiece(self) -> Optional[PieceSCPS]:
        return self.piece
