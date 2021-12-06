from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Evaluation.BoardEvaluator import BoardEvaluator
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
    def __init__(self, board: IBoard):
        BoardEvaluator.__init__(self, board=board)

    def evaluate(self):
        score = 0.
        for piece in self.getBoard().getActivePieces():
             score += piece.evaluate()
        for piece in self.getBoard().getInactivePieces():
            score -= piece.evaluate()
        return score

    def evaluatePawn(self, pawn: IPawn):
        return 1.

    def evaluateKnight(self, knight: IKnight):
        return 3.

    def evaluateBishop(self, bishop: IBishop):
        return 3.5

    def evaluateRook(self, rook: IRook):
        return 5.

    def evaluateQueen(self, queen: IQueen):
        return 9.

    def evaluateKing(self, king: IKing):
        return 1000.

    def supportsIncrementalCalculation(self) -> bool:
        return False


