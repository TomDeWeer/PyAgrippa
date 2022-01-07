from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Moves.MoveRepresentation import IMoveRepresentation


class Player:
    def decideMove(self, board: IBoard):
        raise NotImplementedError

    def getMoveRepresentation(self) -> IMoveRepresentation:
        raise NotImplementedError

