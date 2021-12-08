import time

from PyAgrippa.AI.Negamax import Negamax
from PyAgrippa.Boards.SCPSBoard import BoardSCPS
from PyAgrippa.Evaluation.BoardEvaluatorViaPieces import BoardEvaluatorViaPieces
from PyAgrippa.Moves.MoveGenerator import MoveGenerator
from PyAgrippa.Moves.OOPMoveRepresentation.OOPMoveRepresentation import OOPMoveRepresentation

if __name__ == '__main__':

    board = BoardSCPS()
    board.setInitialSetup()
    depth = 4
    AI = Negamax(depth=depth, moveGenerator=MoveGenerator(moveRepresentation=OOPMoveRepresentation()),
                 boardEvaluator=BoardEvaluatorViaPieces())
    tic = time.time()
    print(AI.computeBestMove(board))
    toc = time.time()
    print(f"Best move found in {toc-tic:.2f}s.")

