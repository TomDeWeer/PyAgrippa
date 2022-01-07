from PyAgrippa.AI.AlphaBeta.AlphaBetaPruner import AlphaBetaPruner
from PyAgrippa.Evaluation.BoardEvaluatorViaPieces import BoardEvaluatorViaPieces
from PyAgrippa.Moves.MoveGeneration.CaptureGenerator import CaptureGenerator
from PyAgrippa.Moves.MoveGeneration.CompositeMoveGenerator import CompositeMoveGenerator
from PyAgrippa.Moves.MoveGeneration.NonCaptureGenerator import NonCaptureGenerator
from PyAgrippa.Moves.OOPMoveRepresentation.OOPMoveRepresentation import OOPMoveRepresentation
from PyAgrippa.Testing.BenchMarksAndCorrectnessTests.CorrectnessAndPerformanceTester import \
    CorrectnessAndPerformanceTester
from PyAgrippa.Testing.BenchMarksAndCorrectnessTests.TestCollection import CorrectnessAndPerformanceTestCollection

if __name__ == '__main__':
    tester = CorrectnessAndPerformanceTester(log=False, verbose=True)
    collection = CorrectnessAndPerformanceTestCollection()
    collection.collectAll()
    representation = OOPMoveRepresentation()
    moveGen = CompositeMoveGenerator([CaptureGenerator(moveRepresentation=representation, useMVV=False, useLVA=False),
                                      NonCaptureGenerator(moveRepresentation=representation)])

    machine1 = AlphaBetaPruner(depth=6,
                               useIncremental=True,
                               moveGenerator=moveGen,
                               boardEvaluator=BoardEvaluatorViaPieces())
    machine1.setName('Incremental')
    machine2 = AlphaBetaPruner(depth=5,
                               useIncremental=False,
                               moveGenerator=moveGen,
                               boardEvaluator=BoardEvaluatorViaPieces())
    machine2.setName('Non-incremental')
    machines = [machine1, machine2]
    # tester.processCollection(machine=machine1, collection=collection)
    tester.processCollection(machine=machine2, collection=collection)
    # tester.compareEngineSpeeds(collection=collection, machines=machines)
