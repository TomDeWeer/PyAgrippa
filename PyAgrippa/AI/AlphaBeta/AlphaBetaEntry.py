from typing import Any

from PyAgrippa.AI.HashTables.HashTableEntry import HashTableEntry


class AlphaBetaEntry(HashTableEntry):
    def __init__(self, move: Any, score: int, depth: int):
        # todo: add upper and lower bounds on the score, principal variation not needed
        self.move = move
        self.score = score
        self.depth = depth

    def getDepth(self):
        return self.depth

    def getScore(self):
        return self.score

    def getMove(self):
        return self.move
