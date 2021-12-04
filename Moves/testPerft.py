import time
import unittest

from Boards.SCPSBoard import BoardSCPS
from Moves.MoveGenerator import MoveGenerator
from Moves.OOPMoveRepresentation.OOPMoveRepresentation import OOPMoveRepresentation
from Moves.Perft import Perft
from Squares.SquareRepresentor import Square0X88Representor

squareRepresentor = Square0X88Representor()
boardClass = BoardSCPS


class PerftTest(unittest.TestCase):
    def testInitialSetup(self):
        board = boardClass(squareRepresentor)
        board.setInitialSetup()
        perft = Perft(board=board, moveGenerator=MoveGenerator(OOPMoveRepresentation()))
        depths = [0, 1, 2, 3, 4, 5, 6]
        correctPerfts = [1, 20, 400, 8902, 197742, 4897256, 120921506]  # from http://www.open-aurec.com/wbforum/viewtopic.php?f=4&t=51764, for pseudo legal (quite hard actually)
        for depth, correctPerft in zip(depths, correctPerfts):
            start = time.time()
            nbNodes = perft.pseudoLegalPerft(depth=depth)
            end = time.time()
            print(f"Found {nbNodes} nodes at depth {depth} in {round(end-start,3)} seconds.")
            self.assertEqual(nbNodes, correctPerft)


if __name__ == '__main__':
    unittest.main()
