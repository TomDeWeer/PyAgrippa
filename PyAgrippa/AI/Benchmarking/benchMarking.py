import time

from PyAgrippa.AI.Benchmarking.Benchmarker import Benchmarker
from PyAgrippa.AI.Benchmarking.Benchmarks import BenchmarkCollection
from PyAgrippa.AI.Negamax import Negamax
from PyAgrippa.Boards.SCPSBoard import BoardSCPS
from PyAgrippa.Evaluation.BoardEvaluatorViaPieces import BoardEvaluatorViaPieces
from PyAgrippa.Moves.MoveGenerator import MoveGenerator
from PyAgrippa.Moves.OOPMoveRepresentation.OOPMoveRepresentation import OOPMoveRepresentation

if __name__ == '__main__':

    benchMarker = Benchmarker(log=False, verbose=True)
    collection = BenchmarkCollection()
    collection.collectAll()
    benchMarker.processCollection(collection=collection)

