from typing import Generator, Any

from PyAgrippa.Evaluation.BoardEvaluator import BoardEvaluator
from PyAgrippa.GUI.GUILayout import IGUILayout
from PyAgrippa.Moves.MoveRepresentation import IMoveRepresentation
from PyAgrippa.Pieces.Piece import IPiece


class IKnight(IPiece):

    def getImage(self, layout: IGUILayout):
        if self.isWhite():
            return layout.getWhiteKnightImage()
        else:
            return layout.getBlackKnightImage()

    def getAllPseudoLegalMoves(self, moveRepresentation: IMoveRepresentation) -> Generator[Any, None, None]:
        board = self.getBoard()
        start = self.getSquare()
        for destinationSquare in start.getKnightDestinationSquares():
            capturedPiece = board.getPieceOn(destinationSquare)
            if capturedPiece is not None:
                if self.isWhite() == capturedPiece.isWhite():
                    continue
                else:
                    yield moveRepresentation.generateCapture(board=board, start=start,
                                                             end=destinationSquare,
                                                             movingPiece=self,
                                                             capturedPiece=capturedPiece)
            else:
                yield moveRepresentation.generateMove(
                    board=board,
                    piece=self,
                    start=start,
                    end=destinationSquare)

    def evaluate(self, evaluator: BoardEvaluator):
        return evaluator.evaluateKnight(self)
