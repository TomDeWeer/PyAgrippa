from typing import List

from PyAgrippa.AI.AI import ChessMachine, IChessMachineResult
from PyAgrippa.AI.CompositeAIs.CompositeChessMachine import CompositeChessMachine
from PyAgrippa.AI.MoveComputationError import MoveComputationError
from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Moves.MoveRepresentation import IMoveRepresentation


class ErrorBasedCompositeEngine(CompositeChessMachine):
    def __init__(self, subMachines: List[ChessMachine], moveRepresentation: IMoveRepresentation):
        CompositeChessMachine.__init__(self, moveRepresentation=moveRepresentation, subMachines=subMachines)
        self.i = 0

    def computeBestMove(self, board: IBoard) -> IChessMachineResult:
        try:
            engine = self.subMachines[self.i]
            return engine.computeBestMove(board)
        except IndexError:
            raise RuntimeError('No more chess engines left.')
        except MoveComputationError:
            self.i += 1
            return self.computeBestMove(board=board)
