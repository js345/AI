import numpy as np
from mp2.p2.board import Board


class Player:
	def __init__(self, stradegy, evaluation, depth, ID, workers,self_designed):
		self.ID = ID
		self.opponent = 3 - ID
		self.stradegy = stradegy
		self.evaluation = evaluation
		self.depth = depth
		self.piece = 16
		self.expendedNodes = 0
		self.move = 0
		self.capture = 0
		self.workers = workers
		self.self_designed = self_designed

	# mini max
	def take_move(self, board, cur_player, cur_depth):
		if self.stradegy == 'm':
			return self.mini_max(board, cur_player, cur_depth)
		else:
			return self.alpha_beta(board, cur_player, cur_depth)

	def mini_max(self, board, cur_player, cur_depth):
		if cur_depth == self.depth:
			return board.get_heuristic(self, board), board
		self.expendedNodes += 1
		queue = []
		next_level = board.nextBoard(cur_player, board)
		# explore the value of each possible step
		# for (it,cap) in next_level:
		for it in next_level:
			# self.capture += cap
			if cur_depth == 1:
				queue.append(self.take_move(it, 3 - cur_player, 1 + cur_depth))
			else:
				queue.append((self.take_move(it, 3 - cur_player, 1 + cur_depth)[0], board))
		queue = sorted(queue)
		if len(queue) == 0:
			#print("q is empty")
			if cur_player == self.ID:
				res = np.inf
			else:
				res = -np.inf
			#for i in range(8):
			#	print(board.state[i])
			return res, board
		if cur_player == self.ID:
			return queue[-1]
		else:
			return queue[0]

	def alpha_beta(self, board, cur_player, cur_depth):
		if cur_player == self.ID:
			return self.max_val(board, cur_player, cur_depth, -np.inf, np.inf)
		else:
			return self.min_val(board, cur_player, cur_depth, -np.inf, np.inf)

	def max_val(self, board, cur_player, cur_depth, alpha, beta):
		if cur_depth == self.depth:
			return board.get_heuristic(self, board), board
		self.expendedNodes += 1

		max_val = -np.inf
		res = None
		next_level = board.nextBoard(cur_player, board)
		for it in next_level:
			cur_val = self.min_val(it, 3 - cur_player, cur_depth + 1, alpha, beta)
			if cur_val is not None and cur_val[0] > max_val:
				max_val = cur_val[0]
				if cur_depth == 1:
					res = (cur_val[0], it)
				else:
					res = cur_val
			if max_val >= beta:
				return res
			alpha = max(alpha, max_val)

		return res

	def min_val(self, board, cur_player, cur_depth, alpha, beta):
		if cur_depth == self.depth:
			return board.get_heuristic(self, board), board
		self.expendedNodes += 1

		min_val = np.inf
		res = None
		next_level = board.nextBoard(cur_player, board)
		for it in next_level:
			cur_val = self.max_val(it, 3 - cur_player, cur_depth + 1, alpha, beta)
			if cur_val is not None and cur_val[0] < min_val:
				min_val = cur_val[0]
				if cur_depth == 1:
					res = (cur_val[0], it)
				else:
					res = cur_val
			if min_val <= alpha:
				return res
			beta = min(beta, min_val)
		return res
