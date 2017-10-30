from player import player
import numpy as np
class board:
    def __init__(self):
        self.state = self.init_state()
        self.curplayer = None
        self.opponent = None
        #self.worker1 = 16
        #self.worker2 = 16

    def init_state(self):
        state = [[0 for x in range(8)] for y in range(8)]
        for i in range(8):
            state[0][i] = 1
            state[1][i] = 1
            state[6][i] = 2
            state[7][i] = 2
        return state


    '''find the result board'''
    def nextBoard(self, player, idx, opponent, depth):
        self.curPlayer = player[idx]
        self.opponent = player[opponent]
        cur_workers = self.get_workers(self.curPlayer.ID)
        bestHeu = 0
        res = None
        cap_num = 0
        for (x, y) in cur_workers:
            boards = self.search(self.state, x, y, self.curPlayer.ID)
            for (ib, cap) in boards:
                cur = self.findBest(ib, depth - 1)  # best heuristic for current board
                if cur > bestHeu:
                    bestHeu = cur
                    res = ib
                    cap_num = cap
        self.curPlayer.move += 1
        self.curPlayer.capture += cap_num
        return res



    '''RETURN a list of next possibe move
        also the should be the final result of the function
        just need to evaluate the heuristic additionally

        input: current board
        current worker coord x and y, id
        return : a list of (next board , opponent captured)

    '''
    def search(self,board, x,y, ID):
        tarX = 0
        tarY = 0
        addColumn = [-1,0,1]
        res  = []
        if ID == 1:
            if x < board.size() - 1:
                tarX == x + 1
                for c in addColumn:
                    tarY = y + addColumn[c]
                    if tarY >= 0 and tarY < board[0].size():
                        cur = board.deepCopy()
                        cur[x][y] = 0
                        if(cur[tarX][tarY] == 0):
                            cap = 0
                        else:
                            cap = 1
                        cur[tarX][tarY] = ID
                        res.append((cur,cap))
        if ID == 2:
            if x >= 1:
                tarX == x - 1
                for c in addColumn:
                    tarY = y + addColumn[c]
                    if tarY >= 0 and tarY < board[0].size():
                        cur = board.deepCopy()
                        cur[x][y] = 0
                        if (cur[tarX][tarY] == 0):
                            cap = 0
                        else:
                            cap = 1
                        cur[tarX][tarY] = ID
                        res.append((cur, cap))
        return res

'''
    Given a list of board,
    find the best one given the evaluation and stradegy and depth
'''
    def findBest(self, player, board, depth):
        if(depth == 0):
            return self.getHeuristic(player, board)






    def getHeuristic(self, player,board):
        if player.evaluation == 1:
            return self.Offensive_Heuristic_1(player,board)
        else:
            return self.Defensive_Heuristic_1(player,board)


    def Defensive_Heuristic_1(self,player, board):
        return 2*self.get_workers(player.ID,board)+ np.random()


    def Offensive_Heuristic_1(self,board):
        return 2 * self.get_workers(player.opponent,board) + np.random()

    '''
        def countWorkers(self,board):
            i = 0   #self
            j = 0   # opponent
            for x in range(8):
                for y in range(8):
                    if board[x][y] == self.ID:
                        i += 1
                    if board[x][y] == 3 - self.ID:
                        j += 1
            return (i,j)

    '''

    def get_workers(self,playerID,board):
        res = []
        for x in range(8):
            for y in range(8):
                if board[x][y] == playerID:
                    res.append((x,y))
        return res
