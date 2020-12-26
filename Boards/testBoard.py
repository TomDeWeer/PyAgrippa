import unittest

from Boards.Board import BoardSquareCenteredWithPieceSets
from Squares.SquareRepresentor import Square0x88Representor

boardClass = BoardSquareCenteredWithPieceSets
squareRepresentor = Square0x88Representor


class MyTestCase(unittest.TestCase):
    def testSetup(self):
        board = boardClass.initialSetup(squareRepresentor)




