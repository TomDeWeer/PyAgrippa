import os
from typing import Optional


class IGUILayout:
    def getSGLookAndFeel(self) -> str:
        raise NotImplementedError

    def getFileLabels(self) -> Optional[str]:
        raise NotImplementedError

    def getFileLabelFont(self) -> str:
        raise NotImplementedError

    def getRankLabels(self) -> Optional[str]:
        raise NotImplementedError

    def getRankLabelFont(self) -> str:
        raise NotImplementedError

    def getBlackPawnImage(self) -> str:
        return os.path.join(self.getPieceIconPath(), 'pawnb.png')

    def getWhitePawnImage(self) -> str:
        return os.path.join(self.getPieceIconPath(), 'pawnw.png')

    def getBlackKnightImage(self) -> str:
        return os.path.join(self.getPieceIconPath(), 'knightb.png')

    def getWhiteKnightImage(self) -> str:
        return os.path.join(self.getPieceIconPath(), 'knightw.png')

    def getBlackBishopImage(self) -> str:
        return os.path.join(self.getPieceIconPath(), 'bishopb.png')

    def getWhiteBishopImage(self) -> str:
        return os.path.join(self.getPieceIconPath(), 'bishopw.png')

    def getBlackRookImage(self) -> str:
        return os.path.join(self.getPieceIconPath(), 'rookb.png')

    def getWhiteRookImage(self) -> str:
        return os.path.join(self.getPieceIconPath(), 'rookw.png')

    def getBlackQueenImage(self) -> str:
        return os.path.join(self.getPieceIconPath(), 'queenb.png')

    def getWhiteQueenImage(self) -> str:
        return os.path.join(self.getPieceIconPath(), 'queenw.png')

    def getBlackKingImage(self) -> str:
        return os.path.join(self.getPieceIconPath(), 'kingb.png')

    def getWhiteKingImage(self) -> str:
        return os.path.join(self.getPieceIconPath(), 'kingw.png')

    def getBlankImage(self):
        return os.path.join(self.getPieceIconPath(), 'blank.png')

    def getPieceIconPath(self) -> str:
        raise NotImplementedError

    def getLightSquareColor(self) -> str:
        raise NotImplementedError

    def getDarkSquareColor(self) -> str:
        raise NotImplementedError


class DefaultGUILayout(IGUILayout):

    def getPieceIconPath(self) -> str:
        return './PieceIcons/Default'  # path to the chess pieces

    def getSGLookAndFeel(self) -> str:
        return "BrownBlue"

    def getFileLabels(self) -> Optional[str]:
        return "abcdefgh"

    def getFileLabelFont(self) -> str:
        return "Any 13"

    def getRankLabels(self) -> Optional[str]:
        return "12345678"

    def getRankLabelFont(self) -> str:
        return "Any 13"

    def getLightSquareColor(self) -> str:
        return '#F0D9B5'

    def getDarkSquareColor(self) -> str:
        return '#B58863'






