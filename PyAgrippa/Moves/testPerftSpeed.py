import time

from PyAgrippa.Boards.SCPSBoard import BoardSCPS
from PyAgrippa.Moves.MoveGeneration.AbstractMoveGenerator import AbstractMoveGenerator
from PyAgrippa.Moves.MoveGeneration.AllMoveGenerator import AllMoveGenerator
from PyAgrippa.Moves.OOPMoveRepresentation.OOPMoveRepresentation import OOPMoveRepresentation
from PyAgrippa.Moves.Perft import Perft
from PyAgrippa.Squares.SquareRepresentor import Square0X88Representor

squareRepresentor = Square0X88Representor()
boardClass = BoardSCPS

board = boardClass(squareRepresentor)
board.setInitialSetup()
perft = Perft(board=board, moveGenerator=AllMoveGenerator(OOPMoveRepresentation()))
depths = [1, 2, 3, 4, 5]
for depth in depths:
    start = time.time()
    nbNodes = perft.pseudoLegalPerft(depth=depth)
    end = time.time()
    print(f"Found {nbNodes} nodes at depth {depth} in {round(end-start,6)} seconds.")

# todo: document results! this way, i can track 