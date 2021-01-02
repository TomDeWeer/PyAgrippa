from typing import Any, Tuple, Optional, Generator


class ISquareRepresentation:
    """
    Internal representation of a chess square.
    """

    def getState(self):
        """
        Returns the internal representation (most of the time an integer, sometimes a tuple of 2 integers).
        """
        raise NotImplementedError

    def getRank(self):
        """
        Returns an integer between 0 and 7 denoting the rank.
        """
        raise NotImplementedError

    def getFile(self):
        """
        Returns an integer between 0 and 7 denoting the rank.
        """
        raise NotImplementedError

    def onBoard(self) -> bool:
        raise NotImplementedError

    def getKnightDestinationSquares(self) -> Generator[Any, None, None]:
        raise NotImplementedError

    def getKingDestinationSquares(self) -> Generator[Any, None, None]:
        raise NotImplementedError

    def getRookDestinationSquares(self) -> Generator[Generator[Any, None, None], None, None]:
        raise NotImplementedError

    def getBishopDestinationSquares(self) -> Generator[Generator[Any, None, None], None, None]:
        raise NotImplementedError

    def getQueenDestinationSquares(self) -> Generator[Generator[Any, None, None], None, None]:
        raise NotImplementedError

    def getPawnAdvancementSquare(self, isWhite: bool) -> Tuple[Any, bool]:
        raise NotImplementedError

    def getPawnCaptureSquares(self, isWhite: bool) -> Generator[Tuple[Any, bool], None, None]:
        raise NotImplementedError

    def getEnPassantCapturedPawnSquare(self):
        raise NotImplementedError

    def getDoublePawnAdvancementDestinationAndEnPassantSquare(self, isWhite: bool) -> Tuple[Optional[Any], Optional[Any]]:
        raise NotImplementedError

    def isQueensideRookSquare(self, isWhite: bool) -> bool:
        raise NotImplementedError

    def isKingsideRookSquare(self, isWhite: bool) -> bool:
        raise NotImplementedError

    def getKingAndRookCastlingSquares(self, kingside: bool, white: bool) -> Tuple[Any, Any]:
        raise NotImplementedError


class Square0x88Representation(ISquareRepresentation):
    knightOffsets = (18, 33, -18, -33, 31, 14, -31, -14)
    kingOffsets = (1, -1, 16, -16, 17, -17, 15, -15)
    rookRays = (1, -1, 16, -16)
    bishopRays = (17, -17, 15, -15)
    queenRays = kingOffsets

    def __init__(self, index):
        self.index = index

    @staticmethod
    def _onBoard(index):
        return not index & 0x88

    def getState(self):
        return self.index

    def getRank(self):
        return self.index >> 4

    def getFile(self):
        return self.index & 7

    def onBoard(self) -> bool:
        return self._onBoard(self.index)

    def getKnightDestinationSquares(self) -> Generator:
        start = self.index
        for offset in self.knightOffsets:
            destinationIdentifier = start + offset
            if self._onBoard(destinationIdentifier):
                yield destinationIdentifier

    def getKingDestinationSquares(self) -> Generator:
        start = self.index
        for offset in self.kingOffsets:
            destinationIdentifier = start + offset
            if self._onBoard(destinationIdentifier):
                yield destinationIdentifier

    def rayGen(self, ray: int):
        start = self.index
        i = 1
        while True:
            nextIndex = start+i*ray
            if self._onBoard(nextIndex):
                yield nextIndex
            else:
                break
            i += 1

    def getDestinationSquares(self, rays: Tuple[int, ...]) -> Generator[Generator[Any, None, None], None, None]:
        for ray in rays:
            yield self.rayGen(ray)

    def getRookDestinationSquares(self) -> Generator[Generator[Any, None, None], None, None]:
        return self.getDestinationSquares(self.rookRays)

    def getBishopDestinationSquares(self) -> Generator[Generator[Any, None, None], None, None]:
        return self.getDestinationSquares(self.bishopRays)

    def getQueenDestinationSquares(self) -> Generator[Generator[Any, None, None], None, None]:
        return self.getDestinationSquares(self.queenRays)

    def getPawnAdvancementSquare(self, isWhite: bool) -> Tuple[int, bool]:
        index = self.index
        rank = self.getRank()
        if isWhite:
            return index + 16, rank == 6
        else:
            return index - 16, rank == 1

    def getPawnCaptureSquares(self, isWhite: bool) -> Generator[Tuple[Any, bool], Any, Any]:
        index = self.index
        if isWhite:
            leftOffset = 15
            rightOffset = 17
            isPromotion = self.getRank() == 6
        else:
            leftOffset = -15
            rightOffset = -17
            isPromotion = self.getRank() == 1
        left = index + leftOffset
        if self._onBoard(left):
            yield left, isPromotion
        right = index + rightOffset
        if self._onBoard(right):
            yield right, isPromotion

    def getEnPassantCapturedPawnSquare(self):
        if self.getRank() == 2:
            return self.index + 16
        elif self.getRank() == 5:
            return self.index - 16
        else:
            raise ValueError()

    def getDoublePawnAdvancementDestinationAndEnPassantSquare(self, isWhite: bool) -> Tuple[Optional[int], Optional[int]]:
        rank = self.getRank()
        if isWhite and rank == 1:
            return self.index + 32, self.index + 16
        elif not isWhite and rank == 6:
            return self.index - 32, self.index - 16
        else:
            return None, None

    def isQueensideRookSquare(self, isWhite: bool) -> bool:
        if isWhite:
            return self.index == 0
        else:
            return self.index == 112

    def isKingsideRookSquare(self, isWhite: bool) -> bool:
        if isWhite:
            return self.index == 7
        else:
            return self.index == 119

    def getKingAndRookCastlingSquares(self, kingside: bool, white: bool) -> Tuple[int, int]:
        if white:
            if kingside:
                return 6, 5
            else:
                return 2, 3
        else:
            if kingside:
                return 118, 117
            else:
                return 114, 115


class RankFileRepresentation(ISquareRepresentation):
    """
    Just represent it as a tuple with two entries, the file and the rank (between 0 and 7).
    """
    knightOffsets = ((1, 2), (2, 1), (-1, 2), (-2, 1), (-1, -2), (-2, -1), (1, -2), (2, -1))
    kingOffsets = ((1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1))
    queenRays = kingOffsets
    bishopRays = ((1, 1), (1, -1), (-1, 1), (-1, -1))
    rookRays = ((1, 0), (0, 1), (-1, 0), (0, -1))

    def __init__(self, file: int, rank: int):
        self.rank = rank
        self.file = file

    def getState(self) -> Tuple[int, int]:
        """
        Returns the internal representation (most of the time an integer, sometimes a tuple of 2 integers).
        """
        return self.file, self.rank

    def getRank(self):
        """
        Returns an integer between 0 and 7 denoting the rank.
        """
        return self.rank

    def getFile(self):
        """
        Returns an integer between 0 and 7 denoting the rank.
        """
        return self.file

    @staticmethod
    def _onBoard(state) -> bool:
        file, rank = state
        return 0 <= file <= 7 and 0 <= rank <= 7

    def onBoard(self) -> bool:
        return self._onBoard(self.getState())

    def getKnightDestinationSquares(self) -> Generator[Any, None, None]:
        startFile, startRank = self.getState()
        for offsetFile, offsetRank in self.knightOffsets:
            yield offsetFile + startFile, offsetRank + startRank

    def getKingDestinationSquares(self) -> Generator[Any, None, None]:
        startFile, startRank = self.getState()
        for offsetFile, offsetRank in self.kingOffsets:
            yield offsetFile + startFile, offsetRank + startRank

    def rayGen(self, ray: int):
        startFile, startRank = self.getState()
        i = 1
        while True:
            nextState = (startFile+i*ray, startRank+i*ray)
            if self._onBoard(nextState):
                yield nextState
            else:
                break
            i += 1

    def getDestinationSquares(self, rays) -> Generator[Generator[Any, None, None], None, None]:
        for ray in rays:
            yield self.rayGen(ray)

    def getRookDestinationSquares(self) -> Generator[Generator[Any, None, None], None, None]:
        return self.getDestinationSquares(self.rookRays)

    def getBishopDestinationSquares(self) -> Generator[Generator[Any, None, None], None, None]:
        return self.getDestinationSquares(self.bishopRays)

    def getQueenDestinationSquares(self) -> Generator[Generator[Any, None, None], None, None]:
        return self.getDestinationSquares(self.queenRays)

    def getPawnAdvancementSquare(self, isWhite: bool) -> Tuple[Tuple[int,int], bool]:
        file, rank = self.getState()
        if isWhite:
            return (file, rank+1), rank == 6
        else:
            return (file, rank-1), rank == 1

    def getPawnCaptureSquares(self, isWhite: bool) -> Generator[Tuple[Any, bool], None, None]:
        file, rank = self.getState()
        if isWhite:
            newRank = rank+1
            isPromotion = rank == 6
        else:
            newRank = rank-1
            isPromotion = rank == 1
        left = (file-1, newRank)
        if self._onBoard(left):
            yield left, isPromotion
        right = (file+1, newRank)
        if self._onBoard(right):
            yield right, isPromotion

    def getDoublePawnAdvancementDestinationAndEnPassantSquare(self, isWhite: bool) \
            -> Tuple[Optional[Tuple[int, int]], Optional[Tuple[int, int]]]:
        file, rank = self.getState()
        if isWhite and rank == 1:
            return (file, rank + 2), (file, rank+1)
        elif not isWhite and rank == 6:
            return (file, rank - 2), (file, rank - 1)
        else:
            return None, None

    def isQueensideRookSquare(self, isWhite: bool) -> bool:
        if isWhite:
            return self.getRank() == 0 and self.getFile() == 0
        else:
            return self.getRank() == 7 and self.getFile() == 0

    def isKingsideRookSquare(self, isWhite: bool) -> bool:
        if isWhite:
            return self.getRank() == 0 and self.getFile() == 7
        else:
            return self.getRank() == 7 and self.getFile() == 7

    def getKingAndRookCastlingSquares(self, kingside: bool, white: bool) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        if white:
            if kingside:
                return (6, 0), (5, 0)
            else:
                return (2, 0), (3, 0)
        else:
            if kingside:
                return (6, 7), (5, 7)
            else:
                return (2, 7), (3, 7)




