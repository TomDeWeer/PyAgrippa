import time

from Boards.SCPSBoard import BoardSCPS
from Moves.MoveGenerator import MoveGenerator
from Moves.OOPMoveRepresentation.OOPMoveRepresentation import OOPMoveRepresentation
from Moves.Perft import Perft
from Squares.SquareRepresentor import Square0X88Representor

squareRepresentor = Square0X88Representor()
boardClass = BoardSCPS

board = boardClass(squareRepresentor)
board.setInitialSetup()
perft = Perft(board=board, moveGenerator=MoveGenerator(OOPMoveRepresentation()))
depths = [1, 2, 3, 4, 5]
for depth in depths:
    start = time.time()
    nbNodes = perft.pseudoLegalPerft(depth=depth)
    end = time.time()
    print(f"Found {nbNodes} nodes at depth {depth} in {round(end-start,6)} seconds.")

# todo: document results! this way, i can track 