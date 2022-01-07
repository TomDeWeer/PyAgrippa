from typing import Any, List, Tuple

from PyAgrippa.AI.HashTables.AlphaBetaHashEntryInterface import AlphaBetaHashEntryInterface

AlphaBetaTupleEntryType = Tuple[float, List[Any], int, float, float]


class AlphaBetaTupleInterface(AlphaBetaHashEntryInterface):
    """
    For entry tuples made up as follows:
     score, pv, depth, ownBestSoFar, otherBestSoFar
    """

    def getDepth(self, entry: AlphaBetaTupleEntryType) -> int:
        return entry[2]

    def getScore(self, entry: AlphaBetaTupleEntryType) -> float:
        return entry[0]

    def getPrincipalVariation(self, entry: AlphaBetaTupleEntryType) -> List[Any]:
        return entry[1]

    def getOwnBestSoFar(self, entry: AlphaBetaTupleEntryType):
        return entry[3]

    def getOtherBestSoFar(self, entry: AlphaBetaTupleEntryType):
        return entry[4]



