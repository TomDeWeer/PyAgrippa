from PyAgrippa.AI.CompositeAIs.ContinuationDeciders.IContinuationDecider import IContinuationDecider
from PyAgrippa.Boards.Board import IBoard


class MiddleGameDetector(IContinuationDecider):
    def decideContinuation(self, board: IBoard) -> bool:
        return self.isMiddleGame(board=board)

    def isMiddleGame(self, board: IBoard) -> bool:
        raise NotImplementedError  # todo: not sure i really need this