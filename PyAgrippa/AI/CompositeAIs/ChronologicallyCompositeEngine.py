from typing import List

from PyAgrippa.AI.AI import ChessMachine
from PyAgrippa.AI.CompositeAIs.CompositeChessMachine import CompositeChessMachine
from PyAgrippa.AI.CompositeAIs.ContinuationDeciders.IContinuationDecider import IContinuationDecider
from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Moves.MoveRepresentation import IMoveRepresentation


class ChronologicallyCompositeEngine(CompositeChessMachine):
    def __init__(self, subMachines: List[ChessMachine], moveRepresentation: IMoveRepresentation,
                 continuationDeciders: List[IContinuationDecider]
                 ):
        CompositeChessMachine.__init__(self, subMachines=subMachines, moveRepresentation=moveRepresentation)
        assert len(subMachines) == len(continuationDeciders) + 1
        self.i = 0
        self.deciders = continuationDeciders

    def decideEngine(self, board: IBoard) -> ChessMachine:
        if self.i < len(self.deciders) and self.deciders[self.i].decideContinuation(board=board):
            self.i += 1
        return self.subMachines[self.i]
