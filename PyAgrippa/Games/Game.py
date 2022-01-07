from typing import List

from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.GUI.BoardRenderer import BoardRenderer
from PyAgrippa.Games.Outcome import Outcome
from PyAgrippa.Games.Player import Player
from PyAgrippa.Games.TimeControl import TimeControl


class Game:
    """
    Class for playing a game of chess. It lets each player move sequentially and applies and stores their selected moves.
    """
    def __init__(self, board: IBoard, whitePlayer: Player, blackPlayer: Player, timeControl: TimeControl = None,
                 attachGUI: bool = True, verbose: int = 3):
        # todo: decouple board representation here from the one used in the chess machine!
        self.board = board
        self.whitePlayer = whitePlayer
        self.blackPlayer = blackPlayer
        self.timeControl = timeControl
        self.verbose = verbose
        self.movesPlayed: List[str] = []
        if attachGUI:
            renderer = BoardRenderer(initialBoard=board)
            renderer.start()
            renderer.show()
            self.gui = renderer
        else:
            self.gui = None

    def getActivePlayer(self) -> Player:
        if self.board.isWhiteToMove():
            return self.whitePlayer
        else:
            return self.blackPlayer

    def checkRepetition(self):
        moves = self.movesPlayed
        if len(moves) < 12:
            return False
        else:
            moves1 = moves[-1:-13:-2]
            moves2 = moves[-2:-14:-2]
            return len(set(moves1)) == 2 and len(set(moves2)) == 2

    def play(self):
        # todo: implement actual legal move checking and proper end of game verification
        while not (self.board.isGameOver() or self.checkRepetition()):
            activePlayer = self.getActivePlayer()
            move = activePlayer.decideMove(self.board)
            self.movesPlayed.append(activePlayer.getMoveRepresentation().toUCI(move))
            if self.verbose >= 3:
                print(f"{activePlayer} moves {move}.")
            activePlayer.getMoveRepresentation().applyMove(move)
            if self.gui is not None:
                self.gui.refresh()
        if self.board.whiteKingTaken():
            if self.verbose >= 1:
                print("Black wins!")
            outcome = Outcome.BLACK_WINS
        elif self.board.blackKingTaken():
            if self.verbose >= 1:
                print("White wins!")
            outcome = Outcome.WHITE_WINS
        else:
            if self.verbose >= 1:
                print('Draw!')
            outcome = Outcome.DRAW
        if self.gui is not None:
            self.gui.waitForUserExit()
        return outcome


