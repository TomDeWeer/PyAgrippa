from Boards.Board import IBoard
from Moves.MoveGenerator import MoveGenerator


class Perft:
    """
    Tests a move generator with perft.
    """

    def __init__(self, board: IBoard, moveGenerator: MoveGenerator):
        self.board = board
        self.moveGenerator = moveGenerator

    def pseudoLegalPerft(self, depth: int):
        nbNodes = 0
        if depth == 0:
            return 1
        pseudoLegalMoves = self.moveGenerator.generatePseudoLegalMoves(self.board)
        if depth == 1:
            return len(list(pseudoLegalMoves))
        for move in pseudoLegalMoves:
            self.moveGenerator.getRepresentation().applyMove(move)
            assert self.board.checkValidity()
            nbNodes += self.pseudoLegalPerft(depth=depth - 1)
            self.moveGenerator.getRepresentation().undoMove(move)
        return nbNodes

