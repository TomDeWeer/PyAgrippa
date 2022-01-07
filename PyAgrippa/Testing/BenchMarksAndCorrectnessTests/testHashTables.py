import time

from PyAgrippa.AI.AlphaBeta.AlphaBetaPruner import AlphaBetaPruner
from PyAgrippa.Boards.SCPSBoard import BoardSCPS
from PyAgrippa.Evaluation.BoardEvaluatorViaPieces import BoardEvaluatorViaPieces
from PyAgrippa.Moves.MoveGeneration.AllMoveGenerator import AllMoveGenerator
from PyAgrippa.Moves.MoveGeneration.CaptureGenerator import CaptureGenerator
from PyAgrippa.Moves.MoveGeneration.CompositeMoveGenerator import CompositeMoveGenerator
from PyAgrippa.Moves.MoveGeneration.NonCaptureGenerator import NonCaptureGenerator
from PyAgrippa.Moves.OOPMoveRepresentation.OOPMoveRepresentation import OOPMoveRepresentation

if __name__ == '__main__':
    board = BoardSCPS()
    board.setInitialSetup()
    depth = 6
    representation = OOPMoveRepresentation()
    moveGen = CompositeMoveGenerator([CaptureGenerator(moveRepresentation=representation, useMVV=False, useLVA=False),
                                      NonCaptureGenerator(moveRepresentation=representation)], killerMoveStrategy=None)
    AI = AlphaBetaPruner(depth=depth, moveGenerator=moveGen,
                         boardEvaluator=BoardEvaluatorViaPieces(),
                         hashTableOptions={})
    tic = time.time()
    result = AI.computeBestMove(board)
    toc = time.time()
    print(
        f"Best move = {representation.toStr(result.getBestMove())} with evaluation {representation.toStr(result.getEvaluation())}. "
        f"Found in {toc - tic:.2f}s.")
    print(f'Visited {len(AI.hashTable)} nodes!')
