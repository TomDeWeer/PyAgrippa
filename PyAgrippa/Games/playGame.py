from PyAgrippa.AI.AlphaBeta.AlphaBetaPruner import AlphaBetaPruner
from PyAgrippa.Boards.SCPSBoard import BoardSCPS
from PyAgrippa.Evaluation.BoardEvaluatorViaPieces import BoardEvaluatorViaPieces
from PyAgrippa.Evaluation.CompositeBoardEvaluator import CompositeBoardEvaluator
from PyAgrippa.Evaluation.PositionalBoardEvaluator import PositionalBoardEvaluator
from PyAgrippa.Games.Game import Game
from PyAgrippa.Games.Player.HumanPlayer import HumanPlayer
from PyAgrippa.Games.Player.MachinePlayer import MachinePlayer
from PyAgrippa.Moves.MoveGeneration.CaptureGenerator import CaptureGenerator
from PyAgrippa.Moves.MoveGeneration.CompositeMoveGenerator import CompositeMoveGenerator
from PyAgrippa.Moves.MoveGeneration.KillerMoveStrategy import LAST_N
from PyAgrippa.Moves.MoveGeneration.NonCaptureGenerator import NonCaptureGenerator
from PyAgrippa.Moves.OOPMoveRepresentation.OOPMoveRepresentation import OOPMoveRepresentation
from PyAgrippa.Squares.SquareRepresentor import Square0X88Representor

if __name__ == '__main__':
    player1 = HumanPlayer(name='Tom')

    representation = OOPMoveRepresentation()
    moveGen = CompositeMoveGenerator([CaptureGenerator(moveRepresentation=representation, useMVV=False, useLVA=False),
                                      NonCaptureGenerator(moveRepresentation=representation)],
                                     killerMoveStrategy=LAST_N(N=2))
    machine = AlphaBetaPruner(depth=6,
                              useIncremental=True,
                              moveGenerator=moveGen,
                              boardEvaluator=CompositeBoardEvaluator(
                                  evaluators=[BoardEvaluatorViaPieces(), PositionalBoardEvaluator()]))
    machine.setName('PyAgrippa')
    player2 = MachinePlayer(machine=machine)

    board = BoardSCPS().fromFEN(fen=r"rnb1kb1r/ppp1pppp/5n2/8/6q1/2N2N2/PPPPBPPP/R1BQK2R w KQkq - 6 6",
                                squareRepresentor=Square0X88Representor())

    game = Game(whitePlayer=player1, blackPlayer=player2, board=board, attachGUI=True)

    game.play()
