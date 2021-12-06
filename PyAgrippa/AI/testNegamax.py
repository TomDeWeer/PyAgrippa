import time

from PyAgrippa.AI.Negamax import Negamax
from PyAgrippa.Boards.SCPSBoard import BoardSCPS
from PyAgrippa.Evaluation.BoardEvaluatorViaPieces import BoardEvaluatorViaPieces
from PyAgrippa.Moves.MoveGenerator import MoveGenerator
from PyAgrippa.Moves.OOPMoveRepresentation.OOPMoveRepresentation import OOPMoveRepresentation

if __name__ == '__main__':

    board = BoardSCPS()
    board.setInitialSetup()
    board.setEvaluator(evaluator=BoardEvaluatorViaPieces(board=board))
    AI = Negamax(depth=5, moveGenerator=MoveGenerator(moveRepresentation=OOPMoveRepresentation()))
    tic = time.time()
    print(AI.getBestMove(board))
    toc = time.time()
    print(f"Best move found in {toc-tic:.2f}s.")

