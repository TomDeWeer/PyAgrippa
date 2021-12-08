from typing import Generator, Any

from PyAgrippa.Evaluation.BoardEvaluator import BoardEvaluator
from PyAgrippa.GUI.GUILayout import IGUILayout
from PyAgrippa.Moves.MoveRepresentation import IMoveRepresentation
from PyAgrippa.Pieces.Piece import IPiece
from PyAgrippa.Pieces.Rook import IRook


class IKing(IPiece):
    def getImage(self, layout: IGUILayout):
        if self.isWhite():
            return layout.getWhiteKingImage()
        else:
            return layout.getBlackKingImage()

    def getAllPseudoLegalMoves(self, moveRepresentation: IMoveRepresentation) -> Generator[Any, None, None]:
        # normal moves
        yield from self.generateNormalMoves(moveRepresentation)
        # castling
        yield from self.generateCastlingMoves(moveRepresentation)

    def generateNormalMoves(self, moveRepresentation):
        board = self.getBoard()
        start = self.getSquare()
        for destinationSquare in start.getKingDestinationSquares():
            capturedPiece = board.getPieceOn(destinationSquare)
            if capturedPiece is None:
                yield moveRepresentation.generateMove(board=board,
                                                      piece=self,
                                                      start=start,
                                                      end=destinationSquare)
            else:
                if self.isWhite() == capturedPiece.isWhite():
                    continue
                else:
                    yield moveRepresentation.generateCapture(board=board, start=start,
                                                             end=destinationSquare,
                                                             movingPiece=self,
                                                             capturedPiece=capturedPiece)

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
