from typing import List

from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Evaluation.BoardEvaluator import BoardEvaluator
from PyAgrippa.Moves.MoveRepresentation import IMoveRepresentation
from PyAgrippa.Moves.OOPMoveRepresentation.Move import IMove
from PyAgrippa.Pieces.Bishop import IBishop
from PyAgrippa.Pieces.King import IKing
from PyAgrippa.Pieces.Knight import IKnight
from PyAgrippa.Pieces.Pawn import IPawn
from PyAgrippa.Pieces.Queen import IQueen
from PyAgrippa.Pieces.Rook import IRook


class CompositeBoardEvaluator(BoardEvaluator):
    def __init__(self, evaluators: List[BoardEvaluator]):
        self.evaluators = evaluators
        BoardEvaluator.__init__(self)

    def evaluate(self, board: IBoard):
        return sum([ev.evaluate(board) for ev in self.evaluators])

    def evaluatePawn(self, pawn: IPawn):
        return sum([ev.evaluatePawn(pawn) for ev in self.evaluators])

    def evaluateKnight(self, knight: IKnight):
        return sum([ev.evaluateKnight(knight) for ev in self.evaluators])

    def evaluateBishop(self, bishop: IBishop):
        return sum([ev.evaluateBishop(bishop) for ev in self.evaluators])

    def evaluateRook(self, rook: IRook):
        return sum([ev.evaluateRook(rook) for ev in self.evaluators])

    def evaluateQueen(self, queen: IQueen):
        return sum([ev.evaluateQueen(queen) for ev in self.evaluators])

    def evaluateKing(self, king: IKing):
        return sum([ev.evaluateKing(king) for ev in self.evaluators])

    def supportsIncrementalCalculation(self) -> bool:
        return all([ev.supportsIncrementalCalculation() for ev in self.evaluators])

    def initializeIncremental(self, board: IBoard, moveRepresentation: IMoveRepresentation):
        for ev in self.evaluators:
            ev.initializeIncremental(board=board, moveRepresentation=moveRepresentation)

    def getScore(self):
        return sum([ev.getScore() for ev in self.evaluators])

    def evaluateMove(self, move: IMove):
        for ev in self.evaluators:
            ev.evaluateMove(move=move)

    def undoLast(self):
        for ev in self.evaluators:
            ev.undoLast()

