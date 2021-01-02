from GUI.GUILayout import IGUILayout
from Pieces.Knight import IKnight
from Pieces.Pawn import IPawn
from Pieces.Queen import IQueen
from Pieces.SCPS.PieceSCPS import PieceSCPS


class PawnSCPS(PieceSCPS, IPawn):
    def getPromotedKnight(self) -> IKnight:
        return self.promotedKnight

    def getPromotedQueen(self) -> IQueen:
        return self.promotedQueen

    def __init__(self, isWhite: bool, identifier: int):
        PieceSCPS.__init__(self, identifier=identifier, isWhite=isWhite)
        IPawn.__init__(self, isWhite)
        self.promotedKnight = None
        self.promotedQueen = None

    def setPromotedKnight(self, knight: IKnight):
        self.promotedKnight = knight

    def setPromotedQueen(self, queen: IQueen):
        self.promotedQueen = queen

    def getImage(self, layout: IGUILayout):
        if self.isWhite():
            return layout.getWhitePawnImage()
        else:
            return layout.getBlackPawnImage()

    def applyCastlingRightChangesDueToMove(self):
        return

    def applyCastlingRightChangesDueToCapture(self):
        return
