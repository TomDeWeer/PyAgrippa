from GUI.GUILayout import IGUILayout
from Pieces.Piece import PieceSCPS
from Pieces.SlidingPiece import ISlidingPiece, SlidingPieceSCPS


class IQueen(ISlidingPiece):
    pass


class QueenSCPS(SlidingPieceSCPS, IQueen):
    def __init__(self, isWhite: bool):
        SlidingPieceSCPS.__init__(self, isWhite=isWhite)
        IQueen.__init__(self, isWhite)

    def getImage(self, layout: IGUILayout):
        if self.isWhite():
            return layout.getWhiteQueenImage()
        else:
            return layout.getBlackQueenImage()
