import numpy as np
from p2.player import Player
from p2.board import Board
from timeit import default_timer


class Game:
	def __init__(self):
		self.board = Board()
		self.player = self.init_players()  # a list of players
		self.curplayerIdx = 0  # current index of the player
		self.done = False
		self.winner = None
		self.turn = 1

	def init_players(self):
		playerlist = []
		worker1 = []
		worker2 = []
		for x in range(8):
			worker1.append((0, x))
			worker1.append((1, x))
			worker2.append((6, x))
			worker2.append((7, x))
		playerlist.append(Player('m','offensive', 4, 1, worker1,False))
		playerlist.append(Player('ab','offensive', 5, 2, worker2,False))
		return playerlist

	def checkDone(self, board):
		state = board.state
		for x in range(8):
			if state[0][x] == 2:
				return True
			elif state[7][x] == 1:
				return True

		worker1 = 0
		worker2 = 0
		for x in range(8):
			for y in range(8):
				if state[x][y] == 1:
					worker1 += 1
				if state[x][y] == 2:
					worker2 += 1

		return worker1 == 0 or worker2 == 0

	def next_player(self):
		self.curplayerIdx = 1 - self.curplayerIdx
		return self.curplayerIdx

	def simulate(self):
		total = default_timer()
		while True:
			# for i in range(10):
			curplayer = self.player[self.curplayerIdx]
			# print(curplayer.ID)
			start = default_timer()
			heu, self.board = curplayer.take_move(self.board, curplayer.ID, 1)
			# end = time()
			#self.print_board()
			#print(str(self.turn) + " " + str(default_timer() - start) + "s  " + str(curplayer.ID))
			self.done = self.checkDone(self.board)
			if self.done:
				self.winner = curplayer.ID
				break
			self.curplayerIdx = 1 - self.curplayerIdx
			self.turn += 1
		self.print_board()
		print("total time used = " + str(default_timer() - total))
		print("player1 expends " + str(self.player[0].expendedNodes))
		print("player2 expends " + str(self.player[1].expendedNodes))
		print("winner  is: player" + str(self.winner))
		player1_cap, player2_cap = self.board.check_capture()
		print("player1 captured: " + str(player1_cap))
		print("player2 captured: " + str(player2_cap))
		print("total turn" + str(self.turn))

	def print_board(self):
		state = self.board.state
		print("------------")
		for i in range(8):
			print(state[i])


if __name__ == "__main__":
	game = Game()
	game.simulate()
