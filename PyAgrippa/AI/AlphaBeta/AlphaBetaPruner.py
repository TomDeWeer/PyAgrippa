from copy import copy
from typing import Tuple, Optional, List, Dict, Any

from PyAgrippa.AI.AI import ChessMachine, IChessMachineResult
from PyAgrippa.AI.AlphaBeta.AlphaBetaEntry import AlphaBetaEntry
from PyAgrippa.AI.AlphaBeta.AlphaBetaResult import AlphaBetaResult
from PyAgrippa.AI.HashTables.AlphaBetaTupleInterface import AlphaBetaTupleInterface
from PyAgrippa.AI.HashTables.DecisionLogic.AlphaBetaDecisionMaker import AlphaBetaDecisionMaker
from PyAgrippa.AI.HashTables.DecisionLogic.HashDecision import HashDecision
from PyAgrippa.AI.HashTables.HashTable import HashTable
from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Evaluation.BoardEvaluator import BoardEvaluator
from PyAgrippa.Moves.MoveGeneration.AbstractMoveGenerator import AbstractMoveGenerator
from PyAgrippa.Moves.OOPMoveRepresentation.Move import IMove


class AlphaBetaPruner(ChessMachine):
    def __init__(self, depth: int, moveGenerator: AbstractMoveGenerator, boardEvaluator: BoardEvaluator,
                 hashTableOptions: Dict = None,
                 useIncremental=True,
                 ):
        self.depth = depth
        if hashTableOptions is None:
            self.hashTable = None
            self.hashDecider = None
        else:
            hashTableOptions['entryInterface'] = AlphaBetaTupleInterface()
            self.hashTable: HashTable[Tuple[float, List[Any], int, float, float]] = HashTable.fromOptions(
                **hashTableOptions)
            self.hashDecider = AlphaBetaDecisionMaker()
        self.useIncremental = useIncremental
        self.boardEvaluator = boardEvaluator
        self.moveGenerator = moveGenerator
        ChessMachine.__init__(self, moveRepresentation=moveGenerator.getRepresentation())

    def getBoardEvaluator(self):
        return self.boardEvaluator

    def computeBestMove(self, board: IBoard) -> AlphaBetaResult:
        if self.moveGenerator.supportsKillerMoveInjection():
            self.moveGenerator.resetKillerMoves()
        if self.getBoardEvaluator().supportsIncrementalCalculation() and self.useIncremental:
            self.getBoardEvaluator().initializeIncremental(board=board,
                                                           moveRepresentation=self.getMoveRepresentation())
            useIncremental = True
        else:
            useIncremental = False

        bestScore, principalVariation, depth, ownBestSoFar, otherBestSoFar = \
            self.__getBestMove__(board, useIncremental=useIncremental,
                                 depth=self.depth,
                                 ownBestSoFar=float(
                                     '-inf'),
                                 otherBestSoFar=float(
                                     'inf'))

        return AlphaBetaResult(principalVariation=principalVariation, score=bestScore, alpha=ownBestSoFar,
                               beta=otherBestSoFar)

    def __getBestMove__(self, board: IBoard, depth: int, ownBestSoFar: float, otherBestSoFar: float,
                        useIncremental: bool) \
            -> Tuple[float, List[Any], int, float, float]:
        """
        Scores must be interpreted (in a certain function call) as follows:
        * the current active player wants to maximize it
        * they are relative to the current active player
        """
        evaluator = self.getBoardEvaluator()
        if depth == 0:
            assert not useIncremental  # not possible when incremental algorithm is used, return at depth == 1
            return evaluator.evaluate(board), [], 0, ownBestSoFar, otherBestSoFar
        moveGenerator = self.moveGenerator
        bestPV = None
        origOwnBestSoFar = copy(ownBestSoFar)
        if self.hashTable is not None:
            hashEntry = self.hashTable[board]
            decision = self.hashDecider.decide(entry=hashEntry, entryInterface=self.hashTable.getEntryInterface(),
                                               remainingDepth=depth, otherBestSoFar=otherBestSoFar)
            if decision == HashDecision.CONTINUE:
                pass
            elif decision == HashDecision.RETURN:
                return hashEntry
            elif decision == HashDecision.MOVE_REORDER:
                hashMove = self.hashTable.getEntryInterface().getBestMove(entry=hashEntry)
                moveGenerator.injectHashMove(move=hashMove)
            else:
                raise NotImplementedError
        for move in moveGenerator.generatePseudoLegalMoves(board=board, depth=depth):
            if useIncremental:
                score, subPV = self.__evaluateMove_incremental__(board, depth, evaluator, move,
                                                                 ownBestSoFar, otherBestSoFar, useIncremental)
            else:
                score, subPV = self.__evaluateMove__(board, depth, evaluator, move, ownBestSoFar,
                                                     otherBestSoFar, useIncremental)

            score *= -1  # now score is relative to active player here
            if score >= otherBestSoFar:  # fail-hard beta cutoff
                if moveGenerator.supportsKillerMoveInjection():
                    moveGenerator.injectKillerMove(move, depth=depth)
                pv = [move, ] + subPV if subPV is not None else [move, ]
                result = score, pv, depth, origOwnBestSoFar, otherBestSoFar
                if self.hashTable is not None:
                    self.hashTable.__add__(board=board, value=result)
                return result
            if score > ownBestSoFar:
                ownBestSoFar = score
                bestPV = [move, ] + subPV if subPV is not None else [move, ]
        result = ownBestSoFar, bestPV, depth, origOwnBestSoFar, otherBestSoFar
        if self.hashTable is not None:
            self.hashTable.__add__(board=board, value=result)
        return result

    def __evaluateMove__(self,
                         board: IBoard,
                         depth: int,
                         evaluator: BoardEvaluator,
                         move: Any,
                         ownBestSoFar,
                         otherBestSoFar,
                         useIncremental):
        moveRepresentation = self.moveGenerator.getRepresentation()
        moveRepresentation.applyMove(move)
        if board.isGameOver():
            score = evaluator.evaluate(board)
            subPV = []
        else:
            score, subPV, _, _, _ = self.__getBestMove__(board, depth=depth - 1,
                                                         ownBestSoFar=-otherBestSoFar,
                                                         otherBestSoFar=-ownBestSoFar,
                                                         useIncremental=useIncremental)
        moveRepresentation.undoMove(move)
        return score, subPV

    def __evaluateMove_incremental__(self,
                                     board,
                                     depth,
                                     evaluator,
                                     move,
                                     ownBestSoFar,
                                     otherBestSoFar,
                                     useIncremental):
        moveRepresentation = self.moveGenerator.getRepresentation()
        if depth == 1:  # don't go until depth=0, applying last move is not necessary
            evaluator.evaluateMove(move)
            score = evaluator.getScore()
            subPV = []
            evaluator.undoLast()
        else:
            evaluator.evaluateMove(move)
            # print(f'Depth {depth}: applying {move}')
            moveRepresentation.applyMove(move)
            # board.checkValidity()
            if board.isGameOver():
                score = evaluator.getScore()
                subPV = []
            else:
                score, subPV, _, _, _ = self.__getBestMove__(board,
                                                             depth=depth - 1,
                                                             ownBestSoFar=-otherBestSoFar,
                                                             otherBestSoFar=-ownBestSoFar,
                                                             useIncremental=useIncremental)
            # print(f'Depth {depth}: undoing {move}')
            moveRepresentation.undoMove(move)
            evaluator.undoLast()
        return score, subPV
