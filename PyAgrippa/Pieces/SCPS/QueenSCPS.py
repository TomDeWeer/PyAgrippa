from PyAgrippa.GUI.GUILayout import IGUILayout
from PyAgrippa.Pieces.Queen import IQueen
from PyAgrippa.Pieces.SCPS.SlidingPieceSCPS import SlidingPieceSCPS


class QueenSCPS(SlidingPieceSCPS, IQueen):
    def __init__(self, isWhite: bool, identifier: int):
        SlidingPieceSCPS.__init__(self, isWhite=isWhite, identifier=identifier)
        IQueen.__init__(self, isWhite)

    def getImage(self, layout: IGUILayout):
        if self.isWhite():
            return layout.getWhiteQueenImage()
        else:
            return layout.getBlackQueenImage()

    def applyCastlingRightChangesDueToMove(self):
        return

    def castlingRightsChangeDueToMove(self):
        return False

    def applyCastlingRightChangesDueToCapture(self):
        return