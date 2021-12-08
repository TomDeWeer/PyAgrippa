from typing import List

from PyAgrippa.AI.AI import ChessMachine
from PyAgrippa.AI.AlphaBetaPruner import AlphaBetaPruner
from PyAgrippa.AI.Negamax import Negamax
from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Boards.SCPSBoard import BoardSCPS
from PyAgrippa.Evaluation.BoardEvaluatorViaPieces import BoardEvaluatorViaPieces
from PyAgrippa.Moves.MoveGenerator import MoveGenerator
from PyAgrippa.Moves.MoveRepresentation import IMoveRepresentation
from PyAgrippa.Moves.OOPMoveRepresentation.Move import IMove
from PyAgrippa.Moves.OOPMoveRepresentation.OOPMoveRepresentation import OOPMoveRepresentation
from PyAgrippa.Squares.SquareRepresentor import Square0X88Representor


class CorrectnessTest:
    def __init__(self, board: IBoard, moveRepresentation: IMoveRepresentation, correctMove: IMove):
        self.correctMove = correctMove
        self.board = board
        self.moveRepresentation = moveRepresentation

    def getBoard(self) -> IBoard:
        return self.board

    def getCorrectMove(self) -> IMove:
        return self.correctMove


class CorrectnessTestCollection:
    def __init__(self):
        self.tests = []

    def getTests(self) -> List[CorrectnessTest]:
        return self.tests

    # def collectFromCombinations(self, boards: List[IBoard], moves: List[IMove]):
    #     for board in boards:
    #         for move in moves:
    #             self.tests.append(CorrectnessTest(board=board, correctMove=move))

    def collectAll(self):
        board = BoardSCPS.fromFEN(r"6rk/pp6/5P2/3p3N/8/5n1b/PP3P1P/R2R3K b - - 7 28",
                                  squareRepresentor=Square0X88Representor())
        moveRepresentation = OOPMoveRepresentation()
        start = board.getSquareAt(file=7, rank=2)
        end = board.getSquareAt(file=6, rank=1)
        move = moveRepresentation.generateMove(board=board, piece=board.getPieceOn(start), start=start, end=end, )
        self.tests.append(CorrectnessTest(board=board,
                                          correctMove=move,
                                          moveRepresentation=moveRepresentation))

