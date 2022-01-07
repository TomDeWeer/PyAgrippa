from typing import Any, List


class HashTableEntryInterface:
    def getPrincipalVariation(self, entry: Any) -> List[Any]:
        raise NotImplementedError

    def getBestMove(self, entry: Any) -> Any:
        return self.getPrincipalVariation(entry)[0]

    def getDepth(self, entry: Any) -> int:
        raise NotImplementedError

    def getScore(self, entry: Any) -> float:
        raise NotImplementedError


