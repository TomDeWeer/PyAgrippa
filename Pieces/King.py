from typing import Generator, Any

from GUI.GUILayout import IGUILayout
from Moves.MoveRepresentation import IMoveRepresentation
from Pieces.Piece import IPiece
from Pieces.Rook import IRook


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
            if capturedPiece is not None:
                if self.isWhite() == capturedPiece.isWhite():
                    continue
                else:
                    yield moveRepresentation.generateCapture(board=board, start=start,
                                                             end=destinationSquare,
                                                             movingPiece=self,
                                                             capturedPiece=capturedPiece)
            yield moveRepresentation.generateMove(board=board,
                                                  piece=self,
                                                  start=start,
                                                  end=destinationSquare)

    def generateCastlingMoves(self, moveRepresentation):
        board = self.getBoard()
        start = self.getSquare()
        # kingside
        for kingside in [True, False]:
            if board.getCastlingRights(self.isWhite(), king=kingside):  # king hasnt moved + rook hasnt moved + rook not taken
                kingDestination, rookDestination = start.getKingAndRookCastlingSquares(kingside=kingside,
                                                                                       white=self.isWhite())
                # check if there are no pieces in between
                if board.getPieceOn(kingDestination) is not None or board.getPieceOn(rookDestination) is not None:
                    continue
                # check if the king and the squares the king passes through are not in check
                for square in [start, rookDestination, kingDestination]:
                    if board.isAttacked(square, attackerIsWhite=not self.isWhite()):
                        break
                else:
                    rook: IRook = board.getPieceOn(start.getRookSquare(white=self.isWhite()), king=kingside) # castling rights guarantee this
                    yield moveRepresentation.getCastlingMove(kingside=kingside, white=self.isWhite())
