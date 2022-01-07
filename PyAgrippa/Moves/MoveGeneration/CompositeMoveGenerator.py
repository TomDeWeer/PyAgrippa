from typing import Generator, Any, List

from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Moves.MoveGeneration.AbstractMoveGenerator import AbstractMoveGenerator
from PyAgrippa.Moves.MoveGeneration.CaptureGenerator import CaptureGenerator
from PyAgrippa.Moves.MoveGeneration.KillerMoveStrategy import KillerMoveStrategy
from PyAgrippa.Moves.MoveGeneration.MoveCollection import SimpleMoveQueue
from PyAgrippa.Moves.MoveGeneration.NonCaptureGenerator import NonCaptureGenerator
from PyAgrippa.Moves.MoveRepresentation import IMoveRepresentation


class CompositeMoveGenerator(AbstractMoveGenerator):
    def __init__(self, subGenerators: List[AbstractMoveGenerator], killerMoveStrategy: KillerMoveStrategy = None):
        """
        Gives control over the ordering, since generators are called sequentially based on the given list.
        """
        # todo: somehow, this should guarantee that all moves are generated and no move is doubly generated
        # todo: this is piece based but ideally one can choose this!
        self.subGenerators = subGenerators
        representation = subGenerators[0].getRepresentation()
        for generator in subGenerators:
            assert generator.getRepresentation() is representation
        AbstractMoveGenerator.__init__(self, moveRepresentation=representation, killerMoveStrategy=killerMoveStrategy)

    @classmethod
    def capturesFirstGenerator(cls, moveRepresentation: IMoveRepresentation, strategy: str = 'PC', maxMovesInjected: int = 0):
        """First captures, then everything else."""
        return cls(subGenerators=[CaptureGenerator(moveRepresentation=moveRepresentation),
                                  NonCaptureGenerator(moveRepresentation=moveRepresentation)],
                   maxMovesInjected=maxMovesInjected)

    def __generatePseudoLegalMoves__(self,
                                     board: IBoard,
                                     ) -> Generator[Any, None, None]:
        """
        Generator moves for the board.
        """
        for generator in self.subGenerators:
            yield from generator.generatePseudoLegalMoves(board=board)
        return
