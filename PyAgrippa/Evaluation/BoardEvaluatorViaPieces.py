from typing import Optional

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


class BoardEvaluatorViaPieces(BoardEvaluator):
    """
    Very basic board evaluator. Loops through the piece objects (not identifiers) and sums their values.
    """
    def __init__(self):
        BoardEvaluator.__init__(self)
        self.deltas = None
        self.currentScore = None
        self.moveRepresentation: Optional[IMoveRepresentation] = None

    def evaluate(self, board: IBoard):
        score = 0.
        for piece in board.getActivePieces():
            score += piece.evaluate(self)
        for piece in board.getInactivePieces():
            score -= piece.evaluate(self)
        return score

    def evaluatePawn(self, pawn: IPawn):
        return 1.

    def evaluateKnight(self, knight: IKnight):
        return 3.

    def evaluateBishop(self, bishop: IBishop):
        return 3.25

    def evaluateRook(self, rook: IRook):
        return 5.

    def evaluateQueen(self, queen: IQueen):
        return 9.

    def evaluateKing(self, king: IKing):
        return 1000.

    def supportsIncrementalCalculation(self) -> bool:
        return True

    def initializeIncremental(self, board: IBoard, moveRepresentation: IMoveRepresentation):
        self.moveRepresentation = moveRepresentation
        self.currentScore = self.evaluate(board)
        self.deltas = []

    def getScore(self):
        """
        Evaluates how good the board is for the active player after all moves have been played (controllable with
        applyMove and undoLast).
        """
        return self.currentScore

    def applyMove(self, move: IMove):
        delta = 0.
        # captured piece
        capturedPiece = self.moveRepresentation.getCapturedPiece(move=move)
        if capturedPiece is not None:
            pieceEval = capturedPiece.evaluate(evaluator=self)
            delta += pieceEval
        # promotion
        promotedPiece = self.moveRepresentation.getPromotedPiece(move=move)
        if promotedPiece is not None:
            movingPiece = self.moveRepresentation.getMovingPiece(move=move)
            delta += promotedPiece.evaluate(self)
            delta += -movingPiece.evaluate(self)
        self.deltas.append(delta)
        self.currentScore += delta
        self.currentScore *= -1

    def undoLast(self):
        delta = self.deltas.pop(-1)
        self.currentScore *= -1
        self.currentScore -= delta


