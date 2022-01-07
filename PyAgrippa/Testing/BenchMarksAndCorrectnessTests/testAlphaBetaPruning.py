import time

from PyAgrippa.AI.AlphaBeta.AlphaBetaPruner import AlphaBetaPruner
from PyAgrippa.Boards.SCPSBoard import BoardSCPS
from PyAgrippa.Evaluation.BoardEvaluatorViaPieces import BoardEvaluatorViaPieces
from PyAgrippa.Moves.MoveGeneration.AllMoveGenerator import AllMoveGenerator
from PyAgrippa.Moves.OOPMoveRepresentation.OOPMoveRepresentation import OOPMoveRepresentation

if __name__ == '__main__':
    board = BoardSCPS()
    board.setInitialSetup()
    depth = 8
    representation = OOPMoveRepresentation()
    AI = AlphaBetaPruner(depth=depth, moveGenerator=AllMoveGenerator(moveRepresentation=representation),
                         boardEvaluator=BoardEvaluatorViaPieces())
    tic = time.time()
    result = AI.computeBestMove(board)
    toc = time.time()
    print(f"Best move = {representation.toStr(result.getBestMove())} with evaluation {representation.toStr(result.getEvaluation())}. "
          f"Found in {toc - tic:.2f}s.")