from PyAgrippa.AI.AlphaBeta.AlphaBetaPruner import AlphaBetaPruner
from PyAgrippa.Testing.BenchMarksAndCorrectnessTests.TestCollection import CorrectnessAndPerformanceTestCollection
from PyAgrippa.Testing.BenchMarksAndCorrectnessTests.CorrectnessAndPerformanceTester import CorrectnessAndPerformanceTester
from PyAgrippa.Evaluation.BoardEvaluatorViaPieces import BoardEvaluatorViaPieces
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
    moveGen1 = CompositeMoveGenerator([CaptureGenerator(moveRepresentation=representation, useMVV=False, useLVA=False),
                                       NonCaptureGenerator(moveRepresentation=representation)], killerMoveStrategy=None)
    moveGen2 = CompositeMoveGenerator([CaptureGenerator(moveRepresentation=representation, useMVV=False, useLVA=False),
                                       NonCaptureGenerator(moveRepresentation=representation)],
                                      killerMoveStrategy=LAST_N(N=1))
    moveGen3 = CompositeMoveGenerator([CaptureGenerator(moveRepresentation=representation, useMVV=False, useLVA=False),
                                       NonCaptureGenerator(moveRepresentation=representation)],
                                      killerMoveStrategy=LAST_N(N=2))
    moveGen4 = CompositeMoveGenerator([CaptureGenerator(moveRepresentation=representation, useMVV=False, useLVA=False),
                                       NonCaptureGenerator(moveRepresentation=representation)],
                                      killerMoveStrategy=LAST_N(N=3))
    machine1 = AlphaBetaPruner(depth=6,
                               useIncremental=True,
                               moveGenerator=moveGen1,
                               boardEvaluator=BoardEvaluatorViaPieces())
    machine1.setName('No killer moves')
    machine2 = AlphaBetaPruner(depth=6,
                               useIncremental=True,
                               moveGenerator=moveGen2,
                               boardEvaluator=BoardEvaluatorViaPieces())
    machine2.setName('LAST_1')
    machine3 = AlphaBetaPruner(depth=6,
                               useIncremental=True,
                               moveGenerator=moveGen3,
                               boardEvaluator=BoardEvaluatorViaPieces())
    machine3.setName('LAST_2')
    machine4 = AlphaBetaPruner(depth=6,
                               useIncremental=True,
                               moveGenerator=moveGen4,
                               boardEvaluator=BoardEvaluatorViaPieces())
    machine4.setName('LAST_3')
    machines = [machine1, machine2, machine3, machine4]
    tester.compareEngineSpeeds(collection=collection, machines=machines)
    # tester.processCollection(collection=collection, machine=machine2)