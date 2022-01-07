from typing import List, Optional, Any

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
from PyAgrippa.Squares.Square import ISquare


class PositionalBoardEvaluator(BoardEvaluator):
    """
    Positional ideas from https://www.chessprogramming.org/Simplified_Evaluation_Function.
    First things to be improved:
    * pawns!!!
    """

    def __init__(self):
        BoardEvaluator.__init__(self)
        self.deltas = None
        self.currentScore = None
        self.moveRepresentation: Optional[IMoveRepresentation] = None
        self.PAWN_EVAL_WHITE = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [50, 50, 50, 50, 50, 50, 50, 50],
            [10, 10, 20, 30, 30, 20, 10, 10],
            [5, 5, 10, 25, 25, 10, 5, 5],
            [0, 0, 0, 20, 20, 0, 0, 0],
            [5, -5, -10, 0, 0, -10, -5, 5],
            [5, 10, 10, -20, -20, 10, 10, 5],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]

        self.KNIGHT_EVAL_WHITE = [
            [-50, -40, -30, -30, -30, -30, -40, -50],
            [-40, -20, 0, 0, 0, 0, -20, -40],
            [-30, 0, 10, 15, 15, 10, 0, -30],
            [-30, 5, 15, 20, 20, 15, 5, -30],
            [-30, 0, 15, 20, 20, 15, 0, -30],
            [-30, 5, 10, 15, 15, 10, 5, -30],
            [-40, -20, 0, 5, 5, 0, -20, -40],
            [-50, -40, -30, -30, -30, -30, -40, -50],
        ]

        self.BISHOP_EVAL_WHITE = [
            [-20, -10, -10, -10, -10, -10, -10, -20],
            [-10, 0, 0, 0, 0, 0, 0, -10],
            [-10, 0, 5, 10, 10, 5, 0, -10],
            [-10, 5, 5, 10, 10, 5, 5, -10],
            [-10, 0, 10, 10, 10, 10, 0, -10],
            [-10, 10, 10, 10, 10, 10, 10, -10],
            [-10, 5, 0, 0, 0, 0, 5, -10],
            [-20, -10, -10, -10, -10, -10, -10, -20],
        ]

        self.ROOK_EVAL_WHITE = [   # todo: this is a bit silly
            [0, 0, 0, 0, 0, 0, 0, 0],
            [5, 10, 10, 10, 10, 10, 10, 5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [0, 0, 0, 5, 5, 0, 0, 0],
        ]

        self.QUEEN_EVAL_WHITE = [
            [-20, -10, -10, -5, -5, -10, -10, -20],
            [-10, 0, 0, 0, 0, 0, 0, -10],
            [-10, 0, 5, 5, 5, 5, 0, -10],
            [-5, 0, 5, 5, 5, 5, 0, -5],
            [0, 0, 5, 5, 5, 5, 0, -5],
            [-10, 5, 5, 5, 5, 5, 0, -10],
            [-10, 0, 5, 0, 0, 0, 0, -10],
            [-20, -10, -10, -5, -5, -10, -10, -20],
        ]

        self.KING_EVAL_WHITE = [  # todo: this actually depends on the state of the game (ending vs middlegame). I keep it mostly zero for now except that i encourage castling
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 30, 0, 0, 0, 0, 30, 0],
        ]

    def evaluatePosition(self, isWhite: bool, table: List[List[float]], square: ISquare):
        file = square.getFile()
        rank = square.getRank()
        if isWhite:
            firstIndex = 7 - rank
            secondIndex = file
        else:
            firstIndex = rank
            secondIndex = file
        return table[firstIndex][secondIndex]

    def evaluate(self, board: IBoard):
        score = 0.
        for piece in board.getActivePieces():
            score += piece.evaluateAt(self, square=piece.getSquare())
        for piece in board.getInactivePieces():
            score -= piece.evaluateAt(self, square=piece.getSquare())
        return score

    def evaluatePawn(self, pawn: IPawn):
        square = pawn.getSquare()
        return self.evaluatePosition(isWhite=pawn.isWhite(), table=self.PAWN_EVAL_WHITE, square=square)

    def evaluateKnight(self, knight: IKnight):
        square = knight.getSquare()
        return self.evaluatePosition(isWhite=knight.isWhite(), table=self.KNIGHT_EVAL_WHITE, square=square)

    def evaluateBishop(self, bishop: IBishop):
        square = bishop.getSquare()
        return self.evaluatePosition(isWhite=bishop.isWhite(), table=self.BISHOP_EVAL_WHITE, square=square)

    def evaluateRook(self, rook: IRook):
        square = rook.getSquare()
        return self.evaluatePosition(isWhite=rook.isWhite(), table=self.ROOK_EVAL_WHITE, square=square)

    def evaluateQueen(self, queen: IQueen):
        square = queen.getSquare()
        return self.evaluatePosition(isWhite=queen.isWhite(), table=self.QUEEN_EVAL_WHITE, square=square)

    def evaluateKing(self, king: IKing):
        square = king.getSquare()
        return self.evaluatePosition(isWhite=king.isWhite(), table=self.KING_EVAL_WHITE, square=square)

    def evaluateRookAt(self, rook: IRook, square):
        return self.evaluatePosition(isWhite=rook.isWhite(), table=self.ROOK_EVAL_WHITE, square=square)

    def evaluateQueenAt(self, queen: IQueen, square):
        return self.evaluatePosition(isWhite=queen.isWhite(), table=self.QUEEN_EVAL_WHITE, square=square)

    def evaluateBishopAt(self, bishop: IBishop, square):
        return self.evaluatePosition(isWhite=bishop.isWhite(), table=self.BISHOP_EVAL_WHITE, square=square)

    def evaluatePawnAt(self, pawn: IPawn, square):
        return self.evaluatePosition(isWhite=pawn.isWhite(), table=self.PAWN_EVAL_WHITE, square=square)

    def evaluateKnightAt(self, knight: IKnight, square):
        return self.evaluatePosition(isWhite=knight.isWhite(), table=self.KNIGHT_EVAL_WHITE, square=square)

    def evaluateKingAt(self, king: IKing, square):
        return self.evaluatePosition(isWhite=king.isWhite(), table=self.KING_EVAL_WHITE, square=square)

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

    def evaluateMove(self, move: Any):
        delta = 0.
        # captured piece
        capturedPiece = self.moveRepresentation.getCapturedPiece(move=move)
        if capturedPiece is not None:
            pieceEval = capturedPiece.evaluate(evaluator=self)
            delta += pieceEval
        # promotion
        promotedPiece = self.moveRepresentation.getPromotedPiece(move=move)
        movingPiece = self.moveRepresentation.getMovingPiece(move=move)
        if promotedPiece is not None:  # todo: castling!!!!!!!
            delta += promotedPiece.evaluateAt(self, square=self.moveRepresentation.getPromotionSquare(move))
            delta += -movingPiece.evaluate(self)
        else:
            delta += -movingPiece.evaluate(self)
            delta += movingPiece.evaluateAt(evaluator=self, square=self.moveRepresentation.getEndingSquare(move))
        self.deltas.append(delta)
        self.currentScore += delta
        self.currentScore *= -1

    def undoLast(self):
        delta = self.deltas.pop(-1)
        self.currentScore *= -1
        self.currentScore -= delta
