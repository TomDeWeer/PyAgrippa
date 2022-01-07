from PyAgrippa.AI.AI import ChessMachine
from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Games.Player.Player import Player
from PyAgrippa.Moves.MoveGeneration.AllMoveGenerator import AllMoveGenerator
from PyAgrippa.Moves.MoveRepresentation import IMoveRepresentation
from PyAgrippa.Moves.OOPMoveRepresentation.OOPMoveRepresentation import OOPMoveRepresentation


class MachinePlayer(Player):
    def __init__(self, machine: ChessMachine):
        self.machine = machine

    def __str__(self):
        return str(self.machine)

    def decideMove(self, board: IBoard):
        result = self.machine.computeBestMove(board=board)
        move = result.getBestMove()
        return move

    def getMoveRepresentation(self) -> IMoveRepresentation:
        return self.machine.getMoveRepresentation()
