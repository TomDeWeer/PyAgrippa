from typing import Any

from PyAgrippa.AI.HashTables.AlphaBetaHashEntryInterface import AlphaBetaHashEntryInterface
from PyAgrippa.AI.HashTables.DecisionLogic.HashDecision import HashDecision
# from PyAgrippa.AI.HashTables.DecisionLogic.HashDecisionMaker import HashDecisionMaker


class AlphaBetaDecisionMaker:
    def decide(self, entry: Any, entryInterface: AlphaBetaHashEntryInterface, remainingDepth: int, otherBestSoFar: float) -> HashDecision:
        if entry is None:
            return HashDecision.CONTINUE
        if entryInterface.nodeFailedLow(entry=entry):
            return HashDecision.CONTINUE
        hashDepth = entryInterface.getDepth(entry=entry)
        if hashDepth < remainingDepth:  # not enough depth, use the move ordering
            return HashDecision.MOVE_REORDER
        else:
            if entryInterface.nodeIsExact(entry=entry):
                return HashDecision.RETURN
            elif entryInterface.isCutNode(entry=entry):
                hashScore = entryInterface.getScore(entry)  # todo: technically, you're twice looking up hashScore here. A micro-optimization is possible here (if ever needed).
                if hashScore >= otherBestSoFar:  # beta cutoff
                    return HashDecision.RETURN  # todo: verify once I'm fully awake that I'm not returning too loose alpha beta bounds here
                else:
                    return HashDecision.CONTINUE
            else:
                raise RuntimeError('Nodes should be either exact, cut nodes or fail low.')
        # todo: make sure that < <= > >= are properly decided...


        # 1) no hash entry -> A) continue
        # 2) hash entry but the alpha was too high and thus couldnt be improved (i.e. no best move found) -> A) (todo: although one could try to still try to return something?)
        # 3) hash entry does not have the depth required (strictly less than required depth) -> C) put the hash move in the move ordering (there is one or else we'd be in option 2)
        # 4) hash entry has enough depth (at least the remaining depth)
        #     a) exact result -> B) return
        #     b) no move found -> not possible! should be option nb 2
        #     c) hashScore is a lower bound
        #       x) hashScore is larger than otherBestSoFar -> beta cutoff (hash move is better than opponent options, and will never be played) -> B)
        #       y) hashScore is smaller than otherBestSoFar -> hash move was good enough for cutoff back then, but not now -> C) put the hash move in the move ordering
