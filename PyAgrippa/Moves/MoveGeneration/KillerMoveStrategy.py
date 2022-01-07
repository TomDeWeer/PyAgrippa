from typing import Dict, Generator, Any, Iterator

from PyAgrippa.Moves.MoveGeneration.MoveCollection import MoveCollection, SimpleMoveQueue


class KillerMoveStrategy:

    def injectMove(self, move: Any, depth: int):
        raise NotImplementedError

    def getInjected(self, depth: int) -> Iterator[Any]:
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError


class LAST_N(KillerMoveStrategy):
    def __init__(self, N: int):
        self.injectionQueues: Dict[int, MoveCollection] = {}
        self.N = N

    def injectMove(self, move: Any, depth: int):
        self.getInjectionQueue(depth=depth).add(move)

    def getInjectionQueue(self, depth):
        if depth not in self.injectionQueues:
            self.injectionQueues[depth] = SimpleMoveQueue(maxLength=self.N)
        return self.injectionQueues[depth]

    def getInjected(self, depth: int) -> Iterator[Any]:
        yield from self.getInjectionQueue(depth)

    def reset(self):
        self.injectionQueues = {}


class BEST_N(KillerMoveStrategy):
    def __init__(self, N: int):
        self.injectionQueues: Dict[int, BestMoveCollection] = {}
        self.N = N

    def injectMove(self, move: Any, depth: int):
        self.getInjectionQueue(depth=depth).add(move)

    def getInjectionQueue(self, depth):
        if depth not in self.injectionQueues:
            self.injectionQueues[depth] = SimpleMoveQueue(maxLength=self.N)
        return self.injectionQueues[depth]

    def getInjected(self, depth: int) -> Iterator[Any]:
        yield from self.getInjectionQueue(depth)