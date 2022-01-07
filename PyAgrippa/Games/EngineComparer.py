from PyAgrippa.AI.AI import ChessMachine
from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Games.Game import Game
from PyAgrippa.Games.Outcome import Outcome
from PyAgrippa.Games.Player.MachinePlayer import MachinePlayer
from PyAgrippa.Games.TimeControl import TimeControl


class EngineComparer:
    def __init__(self, board: IBoard, engine1: ChessMachine, engine2: ChessMachine, nbGames: int = 100, timeControl: TimeControl = None):
        self.board = board
        self.engine1 = engine1
        self.engine2 = engine2
        self.timeControl = timeControl
        self.nbGames = nbGames

    def compare(self):
        engine1Wins = 0
        engine2Wins = 0
        draws = 0
        for i in range(self.nbGames):
            print(f'Playing game #{i+1}...')
            if i % 2 == 0:
                whiteEngine, blackEngine = self.engine1, self.engine2
            else:
                whiteEngine, blackEngine = self.engine2, self.engine1

            whitePlayer = MachinePlayer(machine=whiteEngine)
            blackPlayer = MachinePlayer(machine=blackEngine)

            game = Game(whitePlayer=whitePlayer, blackPlayer=blackPlayer, timeControl=self.timeControl, attachGUI=False,
                        board=self.board, verbose=2)

            outcome = game.play()
            if outcome is Outcome.DRAW:
                draws += 1
            elif outcome is Outcome.BLACK_WINS:
                if blackEngine is self.engine1:
                    engine1Wins += 1
                else:
                    engine2Wins += 1
            else:
                if whiteEngine is self.engine1:
                    engine1Wins += 1
                else:
                    engine2Wins += 1
            print(f'Score: ({draws}, {engine1Wins}, {engine2Wins}) = (#draws, #wins for {self.engine1}, #wins for {self.engine2})')
            self.board.clear()
            self.board.setInitialSetup()


