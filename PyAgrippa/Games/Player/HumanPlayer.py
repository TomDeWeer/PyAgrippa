from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Games.Player.Player import Player
from PyAgrippa.Moves.MoveGeneration.AllMoveGenerator import AllMoveGenerator
from PyAgrippa.Moves.MoveRepresentation import IMoveRepresentation
from PyAgrippa.Moves.OOPMoveRepresentation.OOPMoveRepresentation import OOPMoveRepresentation


class HumanPlayer(Player):
    def __init__(self, name: str):
        self.name = name
        self.moveGenerator = AllMoveGenerator(OOPMoveRepresentation())

    def __str__(self):
        return self.name

    def decideMove(self, board: IBoard):
        while True:
            while True:
                try:
                    startSquare = board.getSquareViaStr(square=input('Start square: '))
                    break
                except (ValueError, IndexError):
                    print('Invalid square.')
            while True:
                try:
                    endSquare = board.getSquareViaStr(square=input('End square: '))
                    break
                except (ValueError, IndexError):
                    print('Invalid square.')
            move = None
            possibleMoves = list(self.moveGenerator.generatePseudoLegalMoves(board=board))
            for possibleMove in possibleMoves:
                if self.getMoveRepresentation().getStartingSquare(possibleMove) == startSquare and \
                        self.getMoveRepresentation().getEndingSquare(possibleMove) == endSquare:
                    move = possibleMove
                    break
            if move is None:
                print('Invalid move.')
            else:
                break
        return move

    def getMoveRepresentation(self) -> IMoveRepresentation:
        return self.moveGenerator.getRepresentation()
