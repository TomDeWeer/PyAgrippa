from typing import Generator, Any

from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Moves.MoveGeneration.AbstractMoveGenerator import AbstractMoveGenerator
from PyAgrippa.Moves.MoveGeneration.KillerMoveStrategy import KillerMoveStrategy
from PyAgrippa.Moves.MoveRepresentation import IMoveRepresentation


class LeafMoveGenerator(AbstractMoveGenerator):
    def __init__(self, moveRepresentation: IMoveRepresentation, strategy: str = 'PC', killerMoveStrategy: KillerMoveStrategy = None):
        """
        The variable strategy is (for now) a string deciding between Piece Centered ('PC') or Square Centered ('SC')
        move generation approaches. I might expand to bitboards later on and I also might move away from strings and
        use a strategy pattern instead.
        :param moveRepresentation:
        :param strategy:
        """

        self.representation = moveRepresentation
        self.strategy = strategy
        AbstractMoveGenerator.__init__(self, moveRepresentation=moveRepresentation, killerMoveStrategy=killerMoveStrategy)

    def __generatePseudoLegalMoves__(self,
                                     board: IBoard,
                                     ) -> Generator[Any, None, None]:
        if self.strategy == 'PC':
            return self.generatePseudoLegalMoves_PC(board)
        elif self.strategy == 'SC':
            return self.generatePseudoLegalMoves_SC(board)
        else:
            raise NotImplementedError
