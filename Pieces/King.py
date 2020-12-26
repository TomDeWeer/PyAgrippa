from GUI.GUILayout import IGUILayout
from Pieces.Piece import IPiece, PieceSCPS


class IKing(IPiece):
    pass


class KingSCPS(PieceSCPS, IKing):
    def __init__(self, isWhite: bool):
        PieceSCPS.__init__(self, isWhite=isWhite)
        IKing.__init__(self, isWhite)

    def getImage(self, layout: IGUILayout):
        if self.isWhite():
            return layout.getWhiteKingImage()
        else:
            return layout.getBlackKingImage()
