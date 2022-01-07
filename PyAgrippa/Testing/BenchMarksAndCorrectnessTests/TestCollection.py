from typing import List

from PyAgrippa.Testing.BenchMarksAndCorrectnessTests.CorrectnessAndPerformanceTest import CorrectnessAndPerformanceTest
from PyAgrippa.Boards.SCPSBoard import BoardSCPS
from PyAgrippa.Moves.OOPMoveRepresentation.OOPMoveRepresentation import OOPMoveRepresentation
from PyAgrippa.Squares.Square import C6, H1, H4, H3, E4, E3, F6, G6, E6, G5
from PyAgrippa.Squares.SquareRepresentor import Square0X88Representor


class CorrectnessAndPerformanceTestCollection:
    # todo: expand to options for other board representations
    def __init__(self):
        self.tests = []

    def getTests(self) -> List[CorrectnessAndPerformanceTest]:
        return self.tests

    # def collectFromCombinations(self, boards: List[IBoard], moves: List[IMove]):
    #     for board in boards:
    #         for move in moves:
    #             self.tests.append(CorrectnessTest(board=board, correctMove=move))

    def collectAll(self):
        self.collectInitialSetup()
        self.collectMateIn2s()
        self.collectMateIn3s()
        self.collectPuzzles()
        self.collectMiddleGames()

    def collectInitialSetup(self):
        board = BoardSCPS().setInitialSetup()
        self.tests.append(CorrectnessAndPerformanceTest(board=board, moveRepresentation=OOPMoveRepresentation(),
                                                        correctMove=None, name="Initial Setup"))

    def collectMateIn2s(self):
        self.collectMateIn2_1()
        self.collectMateIn2_2()

    def collectMateIn2_1(self):
        board = BoardSCPS.fromFEN(r"6rk/pp6/5P2/3p3N/8/5n1b/PP3P1P/R2R3K b - - 7 28",
                                  squareRepresentor=Square0X88Representor())
        moveRepresentation = OOPMoveRepresentation()
        start = board.getSquareAt(file=7, rank=2)
        end = board.getSquareAt(file=6, rank=1)
        move = moveRepresentation.generateMove(board=board, piece=board.getPieceOn(start), start=start, end=end, )
        self.tests.append(CorrectnessAndPerformanceTest(board=board,
                                                        name="Mate in 2 (1)",
                                                        correctMove=move,
                                                        moveRepresentation=moveRepresentation))

    def collectMateIn2_2(self):
        board = BoardSCPS.fromFEN(r"6k1/7p/1pq2pp1/p3p3/2P4P/1P4PK/P2Q1P2/8 b - - 1 32",
                                  squareRepresentor=Square0X88Representor())
        moveRepresentation = OOPMoveRepresentation()
        start = board.getSquareAt(*C6)
        end = board.getSquareAt(*H1)
        move = moveRepresentation.generateMove(board=board, piece=board.getPieceOn(start), start=start, end=end, )
        self.tests.append(CorrectnessAndPerformanceTest(board=board,
                                                        name="Mate in 2 (2)",
                                                        correctMove=move,
                                                        moveRepresentation=moveRepresentation))

    def collectMateIn3s(self):
        self.collectMateIn3_1()

    def collectMateIn3_1(self):
        board = BoardSCPS.fromFEN(fen=r"7k/p1p3pp/1p1P3r/4p3/1P2P2r/P2R1PqP/3Q1RP1/7K b - - 0 28",
                                  squareRepresentor=Square0X88Representor())
        moveRepresentation = OOPMoveRepresentation()
        start = board.getSquareAt(*H4)
        end = board.getSquareAt(*H3)
        move = moveRepresentation.generateCapture(board=board, start=start, end=end,
                                                  capturedPiece=board.getPieceOn(end),
                                                  movingPiece=board.getPieceOn(start))
        self.tests.append(CorrectnessAndPerformanceTest(board=board,
                                                        name="Mate in 3 (1)",
                                                        correctMove=move,
                                                        moveRepresentation=moveRepresentation))

    def collectPuzzles(self):
        self.collectPuzzle1()
        self.collectPuzzle2()
        self.collectPuzzle3()

    def collectPuzzle1(self):
        board = BoardSCPS.fromFEN(fen="6r1/1p5p/p7/3P3p/2P1pk1P/1P6/P4K2/6R1 b - - 1 38",
                                  squareRepresentor=Square0X88Representor())
        moveRepresentation = OOPMoveRepresentation()
        start = board.getSquareAt(*E4)
        end = board.getSquareAt(*E3)
        move = moveRepresentation.generateMove(board=board, start=start, end=end,
                                               piece=board.getPieceOn(start))
        self.tests.append(CorrectnessAndPerformanceTest(board=board,
                                                        name="Puzzle 1",
                                                        correctMove=move,
                                                        moveRepresentation=moveRepresentation))

    def collectPuzzle2(self):
        board = BoardSCPS.fromFEN(fen=r"7r/p4k2/2p2nRp/1pPp1p1P/5P2/8/PPKB4/8 w - - 0 40",
                                  squareRepresentor=Square0X88Representor())
        moveRepresentation = OOPMoveRepresentation()
        start = board.getSquareAt(*G6)
        end = board.getSquareAt(*F6)
        move = moveRepresentation.generateCapture(board=board, start=start, end=end,
                                                  movingPiece=board.getPieceOn(start),
                                                  capturedPiece=board.getPieceOn(end))
        self.tests.append(CorrectnessAndPerformanceTest(board=board,
                                                        name="Puzzle 2",
                                                        correctMove=move,
                                                        moveRepresentation=moveRepresentation))

    def collectPuzzle3(self):
        board = BoardSCPS.fromFEN(fen=r'1k1rr3/pp3p1R/2p1n1p1/2Pp1q2/P2P4/4PPP1/3Q1KP1/R7 b - - 2 23',
                                  squareRepresentor=Square0X88Representor())
        moveRepresentation = OOPMoveRepresentation()
        start = board.getSquareAt(*E6)
        end = board.getSquareAt(*G5)
        move = moveRepresentation.generateMove(board=board, start=start, end=end,
                                               piece=board.getPieceOn(start),
                                               )
        self.tests.append(CorrectnessAndPerformanceTest(board=board,
                                                        name="Puzzle 3, (middlegame from own game)",
                                                        correctMove=move,
                                                        moveRepresentation=moveRepresentation))

    def collectMiddleGames(self):
        self.collectMiddleGame1()
        self.collectMiddleGame2()
        self.collectMiddleGame3()

    def collectMiddleGame1(self):
        board = BoardSCPS.fromFEN(fen=r"r2qkb1r/pp1nppp1/2p2n1p/3p1b2/2PP1B2/2NBPN2/PP3PPP/R2QK2R b KQkq - 1 7",
                                  squareRepresentor=Square0X88Representor())
        moveRepresentation = OOPMoveRepresentation()
        self.tests.append(CorrectnessAndPerformanceTest(board=board,
                                                        name="Queen's Gambit Declined middlegame",
                                                        correctMove=None,
                                                        moveRepresentation=moveRepresentation))

    def collectMiddleGame2(self):
        board = BoardSCPS.fromFEN(fen=r"r1bq1rk1/ppp1bppp/3p1n2/6B1/2BQP3/8/PPP2PPP/RN3RK1 w - - 6 9",
                                  squareRepresentor=Square0X88Representor())
        moveRepresentation = OOPMoveRepresentation()
        self.tests.append(CorrectnessAndPerformanceTest(board=board,
                                                        name="Scotch middlegame",
                                                        correctMove=None,
                                                        moveRepresentation=moveRepresentation))

    def collectMiddleGame3(self):
        board = BoardSCPS.fromFEN(fen="3r1rk1/p4ppp/1p2b3/2p5/8/2b1P1P1/P4PBP/1RB2RK1 w - - 0 16",
                                  squareRepresentor=Square0X88Representor())
        moveRepresentation = OOPMoveRepresentation()
        self.tests.append(CorrectnessAndPerformanceTest(board=board,
                                                        name="Middlegame 3",
                                                        correctMove=None,
                                                        moveRepresentation=moveRepresentation))
