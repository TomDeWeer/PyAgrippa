import time

from PyAgrippa.AI.AlphaBetaPruner import AlphaBetaPruner
from PyAgrippa.AI.Benchmarking.Benchmarker import Benchmarker
from PyAgrippa.AI.Benchmarking.Benchmarks import BenchmarkCollection
from PyAgrippa.AI.CorrectnessTests.CorrectnessTest import CorrectnessTestCollection
from PyAgrippa.AI.CorrectnessTests.CorrectnessTester import CorrectnessTester
from PyAgrippa.AI.Negamax import Negamax
from PyAgrippa.Boards.SCPSBoard import BoardSCPS
from PyAgrippa.Evaluation.BoardEvaluatorViaPieces import BoardEvaluatorViaPieces
from PyAgrippa.Moves.MoveGenerator import MoveGenerator
from PyAgrippa.Moves.OOPMoveRepresentation.OOPMoveRepresentation import OOPMoveRepresentation

if __name__ == '__main__':

    tester = CorrectnessTester(log=False, verbose=True)
    collection = CorrectnessTestCollection()
    collection.collectAll()
    tester.processCollection(collection=collection,
                             machine=AlphaBetaPruner(depth=5,
                                                     useIncremental=True,
                                                     moveGenerator=MoveGenerator(moveRepresentation=OOPMoveRepresentation()),
                                boardEvaluator=BoardEvaluatorViaPieces()))

