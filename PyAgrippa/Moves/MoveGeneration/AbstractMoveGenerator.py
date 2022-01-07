from typing import Generator, Any, Optional

from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Moves.MoveGeneration.KillerMoveStrategy import KillerMoveStrategy
from PyAgrippa.Moves.MoveGeneration.MoveCollection import SimpleMoveQueue
from PyAgrippa.Moves.MoveRepresentation import IMoveRepresentation


class AbstractMoveGenerator:
    def __init__(self, moveRepresentation: IMoveRepresentation,
                 killerMoveStrategy: Optional[KillerMoveStrategy] = None):
        """
        Ideally, allows for all types of move ordering described in https://www.chessprogramming.org/Move_Ordering.

        Killer move support:
        * LAST_N: keep the last N added killer moves (per ply!)
        * BEST_N: keep the best N killer moves (based on their number of kills) for every ply (!)
        """
        self.representation = moveRepresentation
        self.killerStrat = killerMoveStrategy
        self.hashMove = None

    def getRepresentation(self):
        return self.representation

    def generatePseudoLegalMoves(self,
                                 board: IBoard,
                                 depth: int = None,
                                 ) -> Generator[Any, None, None]:
        injected = []
        if self.hashMove is not None:
            hashMove = self.hashMove
            self.hashMove = None  # clear
            assert board.isPseudoLegalMove(move=hashMove, representation=self.getRepresentation())
            yield hashMove
            injected.append(hashMove)
        if self.supportsKillerMoveInjection():
            assert depth is not None, "A depth must be supplied when using killer moves."
            for move in self.killerStrat.getInjected(depth=depth):
                if board.isPseudoLegalMove(move, self.getRepresentation()):
                    if move not in injected:
                        # print(f'Yielding {move}')
                        yield move
                        injected.append(move)
        for move in self.__generatePseudoLegalMoves__(board):
            if move not in injected:
                yield move
        return

    def __generatePseudoLegalMoves__(self,
                                     board: IBoard,
                                     ) -> Generator[Any, None, None]:
        raise NotImplementedError

    def generatePseudoLegalMoves_PC(self,
                                    board: IBoard,
                                    ) -> Generator[Any, None, None]:
        """
        PC = Piece centered
        """
        raise NotImplementedError

    def generatePseudoLegalMoves_SC(self,
                                    board: IBoard,
                                    ) -> Generator[Any, None, None]:
        """
        SC = Square centered
        """
        raise NotImplementedError

    def generateLegal_PC(self):
        raise NotImplementedError

    def generateLegal_SC(self):
        raise NotImplementedError

    def supportsKillerMoveInjection(self):
        return self.killerStrat is not None

    def injectKillerMove(self, move: Any, depth: int):
        self.killerStrat.injectMove(move, depth)

    def resetKillerMoves(self):
        self.killerStrat.reset()

    def injectHashMove(self, move: Any):
        assert self.hashMove is None
        self.hashMove = move
