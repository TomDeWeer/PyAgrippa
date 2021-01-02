from Pieces.King import IKing
from Pieces.SCPS.PieceSCPS import PieceSCPS


class KingSCPS(PieceSCPS, IKing):
    def __init__(self, isWhite: bool, identifier: int):
        PieceSCPS.__init__(self, isWhite=isWhite, identifier=identifier)
        IKing.__init__(self, isWhite)

    def applyCastlingRightChangesDueToMove(self):
        self.getBoard().setCastlingRightsOf(white=self.isWhite(), kingsideValue=False, queensideValue=False)

    def applyCastlingRightChangesDueToCapture(self):
        self.getBoard().setCastlingRightsOf(white=self.isWhite(), kingsideValue=False, queensideValue=False)


