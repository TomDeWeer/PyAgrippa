from pathlib import Path
from typing import List, Any
from random import choice
from PyAgrippa.AI.AI import ChessMachine, IChessMachineResult
from PyAgrippa.AI.MoveComputationError import MoveComputationError
from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Moves.MoveGeneration.AllMoveGenerator import AllMoveGenerator
from PyAgrippa.Moves.MoveRepresentation import IMoveRepresentation
import chess
import chess.polyglot


class OpeningBookResult(IChessMachineResult):
    def __init__(self, move: Any):
        self.move = move

    def getBestMove(self):
        return self.move


class OpeningBookExplorer(ChessMachine):
    def __init__(self, moveRepresentation: IMoveRepresentation, verbose: bool = True):
        ChessMachine.__init__(self, moveRepresentation=moveRepresentation)
        self.verbose = verbose
        self.moveGenerator = AllMoveGenerator(moveRepresentation=moveRepresentation)
        openingBookDir = Path(__file__).parent / 'OpeningBooks'
        self.bookPaths = []
        for openingBookPath in openingBookDir.glob('*.bin'):
            self.bookPaths.append(openingBookPath)

    def findBookMoves(self, board: IBoard) -> List[Any]:
        fen = board.toFEN()
        pychess_board = chess.Board(fen)
        pychess_entries = []
        for bookPath in self.bookPaths:
            try:
                reader = chess.polyglot.open_reader(bookPath)
            except FileNotFoundError as err:
                raise MoveComputationError(f"Book at location {bookPath} not found.")
            pychess_entries += list(reader.find_all(pychess_board))
        pychess_ucis = list(set([entry.move.uci() for entry in pychess_entries]))
        allPossibleMoves = self.moveGenerator.generatePseudoLegalMoves(board=board)
        bookMoves = []
        for move in allPossibleMoves:
            if self.getMoveRepresentation().toUCI(move) in pychess_ucis:
                bookMoves.append(move)
        if self.verbose:
            print(f'Found {len(bookMoves)} book moves.')
        return bookMoves

    def computeBestMove(self, board: IBoard) -> IChessMachineResult:
        bookMoves = self.findBookMoves(board=board)
        if len(bookMoves) == 0:
            raise MoveComputationError('No opening book entry for this board.')
        else:
            randomBookMove = choice(bookMoves)
            return OpeningBookResult(move=randomBookMove)
