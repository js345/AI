import numpy as np
from search import search
class player:
    def __init__(self, stradegy, evaluation,depth,ID ,workers):
        self.ID = ID
        self.opponent = 3-ID
        self.stradegy = stradegy
        self.evaluation = evaluation
        self.depth = depth
        self.piece = 16
        self.expendedNodes = 0
        self.move = 0
        self.capture = 0
        self.workers = workers




    def move(self,board):
        bestHeu = 0
        res = None
        cap_num = 0
        for (x,y) in self.workers:
            boards = self.nextBoard(board,x,y)
            for (ib,cap) in boards:
                cur = self.findBest(ib,self.depth-1) # best heuristic for current board
                if cur > bestHeu:
                    bestHeu = cur
                    res = board
                    cap_num = cap
        self.move += 1
        self.capture += cap_num
        return










