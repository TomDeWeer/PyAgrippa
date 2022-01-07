from typing import List, Any

from PyAgrippa.AI.AI import IChessMachineResult
from PyAgrippa.AI.AlphaBeta.AlphaBetaEntry import AlphaBetaEntry


class AlphaBetaResult(IChessMachineResult):
    def __init__(self, principalVariation: List[Any], score: float, alpha: float, beta: float):
        self.score = score
        self.principalVariation = principalVariation
        self.alpha = alpha
        self.beta = beta

    def getBestMove(self):
        return self.principalVariation[0]

    def getPrincipalVariation(self):
        return self.principalVariation

    def getEvaluation(self):
        return self.score
