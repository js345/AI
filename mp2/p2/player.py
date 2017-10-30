import numpy as np
from search import search
from board import board
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




    def take_move(self,board,cur_player,cur_depth):
        self.expendedNodes += 1
        if cur_depth == self.depth:
            '''
            if self.style is 0:
                return (self.heuristic_defensive(board, order, worker), board)
            else:
                return (self.heuristic_offensive(board, order, worker), board)
            '''
        queue = []
        next_level = board.nextBoard(self,cur_player,board)
        # explore the value of each possible step
        for it in next_level:
            queue.append(self.take_move(it, 3 - cur_player, 1 + cur_depth))
        queue = sorted(queue)

        if cur_player == self.ID:
            return queue[-1]
        else:
            return queue[0]



        '''
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
        '''









