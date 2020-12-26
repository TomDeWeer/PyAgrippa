import unittest

from Boards.Board import BoardSquareCenteredWithPieceSets, IBoard
from Squares.SquareRepresentor import Square0x88Representor

boardClass = BoardSquareCenteredWithPieceSets
squareRepresentor = Square0x88Representor()


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.board: IBoard = boardClass(squareRepresentor)

    def testGetSquares(self):
        for j, rank in enumerate(self.board.getSquares()):
            for i, square in enumerate(rank):
                self.assertEqual(j, square.getRank())
                self.assertEqual(i, square.getFile())




