from typing import Generator, Any

from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Moves.MoveGeneration.AbstractMoveGenerator import AbstractMoveGenerator
from PyAgrippa.Moves.MoveGeneration.KillerMoveStrategy import KillerMoveStrategy
from PyAgrippa.Moves.MoveGeneration.LeafMoveGenerator import LeafMoveGenerator
from PyAgrippa.Moves.MoveGeneration.MoveCollection import SimpleMoveQueue
from PyAgrippa.Moves.MoveRepresentation import IMoveRepresentation


class AllMoveGenerator(LeafMoveGenerator):
    def __init__(self, moveRepresentation: IMoveRepresentation, strategy: str = 'PC', killerMoveStrategy: KillerMoveStrategy = None):
        """
        Injected moves are used first (and last added mans first used among these). No more than maxMovesInjected are
        kept for both black and white. If more are added, then the last one added is removed.
        # todo: add ply-dependent move gathering +
        # todo: options in https://escholarship.mcgill.ca/concern/theses/j96022066?locale=en (see e.g. LAST_1 and LAST_2)
        """
        LeafMoveGenerator.__init__(self, moveRepresentation, strategy=strategy, killerMoveStrategy=killerMoveStrategy)

    def generatePseudoLegalMoves_PC(self,
                                 board: IBoard,
                                 ) -> Generator[Any, None, None]:
        """
        Generator moves for the board.
        """
        activePieces = board.getActivePieces()
        for piece in activePieces:
            for move in piece.getAllPseudoLegalMoves(moveRepresentation=self.representation):
                yield move
        return


