from typing import Generator, Any

from Boards.Board import IBoard
from Moves.MoveRepresentation import IMoveRepresentation


class MoveGenerator:
    def __init__(self, moveRepresentation: IMoveRepresentation):
        self.representation = moveRepresentation

    def getRepresentation(self):
        return self.representation

    def generatePseudoLegalMoves(self,
                                 board: IBoard,
                                 # ordering: MoveOrderingScheme,
                                 ) -> Generator[Any, None, None]:
        """
        Generator moves for the board.
        """
        activePieces = board.getActivePieces()
        for piece in activePieces:
            for move in piece.getAllPseudoLegalMoves(moveRepresentation=self.representation):
                yield move
        return




