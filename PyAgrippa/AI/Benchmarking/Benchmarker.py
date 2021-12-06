import time

from PyAgrippa.AI.Benchmarking.Benchmarks import Benchmark, BenchmarkCollection


class Benchmarker:
    def __init__(self, verbose: bool = True, log: bool = True):
        self.verbose = verbose
        self.log = log
        assert not log, "Logging not yet implemented."

    def process(self, benchMark: Benchmark):
        machine = benchMark.getAI()
        board = benchMark.getBoard()
        if self.verbose:
            print(f"Benchmarking {board} with {machine}.")
        tic = time.time()
        print(machine.getBestMove(board))
        toc = time.time()
        if self.verbose:
            print(f"Best move found in {toc - tic:.2f}s.")

    def processCollection(self, collection: BenchmarkCollection):
        for benchMark in collection.getBenchmarks():
            self.process(benchMark)