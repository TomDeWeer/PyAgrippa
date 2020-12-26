import unittest

from Squares.SquareRepresentor import Square0x88Representor

representor = Square0x88Representor


class MyTestCase(unittest.TestCase):
    def testFileAndRank(self):
        for rank in range(8):
            for file in range(8):
                pos = representor.generateViaRankAndFile(rank=rank, file=file)
                self.assertEqual(file, pos.getFile())
                self.assertEqual(rank, pos.getRank())




