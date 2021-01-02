from Boards.Board import IBoard


class AI:
    def __init__(self, ):
        cheapOrdering = None
        expensiveOrdering = None

    def getOrderingScheme(self, depth):
        if depth >

    def getBestMove(self, board: IBoard):
        ordering = self.getOrderingScheme(depth)
        for move in board.getPseudoLegalMoves(ordering):
