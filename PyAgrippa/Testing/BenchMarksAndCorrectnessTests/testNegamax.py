import time

from PyAgrippa.AI.Negamax import Negamax
from PyAgrippa.Boards.SCPSBoard import BoardSCPS
from PyAgrippa.Evaluation.BoardEvaluatorViaPieces import BoardEvaluatorViaPieces
from PyAgrippa.Moves.MoveGeneration.AbstractMoveGenerator import AbstractMoveGenerator
from PyAgrippa.Moves.MoveGeneration.AllMoveGenerator import AllMoveGenerator
from PyAgrippa.Moves.OOPMoveRepresentation.OOPMoveRepresentation import OOPMoveRepresentation

if __name__ == '__main__':

    board = BoardSCPS()
    board.setInitialSetup()
    depth = 4
    AI = Negamax(depth=depth, moveGenerator=AllMoveGenerator(moveRepresentation=OOPMoveRepresentation()),
                 boardEvaluator=BoardEvaluatorViaPieces())
    tic = time.time()
    print(AI.computeBestMove(board))
    toc = time.time()
    print(f"Best move found in {toc-tic:.2f}s.")

