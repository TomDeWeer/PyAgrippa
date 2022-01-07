from PyAgrippa.AI.AlphaBeta.AlphaBetaPruner import AlphaBetaPruner
from PyAgrippa.Testing.BenchMarksAndCorrectnessTests.TestCollection import CorrectnessAndPerformanceTestCollection
from PyAgrippa.Testing.BenchMarksAndCorrectnessTests.CorrectnessAndPerformanceTester import CorrectnessAndPerformanceTester
from PyAgrippa.Evaluation.BoardEvaluatorViaPieces import BoardEvaluatorViaPieces
from PyAgrippa.Evaluation.CompositeBoardEvaluator import CompositeBoardEvaluator
from PyAgrippa.Evaluation.PositionalBoardEvaluator import PositionalBoardEvaluator
from PyAgrippa.Moves.MoveGeneration.CaptureGenerator import CaptureGenerator
from PyAgrippa.Moves.MoveGeneration.CompositeMoveGenerator import CompositeMoveGenerator
from PyAgrippa.Moves.MoveGeneration.KillerMoveStrategy import LAST_N
from PyAgrippa.Moves.MoveGeneration.NonCaptureGenerator import NonCaptureGenerator
from PyAgrippa.Moves.OOPMoveRepresentation.OOPMoveRepresentation import OOPMoveRepresentation

if __name__ == '__main__':
    tester = CorrectnessAndPerformanceTester(log=False, verbose=True)
    collection = CorrectnessAndPerformanceTestCollection()
    collection.collectAll()
    representation = OOPMoveRepresentation()
    moveGen = CompositeMoveGenerator([CaptureGenerator(moveRepresentation=representation, useMVV=False, useLVA=False),
                                      NonCaptureGenerator(moveRepresentation=representation)],
                                     killerMoveStrategy=LAST_N(N=2))

    machine1 = AlphaBetaPruner(depth=6,
                               useIncremental=True,
                               moveGenerator=moveGen,
                               boardEvaluator=CompositeBoardEvaluator(
                                   evaluators=[BoardEvaluatorViaPieces(), PositionalBoardEvaluator()]))
    machine1.setName('With positional play')

    machine2 = AlphaBetaPruner(depth=6,
                               useIncremental=True,
                               moveGenerator=moveGen,
                               boardEvaluator=BoardEvaluatorViaPieces())
    machine2.setName('Without positional play')

    tester.compareEngineSpeeds(collection=collection, machines=[machine1, machine2])
