
import math, random


class State:

	paddle_height = 0.2

	def __init__(self, ball_x, ball_y, velocity_x, velocity_y, paddle_y):
		self.ball_x = ball_x
		self.ball_y = ball_y
		self.velocity_x = velocity_x
		self.velocity_y = velocity_y
		self.paddle_y = paddle_y

	def __str__(self):
		vx = '+' if self.velocity_x > 0 else '-'
		vy = '+' if self.velocity_y > 0 else '-'
		if abs(self.velocity_y) < 0.015:
			vy = '0'
		paddle = str(int(math.floor(self.paddle_y*12/(1-State.paddle_height))))
		return ','.join([str(int(self.ball_x*12)), str(int(self.ball_y*12)), vx, vy, paddle])

	def update_ball(self):
		"""
		Update function to update positions
		:return: 0 for normal movements, 1 for bounce, -1 for miss
		:rtype: 
		"""
		self.ball_x += self.velocity_x
		self.ball_y += self.velocity_y
		if self.ball_y < 0:
			self.ball_y = -self.ball_y
			self.velocity_y = -self.velocity_y
		if self.ball_y > 1:
			self.ball_y = 2 - self.ball_y
			self.velocity_y = -self.velocity_y
		if self.ball_x < 0:
			self.ball_x = -self.ball_x
			self.velocity_x = -self.velocity_x
		if self.ball_x < 1:
			return 0
		if self.ball_y > self.paddle_y + State.paddle_height or self.ball_y < self.paddle_y:
			return -1
		self.ball_x = 2 - self.ball_x
		self.velocity_x = random.uniform(-0.015, 0.015) - self.velocity_x
		if abs(self.velocity_x) < 0.03:
			self.velocity_x = 0.03 if self.velocity_x > 0 else -0.03
		self.velocity_y = random.uniform(-0.03, 0.03) - self.velocity_y
		self.velocity_x = max(min(self.velocity_x, 1.0), -1.0)
		self.velocity_y = max(min(self.velocity_y, 1.0), -1.0)
		return 1

	def update_paddle(self, move):
		self.paddle_y += move
		self.paddle_y = min(max(0.0, self.paddle_y), 1-State.paddle_height)

	@staticmethod
	def update_reward(state, reward, max_reward, alpha=1, c=65, gamma=0.88):
		"""
		Update state rewards and action counts of states
		:param state: state in string representation
		:type state: 
		:param reward: reward number
		:type reward: 
		:param max_reward: maximum reward found so far in this state
		:type max_reward: 
		:param c: decay constant
		:type c: 
		:param gamma: discount factor
		:type gamma: 
		:return: 
		:rtype: 
		"""
		# update number of actions done so far to this state
		actions[state] = actions.get(state, 0.0) + 1.0
		# compute learning rate
		alpha *= c / (c + actions[state])
		rewards[state] = rewards.get(state, 0.0) + alpha*(reward+gamma*max_reward-rewards.get(state, 0.0))

	@staticmethod
	def find_max_reward(state):
		return max([rewards.get(state + str(m), 0.0) for m in range(3)])

	@staticmethod
	def find_best_move(state, greedy=False):
		nums = [rewards.get(state+str(m), 0.0) if greedy else State.explore(rewards.get(state+str(m), 0.0), actions.get(state+str(m), 0.0)) for m in range(3)]
		return random.choice([idx for idx, r in enumerate(nums) if r == max(nums)])

	@staticmethod
	def explore(reward, count, e=70):
		if count >= e:
			return reward
		return 1001


if __name__ == "__main__":
	moves = [-0.04, 0, 0.04]
	rewards, actions = dict(), dict()
	score = 0
	alpha = 1
	for it in range(100000):
		s = State(0.5, 0.5, 0.03, 0.01, 0.5 - State.paddle_height/2)
		prev_s, prev_r = None, 0
		# training
		while True:
			if prev_r < 0:
				State.update_reward(prev_s, prev_r, -1, alpha=alpha)
				score += 1
				break
			curr_s = s.__str__()
			curr_r = s.update_ball()
			if prev_s is not None:
				State.update_reward(prev_s, prev_r, State.find_max_reward(curr_s), alpha=alpha)
			action = State.find_best_move(curr_s)
			prev_s = curr_s + str(action)
			s.update_paddle(moves[action])
			prev_r = curr_r
			score += curr_r
		if it % 1000 == 999:
			print(str(score/1000) + " at round " + str(it+1))
			score = 0
	print(len(actions))
	print(sum(1 for action in actions if actions[action] < 65))
