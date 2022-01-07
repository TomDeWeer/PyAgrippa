from PyAgrippa.AI.AlphaBeta.AlphaBetaPruner import AlphaBetaPruner
from PyAgrippa.AI.CompositeAIs.ErrorBasedCompositeEngine import ErrorBasedCompositeEngine
from PyAgrippa.AI.OpeningBookExplorer import OpeningBookExplorer
from PyAgrippa.Boards.SCPSBoard import BoardSCPS
from PyAgrippa.Evaluation.BoardEvaluatorViaPieces import BoardEvaluatorViaPieces
from PyAgrippa.Evaluation.CompositeBoardEvaluator import CompositeBoardEvaluator
from PyAgrippa.Evaluation.PositionalBoardEvaluator import PositionalBoardEvaluator
from PyAgrippa.Games.EngineComparer import EngineComparer
from PyAgrippa.Moves.MoveGeneration.CaptureGenerator import CaptureGenerator
from PyAgrippa.Moves.MoveGeneration.CompositeMoveGenerator import CompositeMoveGenerator
from PyAgrippa.Moves.MoveGeneration.KillerMoveStrategy import LAST_N
from PyAgrippa.Moves.MoveGeneration.NonCaptureGenerator import NonCaptureGenerator
from PyAgrippa.Moves.OOPMoveRepresentation.OOPMoveRepresentation import OOPMoveRepresentation
from PyAgrippa.Squares.SquareRepresentor import Square0X88Representor

if __name__ == '__main__':
    representation = OOPMoveRepresentation()
    moveGen1 = CompositeMoveGenerator([CaptureGenerator(moveRepresentation=representation, useMVV=False, useLVA=False),
                                       NonCaptureGenerator(moveRepresentation=representation)],
                                      killerMoveStrategy=LAST_N(N=2))
    alphaBetaPruner1 = AlphaBetaPruner(depth=3,
                                       useIncremental=True,
                                       moveGenerator=moveGen1,
                                       boardEvaluator=CompositeBoardEvaluator(
                                           evaluators=[BoardEvaluatorViaPieces(), PositionalBoardEvaluator()]))

    openingBookExplorer1 = OpeningBookExplorer(moveRepresentation=representation, verbose=False)

    machine1 = ErrorBasedCompositeEngine(subMachines=[openingBookExplorer1, alphaBetaPruner1],
                                         moveRepresentation=representation)
    machine1.setName('PyAgrippa1')

    moveGen2 = CompositeMoveGenerator([CaptureGenerator(moveRepresentation=representation, useMVV=False, useLVA=False),
                                       NonCaptureGenerator(moveRepresentation=representation)],
                                      killerMoveStrategy=LAST_N(N=2))
    alphaBetaPruner2 = AlphaBetaPruner(depth=4,
                                       useIncremental=True,
                                       moveGenerator=moveGen2,
                                       boardEvaluator=CompositeBoardEvaluator(
                                           evaluators=[BoardEvaluatorViaPieces(), PositionalBoardEvaluator()]))

    openingBookExplorer2 = OpeningBookExplorer(moveRepresentation=representation, verbose=False)

    machine2 = ErrorBasedCompositeEngine(subMachines=[openingBookExplorer2, alphaBetaPruner2],
                                         moveRepresentation=representation)
    machine2.setName('PyAgrippa2')

    # board = BoardSCPS().fromFEN(fen=r"rnb1kb1r/ppp1pppp/5n2/8/6q1/2N2N2/PPPPBPPP/R1BQK2R w KQkq - 6 6",
    #                             squareRepresentor=Square0X88Representor())
    board = BoardSCPS(squareRepresentor=Square0X88Representor()).setInitialSetup()
    comparer = EngineComparer(board=board, engine1=machine1, engine2=machine2)
    comparer.compare()

