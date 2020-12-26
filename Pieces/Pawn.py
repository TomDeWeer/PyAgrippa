from GUI.GUILayout import IGUILayout
from Pieces.Piece import IPiece, PieceSCPS


class IPawn(IPiece):
    pass


class PawnSCPS(PieceSCPS, IPawn):
    def __init__(self, isWhite: bool):
        PieceSCPS.__init__(self, isWhite=isWhite)
        IPawn.__init__(self, isWhite)

    def getImage(self, layout: IGUILayout):
        if self.isWhite():
            return layout.getWhitePawnImage()
        else:
            return layout.getBlackPawnImage()
