from typing import Generator, Any

from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Evaluation.BoardEvaluatorViaPieces import BoardEvaluatorViaPieces
from PyAgrippa.Moves.MoveGeneration.AbstractMoveGenerator import AbstractMoveGenerator
from PyAgrippa.Moves.MoveGeneration.LeafMoveGenerator import LeafMoveGenerator
from PyAgrippa.Moves.MoveRepresentation import IMoveRepresentation


class CaptureGenerator(LeafMoveGenerator):
    def __init__(self, moveRepresentation: IMoveRepresentation, strategy: str = 'PC',
                 useMVV: bool = True,
                 useLVA: bool = True):
        """
        MVV-LVA = Most Valuable Victim - Least Valuable Aggressor, see https://www.chessprogramming.org/MVV-LVA
        """
        LeafMoveGenerator.__init__(self, moveRepresentation=moveRepresentation, strategy=strategy)
        self.useMVV = useMVV
        self.useLVA = useLVA
        if self.useLVA or self.useMVV:  # todo: make this optional
            self.evaluator = BoardEvaluatorViaPieces()

    def generatePseudoLegalMoves_PC(self,
                                 board: IBoard,
                                 ) -> Generator[Any, None, None]:
        """
        PC = Piece centered
        """
        activePieces = board.getActivePieces()
        assert all([piece.isWhite() is board.isWhiteToMove() for piece in activePieces])
        if self.useLVA:  # LVA is quite cheap now because active pieces are not generated but already exist
            activePieces = sorted(activePieces, key=lambda piece: piece.evaluate(evaluator=self.evaluator))
        for piece in activePieces:
            # assert piece.isWhite() is board.isWhiteToMove()
            if self.useMVV:  # more expensive because you generate moves you might not apply
                moves = list(piece.getAllPseudoLegalCaptures(moveRepresentation=self.representation))
                moves = sorted(moves, key=lambda move: self.getRepresentation().getCapturedPiece(move).evaluate(evaluator=self.evaluator), reverse=True)
                yield from moves
            else:
                for move in piece.getAllPseudoLegalCaptures(moveRepresentation=self.representation):
                    yield move
        return
