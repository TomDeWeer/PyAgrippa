from PyAgrippa.AI.AlphaBeta.AlphaBetaPruner import AlphaBetaPruner
from PyAgrippa.Testing.BenchMarksAndCorrectnessTests.TestCollection import CorrectnessAndPerformanceTestCollection
from PyAgrippa.Testing.BenchMarksAndCorrectnessTests.CorrectnessAndPerformanceTester import CorrectnessAndPerformanceTester
from PyAgrippa.Evaluation.BoardEvaluatorViaPieces import BoardEvaluatorViaPieces
from PyAgrippa.Moves.MoveGeneration.CaptureGenerator import CaptureGenerator
from PyAgrippa.Moves.MoveGeneration.CompositeMoveGenerator import CompositeMoveGenerator
from PyAgrippa.Moves.MoveGeneration.NonCaptureGenerator import NonCaptureGenerator
from PyAgrippa.Moves.OOPMoveRepresentation.OOPMoveRepresentation import OOPMoveRepresentation

if __name__ == '__main__':

    tester = CorrectnessAndPerformanceTester(log=False, verbose=True)
    collection = CorrectnessAndPerformanceTestCollection()
    collection.collectAll()
    representation = OOPMoveRepresentation()
    moveGen1 = CompositeMoveGenerator([CaptureGenerator(moveRepresentation=representation, useMVV=False, useLVA=False),
                                       NonCaptureGenerator(moveRepresentation=representation)])
    moveGen2 = CompositeMoveGenerator([CaptureGenerator(moveRepresentation=representation, useMVV=True, useLVA=False),
                                       NonCaptureGenerator(moveRepresentation=representation)])
    moveGen3 = CompositeMoveGenerator([CaptureGenerator(moveRepresentation=representation, useMVV=False, useLVA=True),
                                       NonCaptureGenerator(moveRepresentation=representation)])
    moveGen4 = CompositeMoveGenerator([CaptureGenerator(moveRepresentation=representation, useMVV=True, useLVA=True),
                                       NonCaptureGenerator(moveRepresentation=representation)])
    print("Testing without MVV-LVA.")
    tester.processCollection(collection=collection,
                             machine=AlphaBetaPruner(depth=6,
                                                     useIncremental=True,
                                                     moveGenerator=moveGen1,
                                                     boardEvaluator=BoardEvaluatorViaPieces()))
    print("\n\nTesting with MVV")
    tester.processCollection(collection=collection,
                             machine=AlphaBetaPruner(depth=6,
                                                     useIncremental=True,
                                                     moveGenerator=moveGen2,
                                                     boardEvaluator=BoardEvaluatorViaPieces()))
    print("\n\nTesting with LVA.")
    tester.processCollection(collection=collection,
                             machine=AlphaBetaPruner(depth=6,
                                                     useIncremental=True,
                                                     moveGenerator=moveGen3,
                                                     boardEvaluator=BoardEvaluatorViaPieces()))
    print("\n\nTesting with MVV-LVA.")
    tester.processCollection(collection=collection,
                             machine=AlphaBetaPruner(depth=6,
                                                     useIncremental=True,
                                                     moveGenerator=moveGen4,
                                                     boardEvaluator=BoardEvaluatorViaPieces()))