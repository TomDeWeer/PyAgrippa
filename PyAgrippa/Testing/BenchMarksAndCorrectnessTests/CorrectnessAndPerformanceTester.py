import time
from typing import List
from tabulate import tabulate
from PyAgrippa.AI.AI import ChessMachine
from PyAgrippa.Testing.BenchMarksAndCorrectnessTests.CorrectnessAndPerformanceTest import CorrectnessAndPerformanceTest
from PyAgrippa.Testing.BenchMarksAndCorrectnessTests.TestCollection import CorrectnessAndPerformanceTestCollection


class CorrectnessAndPerformanceTester:
    def __init__(self, verbose: bool = True, log: bool = True):
        self.verbose = verbose
        self.log = log
        assert not log, "Logging not yet implemented."

    def process(self, machine: ChessMachine, test: CorrectnessAndPerformanceTest):
        board = test.getBoard()
        if self.verbose:
            print(f"Testing {test} ...")
        tic = time.time()
        result = machine.computeBestMove(board)
        toc = time.time()
        # todo: == checker between moves
        msg = f"Move found (in {toc - tic: .2f}s): {machine.getMoveRepresentation().toStr(result.getBestMove())}."
        if test.getCorrectMove() is not None:
              msg += f"\nCorrect move: {test.getCorrectMove()}."
        if self.verbose:
            print(msg)

    def processCollection(self, machine: ChessMachine, collection: CorrectnessAndPerformanceTestCollection):
        tic = time.time()
        for test in collection.getTests():
            self.process(test=test, machine=machine)
        toc = time.time()
        print(f"Collection tested in {toc-tic:.2f}s.")

    def compareEngineSpeeds(self, collection: CorrectnessAndPerformanceTestCollection, machines: List[ChessMachine]):
        tests = collection.getTests()
        allTimes = []
        for machine in machines:
            if self.verbose:
                print(f"Testing {machine} ...")
            machineTimes = [str(machine), ]
            totalTic = time.time()
            for test in tests:
                board = test.getBoard()
                tic = time.time()
                result = machine.computeBestMove(board)
                toc = time.time()
                compTime = toc - tic
                machineTimes.append(compTime)
            totalToc = time.time()
            machineTimes.append(totalToc - totalTic)
            allTimes.append(machineTimes)

        # create header
        head = [test.name for test in tests]
        head.append('Total')

        # display table
        print(tabulate(allTimes, headers=head, tablefmt="grid"))
