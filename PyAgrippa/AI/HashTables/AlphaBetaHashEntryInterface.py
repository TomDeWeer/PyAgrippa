from typing import Any

from PyAgrippa.AI.HashTables.HashTableEntryInterface import HashTableEntryInterface


class AlphaBetaHashEntryInterface(HashTableEntryInterface):
    def getOwnBestSoFar(self, entry: Any):
        raise NotImplementedError

    def getOtherBestSoFar(self, entry: Any):
        raise NotImplementedError

    def nodeFailedLow(self, entry: Any):
        score = self.getScore(entry)
        ownBestSoFar = self.getOwnBestSoFar(entry)
        assert (self.getPrincipalVariation(entry) is None) == (score == ownBestSoFar)  # I don't think score < alpha is possible
        return score == ownBestSoFar

    def nodeIsExact(self, entry: Any):
        return self.getOwnBestSoFar(entry) < self.getScore(entry) < self.getOtherBestSoFar(entry)
        # alpha < score < beta (twice < due to alphabeta implementation)

    def isCutNode(self, entry: Any):
        return self.getScore(entry=entry) >= self.getOtherBestSoFar(entry)
