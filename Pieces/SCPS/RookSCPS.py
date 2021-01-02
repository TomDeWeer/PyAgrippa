from GUI.GUILayout import IGUILayout
from Pieces.Rook import IRook
from Pieces.SCPS.SlidingPieceSCPS import SlidingPieceSCPS


class RookSCPS(SlidingPieceSCPS, IRook):
    def __init__(self, isWhite: bool, identifier: int):
        SlidingPieceSCPS.__init__(self, isWhite=isWhite, identifier=identifier)
        IRook.__init__(self, isWhite)

    def getImage(self, layout: IGUILayout):
        if self.isWhite():
            return layout.getWhiteRookImage()
        else:
            return layout.getBlackRookImage()

    def applyCastlingRightChangesDueToMove(self):
        # if a rook moves for the first time, then castling rights are surely lost for king or queenside
        # how to check if its the first time and if its a kingside or queenside rook?
        # if it is currently on the original kingside square -> kingside castling rights can be revoked because
        # 1. if it hasn't moved before then its a kingside rook and moving it the first time means revoking the rights
        # 2. if it has moved before then the kingside castling rights are already revoked, so revoking them again is ok
        # if its not on the original square, then we can assume rights have been revoked before
        square = self.getSquare()
        if square.isKingsideRookSquare(self.isWhite()):
            self.getBoard().setCastlingRights(white=self.isWhite(), king=True, value=False)
        if square.isQueensideRookSquare(self.isWhite()):
            self.getBoard().setCastlingRights(white=self.isWhite(), king=False, value=False)

    def applyCastlingRightChangesDueToCapture(self):
        # if a rook gets captured that hasn't moved before, one must remove the castling rights
        # if it's on the original kingside rook square you can remove the kingside castling rights because
        # if it hasn't moved before then this fits the definition for removal
        # if it has moved before (and is thus either the original rook, the other rook or a promoted pawn), then the
        # castling rights can be revoked anyhow because they were already revoked
        square = self.getSquare()
        if square.isKingsideRookSquare(self.isWhite()):
            self.getBoard().setCastlingRights(white=self.isWhite(), king=True, value=False)
        if square.isQueensideRookSquare(self.isWhite()):
            self.getBoard().setCastlingRights(white=self.isWhite(), king=False, value=False)

