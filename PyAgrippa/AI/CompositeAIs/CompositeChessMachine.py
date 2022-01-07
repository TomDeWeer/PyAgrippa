from abc import ABC
from typing import List

from PyAgrippa.AI.AI import ChessMachine, IChessMachineResult
from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Moves.MoveGeneration.AbstractMoveGenerator import AbstractMoveGenerator
from PyAgrippa.Moves.MoveRepresentation import IMoveRepresentation


class CompositeChessMachine(ChessMachine, ABC):
    def __init__(self, subMachines: List[ChessMachine], moveRepresentation: IMoveRepresentation):
        #  todo: allow for transitioning between chess machines based on board state (middle vs endgame) & errors thrown
        self.subMachines = subMachines
        for subMachine in subMachines:
            assert subMachine.getMoveRepresentation() is moveRepresentation
        ChessMachine.__init__(self, moveRepresentation=moveRepresentation)

    def decideEngine(self, board: IBoard) -> ChessMachine:
        raise NotImplementedError

    def computeBestMove(self, board: IBoard) -> IChessMachineResult:
        engine = self.decideEngine(board=board)
        return engine.computeBestMove(board=board)

