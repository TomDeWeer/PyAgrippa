from typing import Generator, Any

from chess import PieceType, KNIGHT

from PyAgrippa.Evaluation.BoardEvaluator import BoardEvaluator
from PyAgrippa.GUI.GUILayout import IGUILayout
from PyAgrippa.Moves.MoveRepresentation import IMoveRepresentation
from PyAgrippa.Pieces.NonSlidingPiece import INonSlidingPiece
from PyAgrippa.Pieces.Piece import IPiece
from PyAgrippa.Squares.Square import ISquare


class IKnight(INonSlidingPiece):

    def getPythonChessPieceType(self) -> PieceType:
        return KNIGHT

    def getImage(self, layout: IGUILayout):
        if self.isWhite():
            return layout.getWhiteKnightImage()
        else:
            return layout.getBlackKnightImage()

    def getDestinationSquares(self, start: ISquare):
        return start.getKnightDestinationSquares()

    def evaluate(self, evaluator: BoardEvaluator):
        return evaluator.evaluateKnight(self)

    def evaluateAt(self, evaluator: BoardEvaluator, square: ISquare):
        return evaluator.evaluateKnightAt(self, square=square)

    def getAllPseudoLegalMoves(self, moveRepresentation: IMoveRepresentation) -> Generator[Any, None, None]:
        yield from self.__getAllPseudoLegalMoves__(moveRepresentation=moveRepresentation)

    def getAllPseudoLegalNonCaptures(self, moveRepresentation: IMoveRepresentation) -> Generator[Any, None, None]:
        yield from self.__getAllPseudoLegalNonCaptures__(moveRepresentation=moveRepresentation)

    def getAllPseudoLegalCaptures(self, moveRepresentation: IMoveRepresentation) -> Generator[Any, None, None]:
        yield from self.__getAllPseudoLegalCaptures__(moveRepresentation=moveRepresentation)