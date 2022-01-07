from typing import Generator, Any

from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Moves.MoveGeneration.AbstractMoveGenerator import AbstractMoveGenerator
from PyAgrippa.Moves.MoveGeneration.LeafMoveGenerator import LeafMoveGenerator
from PyAgrippa.Moves.MoveRepresentation import IMoveRepresentation


class NonCaptureGenerator(LeafMoveGenerator):
    def __init__(self, moveRepresentation: IMoveRepresentation, strategy: str = 'PC'):
        LeafMoveGenerator.__init__(self, moveRepresentation=moveRepresentation, strategy=strategy)

    def generatePseudoLegalMoves_PC(self,
                                 board: IBoard,
                                 ) -> Generator[Any, None, None]:
        """
        PC = Piece centered
        """
        activePieces = board.getActivePieces()
        for piece in activePieces:
            for move in piece.getAllPseudoLegalNonCaptures(moveRepresentation=self.representation):
                yield move
        return
