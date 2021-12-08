import time

from PyAgrippa.AI.AlphaBetaPruner import AlphaBetaPruner
from PyAgrippa.AI.Negamax import Negamax
from PyAgrippa.Boards.SCPSBoard import BoardSCPS
from PyAgrippa.Evaluation.BoardEvaluatorViaPieces import BoardEvaluatorViaPieces
from PyAgrippa.Moves.MoveGenerator import MoveGenerator
from PyAgrippa.Moves.OOPMoveRepresentation.OOPMoveRepresentation import OOPMoveRepresentation

if __name__ == '__main__':
    board = BoardSCPS()
    board.setInitialSetup()
    depth = 8
    AI = AlphaBetaPruner(depth=depth, moveGenerator=MoveGenerator(moveRepresentation=OOPMoveRepresentation()),
                         boardEvaluator=BoardEvaluatorViaPieces())
    tic = time.time()
    result = AI.computeBestMove(board)
    toc = time.time()
    print(f"Best move = {result.getBestMove()} with evaluation {result.getEvaluation()}. "
          f"Found in {toc - tic:.2f}s.")