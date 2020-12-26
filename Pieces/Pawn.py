from Pieces.Piece import IPiece, PieceSCPS


class IPawn(IPiece):
    pass


class PawnSCPS(PieceSCPS, IPawn):
    def __init__(self, isWhite: bool):
        PieceSCPS.__init__(self, isWhite=isWhite)
        IPawn.__init__(self, isWhite)

