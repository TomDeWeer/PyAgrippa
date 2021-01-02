from GUI.GUILayout import IGUILayout
from Pieces.Bishop import IBishop
from Pieces.SCPS.SlidingPieceSCPS import SlidingPieceSCPS


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

    def applyCastlingRightChangesDueToCapture(self):
        return
