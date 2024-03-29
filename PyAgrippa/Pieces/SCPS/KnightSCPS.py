from PyAgrippa.Pieces.Knight import IKnight
from PyAgrippa.Pieces.SCPS.PieceSCPS import PieceSCPS


class KnightSCPS(PieceSCPS, IKnight):
    def __init__(self, isWhite: bool, identifier: int):
        PieceSCPS.__init__(self, isWhite=isWhite, identifier=identifier)
        IKnight.__init__(self, isWhite)

    def applyCastlingRightChangesDueToMove(self):
        return

    def castlingRightsChangeDueToMove(self):
        return False

    def applyCastlingRightChangesDueToCapture(self):
        return

