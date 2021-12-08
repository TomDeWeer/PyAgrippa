import time

from PyAgrippa.AI.AI import ChessMachine
from PyAgrippa.AI.Benchmarking.Benchmarks import Benchmark, BenchmarkCollection
from PyAgrippa.AI.CorrectnessTests.CorrectnessTest import CorrectnessTest, CorrectnessTestCollection


class CorrectnessTester:
    def __init__(self, verbose: bool = True, log: bool = True):
        self.verbose = verbose
        self.log = log
        assert not log, "Logging not yet implemented."

    def process(self, machine: ChessMachine, test: CorrectnessTest):
        board = test.getBoard()
        if self.verbose:
            print(f"Testing...")
        tic = time.time()
        result = machine.computeBestMove(board)
        toc = time.time()
        # if result.getBestMove() == test.getCorrectMove():
        #     msg = f"Best move found ({test.getCorrectMove()})."
        # else:
        #     msg = f"Best move NOT found: {result.getBestMove()} is not {test.getCorrectMove()}."  # todo: == checker between moves
        msg = f"Move found (in {toc - tic: .2f}s): {result.getBestMove()}. \n" \
              f"Correct move: {test.getCorrectMove()}."

        if self.verbose:
            print(msg)

    def processCollection(self, machine: ChessMachine, collection: CorrectnessTestCollection):
        for test in collection.getTests():
            self.process(test=test, machine=machine)
