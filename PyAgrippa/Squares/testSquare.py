import unittest

from PyAgrippa.Squares.SquareRepresentor import Square0X88Representor

representor = Square0X88Representor


class MyTestCase(unittest.TestCase):
    def testFileAndRank(self):
        for rank in range(8):
            for file in range(8):
                pos = representor.generateViaRankAndFile(rank=rank, file=file)
                self.assertEqual(file, pos.getFile())
                self.assertEqual(rank, pos.getRank())

    def testOnBoard(self):
        for rank in range(8):
            for file in range(8):
                pos = representor.generateViaRankAndFile(rank=rank, file=file)
                self.assertTrue(pos.onBoard())

        for rank in range(8):
            for file in [-1, -2, 8, 9]:
                pos = representor.generateViaRankAndFile(rank=rank, file=file)
                self.assertFalse(pos.onBoard())

        for file in range(8):
            for rank in [-1, -2, 8, 9]:
                pos = representor.generateViaRankAndFile(rank=rank, file=file)
                self.assertFalse(pos.onBoard())

