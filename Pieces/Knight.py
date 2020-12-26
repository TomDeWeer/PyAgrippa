from GUI.GUILayout import IGUILayout
from Pieces.Piece import IPiece, PieceSCPS


class IKnight(IPiece):
    pass


class KnightSCPS(PieceSCPS, IKnight):
    def __init__(self, isWhite: bool):
        PieceSCPS.__init__(self, isWhite=isWhite)
        IKnight.__init__(self, isWhite)

    def getImage(self, layout: IGUILayout):
        if self.isWhite():
            return layout.getWhiteKnightImage()
        else:
            return layout.getBlackKnightImage()
