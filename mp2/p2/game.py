import numpy as np
import player
import board
class game:
    def __init__(self):
        self.board = board()
        self.player = self.initplayers() #a list of players
        self.curplayerIdx = 0  # current index of the player
        self.done = False
        self.winner = None

        def initplayers(self):
            playerlist = []
            worker1 = []
            worker2 = []
            for x in range(8):
                worker1.append((0, x))
                worker1.append((1, x))
                worker2.append((6, x))
                worker2.append((7, x))
            playerlist.append = player(0, 0, 3, 1, worker1)
            playerlist.append = player(1, 1, 3, 2, worker2)
            return playerlist

        def checkDone(self, board):
            for x in range(8):
                if board[0][x] == 2:
                    return True
                if board[7][x] == 1:
                    return True
            '''
            worker1 = 0
            worker2 = 0
            for x in range(8):
                for y in range(8):
                    if board[x][y] == 1:
                        worker1 += 1
                    if board[x][y] == 2:
                        worker2 += 1
            '''
            return self.board.worker1 == 0 or self.board.worker2 == 0

        def nextplayer(self):
            self.curplayerIdx = 1 - self.curplayerIdx
            return self.curplayerIdx



        def simulate(self):



            return
