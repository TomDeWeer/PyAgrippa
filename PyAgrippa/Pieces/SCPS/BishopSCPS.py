from PyAgrippa.GUI.GUILayout import IGUILayout
from PyAgrippa.Pieces.Bishop import IBishop
from PyAgrippa.Pieces.SCPS.SlidingPieceSCPS import SlidingPieceSCPS


class BishopSCPS(SlidingPieceSCPS, IBishop):
    def __init__(self, isWhite: bool, identifier: int):
        SlidingPieceSCPS.__init__(self, isWhite=isWhite, identifier=identifier)
        IBishop.__init__(self, isWhite)

    def getImage(self, layout: IGUILayout):
        if self.isWhite():
            return layout.getWhiteBishopImage()
        else:
            return layout.getBlackBishopImage()

    def applyCastlingRightChangesDueToMove(self):
        return

    def castlingRightsChangeDueToMove(self):
        return False

    def applyCastlingRightChangesDueToCapture(self):
        return
