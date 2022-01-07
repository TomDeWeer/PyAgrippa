from copy import copy
from typing import Any


class MoveCollection:
    def add(self, move: Any):
        """
        If the move already exists, it's put at the start again. If not, the given move is anyway placed at the start.

        If the length exceeds the maximum length, the last added move is removed.
        """
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def __next__(self):
        raise NotImplementedError


class SimpleMoveQueue(MoveCollection):
    def __init__(self, maxLength: int):
        self.maxLength = maxLength
        self.moves = []

    def add(self, move: Any):
        # first check if it's already in the list of moves
        try:
            self.moves.remove(move)
        except ValueError:
            pass
        self.moves = [move, ] + self.moves
        self.moves = self.moves[0:self.maxLength]

    def __iter__(self):
        return iter(copy(self.moves))

    def __contains__(self, item):
        return item in self.moves


# class BestMoveCollection(MoveCollection):
#     def __init__(self, maxLength: int):
#         self.maxLength = maxLength
#         self.moves = {}
#         self.idx = None
#
#     def add(self, move: Any):
#         if self.idx is not None:
#             assert move in self.moves
#         else:
#             assert self.idx is None, "No move injection during iteration."
#         # first check if it's already in the list of moves
#         try:
#             self.moves.remove(move)
#         except ValueError:
#             pass
#         self.moves = [move, ] + self.moves
#         self.moves = self.moves[0:self.maxLength]
#
#     def __iter__(self):
#         assert self.idx is None
#         if len(self.moves) == 0:
#             self.idx = None
#         else:
#             self.idx = 0
#         return self
#
#     def __next__(self):
#         if self.idx is None:
#             raise StopIteration
#         move = self.moves[self.idx]
#         # increase idx
#         if self.idx == len(self.moves) - 1:
#             self.idx = None
#         else:
#             self.idx += 1
#         return move
#
#     def __contains__(self, item):
#         return item in self.moves