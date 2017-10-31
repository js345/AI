import numpy as np
from random import random
import copy
import math


class Board:
	def __init__(self):
		self.state = self.init_state()

	# self.worker1 = 16
	# self.worker2 = 16

	def __str__(self):
		s = ""
		for row in self.state:
			s += ",".join([str(c) for c in row]) + "\n"
		return s

	def init_state(self):
		state = [[0 for x in range(8)] for y in range(8)]
		for i in range(8):
			state[0][i] = 1
			state[1][i] = 1
			state[6][i] = 2
			state[7][i] = 2
		return state

	def nextBoard(self, player, board):
		cur_workers = self.get_workers(player, board)
		opponent = 3 - player
		res = []
		addColumn = [-1, 0, 1]
		tarX = 0
		tarY = 0
		for (x, y) in cur_workers:
			if player == 1:
				if x < len(board.state) - 1:
					tarX = x + 1
			elif player == 2:
				if x >= 1:
					tarX = x - 1
			for c in addColumn:
				tarY = y + addColumn[c]
				if tarY >= 0 and tarY < len(board.state[0]):
					if board.state[tarX][tarY] == player:
						continue
					cur = copy.deepcopy(board)
					cur.state[x][y] = 0
					'''
					if (cur.state[tarX][tarY] == 0):
						cap = 0
					else:
						cap = 1
					'''
					cur.state[tarX][tarY] = player
					# res.append((cur, cap))
					res.append(cur)
		return res

	def get_heuristic(self, player, board):
		if player.evaluation == 'offensive':
			if player.self_designed is True:
				return self.offensive_heuristic_2(player, board)
			else:
				return self.offensive_heuristic_1(player, board)
		else:
			if player.self_designed is True:
				return self.offensive_heuristic_2(player, board)
			else:
				return self.defensive_heuristic_1(player, board)

	def defensive_heuristic_1(self, player, board):
		dist1, dist2, count1, count2 = self.get_heu_info(player.ID)
		return 2 * count1 + random()

	def defensive_heuristic_2(self, player, board):
		dist1, dist2, count1, count2 = self.get_heu_info(player.ID)
		return len(self.get_workers(player.ID, board)) + 2*dist2 + random()

	def offensive_heuristic_1(self, player, board):
		dist1, dist2, count1, count2 = self.get_heu_info(player.ID)
		return 2 * (30 - count2) + random()

	def offensive_heuristic_2(self, player, board):
		dist1, dist2, count1, count2 = self.get_heu_info(player.ID)
		if dist1 == 0 or count2 == 0:
			return 9999
		if dist2 == 0 or count1 == 0:
			return -9999
		return 32 - 2*count2 + 2*(7 - dist1) + random()

	def get_workers(self, playerID, board):
		res = []
		for x in range(8):
			for y in range(8):
				if board.state[x][y] == playerID:
					res.append((x, y))
		return res

	def check_capture(self):
		worker1 = 0
		worker2 = 0
		for i in range(8):
			for j in range(8):
				if self.state[i][j] == 1:
					worker1 += 1
				elif self.state[i][j] == 2:
					worker2 += 1
		return 16 - worker2, 16 - worker1

	def get_heu_info(self, player_id):
		"""
		Get shortest distance of this player's piece to goal
		:param player_id: 
		:type player_id: 
		:return: 
		:rtype: 
		"""
		if player_id == 1:
			target = (7, 0)
		else:
			target = (0, 7)
		dist1, dist2 = 7, 7
		count1, count2 = 0, 0
		for i, row in enumerate(self.state):
			for piece in row:
				if piece == player_id:
					count1 += 1
					dist1 = min(dist1, abs(target[0] - i))
				elif piece == 3 - player_id:
					count2 += 1
					dist2 = min(dist2, abs(target[1] - i))
		return dist1, dist2, count1, count2
