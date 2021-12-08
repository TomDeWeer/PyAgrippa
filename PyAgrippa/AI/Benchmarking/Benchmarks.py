from typing import List

from PyAgrippa.AI.AI import ChessMachine
from PyAgrippa.AI.AlphaBetaPruner import AlphaBetaPruner
from PyAgrippa.AI.Negamax import Negamax
from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Boards.SCPSBoard import BoardSCPS
from PyAgrippa.Evaluation.BoardEvaluatorViaPieces import BoardEvaluatorViaPieces
from PyAgrippa.Moves.MoveGenerator import MoveGenerator
from PyAgrippa.Moves.OOPMoveRepresentation.OOPMoveRepresentation import OOPMoveRepresentation


class Benchmark:
    def __init__(self, board: IBoard, machine: ChessMachine):
        self.machine = machine
        self.board = board

    def getBoard(self) -> IBoard:
        return self.board

    def getAI(self) -> ChessMachine:
        return self.machine


class BenchmarkCollection:
    def __init__(self):
        self.benchmarks = []

    def getBenchmarks(self) -> List[Benchmark]:
        return self.benchmarks

    def collectFromCombinations(self, boards: List[IBoard], machines: List[ChessMachine]):
        for board in boards:
            for machine in machines:
                self.benchmarks.append(Benchmark(board=board, machine=machine))

    def collectAll(self):
        boards = [BoardSCPS().setInitialSetup()]
        machines = []
        for depth in [2, 3, 4]:
            machines.append(
                Negamax(depth=depth, moveGenerator=MoveGenerator(moveRepresentation=OOPMoveRepresentation()),
                        boardEvaluator=BoardEvaluatorViaPieces()))
            machines.append(
                AlphaBetaPruner(depth=depth, moveGenerator=MoveGenerator(moveRepresentation=OOPMoveRepresentation()),
                                boardEvaluator=BoardEvaluatorViaPieces()))
        self.collectFromCombinations(boards=boards, machines=machines)
