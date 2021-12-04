from Boards.Board import IBoard
from Evaluation.BoardEvaluator import BoardEvaluator
from Pieces.Bishop import IBishop
from Pieces.King import IKing
from Pieces.Knight import IKnight
from Pieces.Pawn import IPawn
from Pieces.Queen import IQueen
from Pieces.Rook import IRook


class BoardEvaluatorViaPieces(BoardEvaluator):
    """
    Very basic board evaluator. Loops through the piece objects (not identifiers) and sums their values.
    """
    def __init__(self, board: IBoard):
        BoardEvaluator.__init__(self, board=board)

    def evaluate(self):
        score = 0.
        for piece in self.getBoard().getActivePieces():
             score += piece.getEvaluation()
        for piece in self.getBoard().getInactivePieces():
            score -= piece.getEvaluation()
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


