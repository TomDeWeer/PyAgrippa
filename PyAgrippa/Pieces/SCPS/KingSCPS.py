from PyAgrippa.Pieces.King import IKing
from PyAgrippa.Pieces.SCPS.PieceSCPS import PieceSCPS


class KingSCPS(PieceSCPS, IKing):
    def __init__(self, isWhite: bool, identifier: int):
        PieceSCPS.__init__(self, isWhite=isWhite, identifier=identifier)
        IKing.__init__(self, isWhite)

    def applyCastlingRightChangesDueToMove(self):
        self.getBoard().setCastlingRightsOf(white=self.isWhite(), kingsideValue=False, queensideValue=False)

    def castlingRightsChangeDueToMove(self):
        return self.getBoard().getCastlingRights(white=self.isWhite(), king=True) or \
               self.getBoard().getCastlingRights(white=self.isWhite(), king=False)

    def applyCastlingRightChangesDueToCapture(self):
        self.getBoard().setCastlingRightsOf(white=self.isWhite(), kingsideValue=False, queensideValue=False)


