import unittest

from Boards.Board import IBoard
from Boards.SCPSBoard import BoardSCPS
from Squares.SquareRepresentor import Square0X88Representor

boardClass = BoardSCPS
squareRepresentor = Square0X88Representor()


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.board: IBoard = boardClass(squareRepresentor)

    def testGetSquares(self):
        for j, rank in enumerate(self.board.getSquares()):
            for i, square in enumerate(rank):
                self.assertEqual(j, square.getRank())
                self.assertEqual(i, square.getFile())




