from abc import ABC

from PyAgrippa.Boards.Board import IBoard


class IContinuationDecider(ABC):
    def decideContinuation(self, board: IBoard) -> bool:
        raise NotImplementedError