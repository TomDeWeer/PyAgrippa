from typing import Optional

from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Moves.MoveRepresentation import IMoveRepresentation
from PyAgrippa.Moves.OOPMoveRepresentation.Move import IMove


class CorrectnessAndPerformanceTest:
    #  todo: expand options for preferred machine or something
    def __init__(self, board: IBoard, moveRepresentation: IMoveRepresentation,
                 correctMove: Optional[IMove],
                 name: Optional[str] = None
                 ):
        self.correctMove = correctMove
        self.board = board
        self.name = name
        self.moveRepresentation = moveRepresentation

    def __str__(self):
        return self.name if self.name is not None else ""

    def getBoard(self) -> IBoard:
        return self.board

    def getCorrectMove(self) -> Optional[IMove]:
        return self.correctMove


