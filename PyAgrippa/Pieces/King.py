from typing import Generator, Any

from chess import PieceType, KING

from PyAgrippa.Evaluation.BoardEvaluator import BoardEvaluator
from PyAgrippa.GUI.GUILayout import IGUILayout
from PyAgrippa.Moves.MoveRepresentation import IMoveRepresentation
from PyAgrippa.Pieces.NonSlidingPiece import INonSlidingPiece
from PyAgrippa.Pieces.Piece import IPiece
from PyAgrippa.Pieces.Rook import IRook
from PyAgrippa.Squares.Square import ISquare


class IKing(INonSlidingPiece):
    def getPythonChessPieceType(self) -> PieceType:
        return KING

    def getImage(self, layout: IGUILayout):
        if self.isWhite():
            return layout.getWhiteKingImage()
        else:
            return layout.getBlackKingImage()

    def getDestinationSquares(self, start: ISquare):
        return start.getKingDestinationSquares()

    def getAllPseudoLegalMoves(self, moveRepresentation: IMoveRepresentation) -> Generator[Any, None, None]:
        yield from self.__getAllPseudoLegalMoves__(moveRepresentation=moveRepresentation)
        yield from self.generateCastlingMoves(moveRepresentation=moveRepresentation)

    def isPseudoLegalMove(self, move: Any, representation: IMoveRepresentation):
        if super().isPseudoLegalMove(move, representation):
            return True
        if representation.isCastling(move):
            kingSide = representation.isKingsideCastling(move)
            if not self.getBoard().getCastlingRights(self.isWhite(), king=kingSide): # king hasnt moved + rook hasnt moved + rook not taken
                return False
            start = self.getSquare()
            kingDestination, rookDestination = start.getKingAndRookCastlingSquares(kingside=kingSide,
                                                                                   white=self.isWhite())
            board = self.getBoard()
            # check if there are no pieces in between
            if board.getPieceOn(square=kingDestination) is not None or board.getPieceOn(rookDestination) is not None:
                return False
            # check if the king and the squares the king passes through are not in check
            for square in [start, rookDestination, kingDestination]:
                if board.isAttacked(square, attackerIsWhite=not self.isWhite()):
                    return False
        else:
            return False

    def getAllPseudoLegalNonCaptures(self, moveRepresentation: IMoveRepresentation) -> Generator[Any, None, None]:
        yield from self.__getAllPseudoLegalNonCaptures__(moveRepresentation=moveRepresentation)
        yield from self.generateCastlingMoves(moveRepresentation=moveRepresentation)

    def getAllPseudoLegalCaptures(self, moveRepresentation: IMoveRepresentation) -> Generator[Any, None, None]:
        yield from self.__getAllPseudoLegalCaptures__(moveRepresentation=moveRepresentation)

    def generateCastlingMoves(self, moveRepresentation: IMoveRepresentation):
        board = self.getBoard()
        start = self.getSquare()
        # kingside
        for kingSide in [True, False]:
            if board.getCastlingRights(self.isWhite(), king=kingSide):  # king hasnt moved + rook hasnt moved + rook not taken
                kingDestination, rookDestination = start.getKingAndRookCastlingSquares(kingside=kingSide,
                                                                                       white=self.isWhite())
                # check if there are no pieces in between
                if board.getPieceOn(kingDestination) is not None or board.getPieceOn(rookDestination) is not None:
                    continue
                # check if the king and the squares the king passes through are not in check
                for square in [start, rookDestination, kingDestination]:
                    if board.isAttacked(square, attackerIsWhite=not self.isWhite()):
                        break
                else:
                    rook = board.getPieceOn(board.getInitialRookSquare(white=self.isWhite(), king=kingSide))  # castling rights guarantee this
                    assert isinstance(rook, IRook)
                    yield moveRepresentation.generateCastlingMove(board=board, rook=rook, king=self,
                                                                  kingSide=kingSide,
                                                                  white=self.isWhite(),
                                                                  kingStart=start, kingEnd=kingDestination,
                                                                  rookStart=rook.getSquare(), rookEnd=rookDestination)

    def evaluate(self, evaluator: BoardEvaluator):
        return evaluator.evaluateKing(self)

    def evaluateAt(self, evaluator: BoardEvaluator, square: ISquare):
        return evaluator.evaluateKingAt(self, square=square)
