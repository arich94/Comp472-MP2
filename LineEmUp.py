# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python
#based on skeleton-tictactoe.py provided in class

import time
import sys
s_e1_wins = 0
class Game:
	MINIMAX = 0
	ALPHABETA = 1
	HUMAN = 2
	AI = 3
	n = 3
	b = 0
	s = 3
	d1 = 3
	d2 = 3
	t = 7
	a1 = False
	a2 = False
	h1 = False
	h2 = False
	forceLose = [False, 'X']
	blocs = []
	gameTrace = "test.txt"
	record_game = False
	original_out = sys.stdout
	file = None
	heur_evals = 0
	heur_evals_depth1 = []
	heur_evals_depth2 = []
	
	turn_counter = 0
	eTimes = []
	allHeurs = []
	evals_by_depth = []
	avg_depths = []
	recur_depths = []
	tempList = []
	
	def __init__(self, recommend = True):
		#self.initialize_game()
		self.recommend = recommend

	def swap_heuristics(self):
		temp = self.h1
		self.h1 = self.h2
		self.h2 = self.h1

	def average_list(self, lst=[]):
		temp = 0
		if len(lst) != 0:
			for l in range(0, len(lst)):
				temp += lst[l]
			avg = temp/len(lst)
			return avg
		else:
			return 0

	def sum_list(self, lst=[]):
		temp = 0
		for l in range(0, len(lst)):
			temp += lst[l]
		return temp

	def sum_evals_by_depth(self):
		for i in range(0, len(self.evals_by_depth)):
			for j in range(0, len(self.evals_by_depth[i])):
				if(j>=len(self.tempList)):
					self.tempList.append(self.evals_by_depth[i][j])
				else:
					self.tempList[j] += self.evals_by_depth[i][j]
		myStr = ""
		for k in range(0, len(self.tempList)):
			myStr += str(k) + ': ' + str(self.tempList[k]) + ', '
		return myStr

	def get_heur_by_depth(self):
		heur_by_depth = ''
		if(self.player_turn == 'X'):
			for d in range(0, len(self.heur_evals_depth1)):
				if(self.heur_evals_depth1[d]!=0):
					heur_by_depth += str(d) + ': ' + str(self.heur_evals_depth1[d]) + ', '
		else:
			for d in range(0, len(self.heur_evals_depth2)):
				if(self.heur_evals_depth2[d]!=0):
					heur_by_depth += str(d) + ': ' + str(self.heur_evals_depth2[d]) + ', '
		return heur_by_depth

	def get_avergae_heur_depth(self):
		avg = 0.0
		if(self.player_turn == 'X'):
			for d in range(0, len(self.heur_evals_depth1)):
				avg += self.heur_evals_depth1[d]*d
			avg = avg/self.heur_evals
		else:
			for d in range(0, len(self.heur_evals_depth2)):
				avg += self.heur_evals_depth2[d]*d
			avg = avg/self.heur_evals
		return round(avg, 2)

	def valid_board_size(self, size):
		if size < 3 or size > 10:
			return False
		else:
			return True

	def input_board_size(self):
		while True:
			size = int(input('please enter the size of the board between 3 and 10: '))
			if self.valid_board_size(size):
				return size
			else:
				print('The board size is not valid! Try again.')

	def valid_block_number(self, blocks):
		if blocks < 0 or blocks > self.n*2:
			return False
		else:
			return True

	def input_number_blocks(self):
		while True:
			blocks = int(input('Please input a number of blocks between 0 and ' + str(self.n*2) + ': '))
			if self.valid_block_number(blocks):
				return blocks
			else:
				print('This number of blocks is not valid! Try again.')

	def input_block_coords(self, block):
		while True:
			self.draw_board()
			print('Enter block #' + str(block+1) + ' coordinates:')
			bx = int(ord(input('enter the x coordinate: '))-65)
			by = int(input('enter the y coordinate: '))
			if self.is_valid(bx, by):
				self.blocs.append((chr(bx+65), by))
				return (bx,by)
			else:
				print('These block coordinates are not valid! Try again.')

	def valid_win_size(self, win):
		if win < 3 or win > self.n:
			return False
		else:
			return True

	def input_win_size(self):
		while True:
			win = int(input('Please input a winning line size between 3 and ' + str(self.n)+ ': '))
			if self.valid_win_size(win):
				return win
			else:
				print('This is not a valid win size! Try again.')
	
	def validate_depth(self, depth):
		if depth < 1:
			return False
		else:
			return True

	def input_depth(self, player):
		while True:
			depth = int(input('Please input the maximum search depth (minimum 1) for player '+ str(player)+ ': '))
			if self.validate_depth(depth):
				return depth
			else:
				print('This is not a valid depth! Please try again.')

	def input_time(self):
		while True:
			time = int(input('Please input number of seconds your AI may search for a move (minmum 1): '))
			if self.validate_depth(time):
				return time
			else:
				print('This is not a valid time! Please try again.')
	
	def input_min_or_alph(self, player):
		while True:
			min_or_alph = int(input('Please input minimax (0) or alpha-beta (1) for player '+ str(player)+ ': '))
			if (min_or_alph==1 or min_or_alph==0):
				return min_or_alph
			else:
				print('This is not a valid option! Please try again.')

	def input_heur(self, number):
		while True:
			playerInt = int(input('Should player ' + str(number) + ' use heuristic e1 (0) or heuristic e2 (1)?: '))
			if(playerInt==0 or playerInt==1):
				return playerInt
			else:
				print('Invalid input! Please try again')

	def initialize_game(self):
		print('Starting a new game...')
		self.n = self.input_board_size()
		self.current_state = []
		for y in range(0, self.n):
			self.current_state.append([])
			for x in range(0, self.n):
				self.current_state[y].append('.')
		self.b = self.input_number_blocks()
		self.blocs=[]
		for block in range(0, self.b):
			(x, y) = self.input_block_coords(block)
			self.current_state[x][y] = 'B'
		self.s = self.input_win_size()
		self.d1 = self.input_depth(1)
		self.d2 = self.input_depth(2)
		for d in range(0, self.d1+1):
			self.heur_evals_depth1.append(0)
		for d in range(0, self.d2+1):
			self.heur_evals_depth2.append(0)
		self.t = self.input_time()
		self.a1 = bool(self.input_min_or_alph(1))
		self.a2 = bool(self.input_min_or_alph(2))
		self.h1 = bool(self.input_heur(1))
		self.h2 = bool(self.input_heur(2))
		self.gameTrace = "gameTrace-" + str(self.n) + str(self.b) + str(self.s) + str(self.t) + ".txt"
		# Player X always plays first
		self.player_turn = 'X'

	def reset_base_defaults(self):
		self.current_state.clear()
		self.current_state = []
		for y in range(0, self.n):
			self.current_state.append([])
			for x in range(0, self.n):
				self.current_state[y].append('.')
		for b in range(0, len(self.blocs)):
			self.current_state[ord(self.blocs[b][0])-65][self.blocs[b][1]] = 'B'
		self.forceLose = [False, 'X']
		self.heur_evals = []
		self.heur_evals_depth1 = []
		self.heur_evals_depth2 = []
		for d in range(0, self.d1+1):
			self.heur_evals_depth1.append(0)
		for d in range(0, self.d2+1):
			self.heur_evals_depth2.append(0)
		self.turn_counter = 0
		self.eTimes = []
		self.allHeurs = []
		self.evals_by_depth = []
		self.avg_depths = []
		self.recur_depths = []
		self.player_turn = 'X'

	def output_beginning(self, player_x=None,player_o=None):
		if player_x == self.AI:
			playerX = "AI"
		else:
			playerX = "HUMAN"
		if player_o == self.AI:
			playerO = "AI"
		else:
			playerO = "HUMAN"
		if self.h1:
			h1_str = "e2 (complex, slow, accurate)"
		else:
			h1_str = "e1 (simple, fast, inaccurate)"
		if self.h2:
			h2_str = "e2 (complex, slow, accurate)"
		else:
			h2_str = "e1 (simple, fast, inaccurate)"
		original_out = sys.stdout
		file = open(self.gameTrace, "a")
		sys.stdout = file
		print('n=' + str(self.n) + ' b=' + str(self.b) + ' s=' + str(self.s) + ' t=' + str(self.t))
		print('blocs positions = ' + str(self.blocs))
		print()
		print('Player 1: ' + playerX + ' d=' + str(self.d1) + ' a=' + str(self.a1) + ' ' + h1_str)
		print('Player 2: ' + playerO + ' d=' + str(self.d2) + ' a=' + str(self.a2) + ' ' + h2_str)
		file.close()
		sys.stdout = original_out

	def draw_board(self):
		print()
		for y in range(0, self.n+1):
			if(y==0):
				print(" |", end="")
			else:
				print(str(y-1)+"|", end="")
			for x in range(0, self.n):
				if(y==0):
					print(chr(65+x), end="")
				else:
					print(F'{self.current_state[x][y-1]}', end="")
			print()
		print()
		
	def is_valid(self, px, py):
		if px < 0 or px > (self.n-1) or py < 0 or py > (self.n-1):
			return False
		elif self.current_state[px][py] != '.':
			return False
		else:
			return True

	def is_end(self):
		if(self.forceLose[0]==True):
			return self.forceLose[1]
		# Vertical win
		for i in range(0, self.n):
			for j in range(0, (self.n-self.s)+1):
				potentialwin = False
				if(self.current_state[i][j] != '.' and self.current_state[i][j] != 'B'):
					potentialwin = True
					for k in range(0, self.s):
						if(self.current_state[i][j] != self.current_state[i][j+k]):
							potentialwin = False
				if(potentialwin):
					return self.current_state[i][j]
		# Horizontal win
		for i in range(0, (self.n-self.s)+1):
			for j in range(0, self.n):
				potentialwin = False
				if(self.current_state[i][j] != '.' and self.current_state[i][j] != 'B'):
					potentialwin = True
					for k in range(0, self.s):
						if(self.current_state[i][j] != self.current_state[i+k][j]):
							potentialwin = False
				if(potentialwin):
					return self.current_state[i][j]
		# Main diagonal win
		for i in range(0, (self.n-self.s)+1):
			for j in range(0, (self.n-self.s)+1):
				potentialwin = False
				if(self.current_state[i][j] != '.' and self.current_state[i][j] != 'B'):
					potentialwin = True
					for k in range(0, self.s):
						if(self.current_state[i][j] != self.current_state[i+k][j+k]):
							potentialwin = False
				if(potentialwin):
					return self.current_state[i][j]
		# Second diagonal win
		for i in range(0, (self.n-self.s)+1):
			for j in range(self.s-1, (self.n-self.s)+1):
				potentialwin = False
				if(self.current_state[i][j] != '.' and self.current_state[i][j] != 'B'):
					potentialwin = True
					for k in range(0, self.s):
						if(self.current_state[i][j] != self.current_state[i+k][j-k]):
							potentialwin = False
				if(potentialwin):
					return self.current_state[i][j]
		# Is whole board full?
		for i in range(0, self.n):
			for j in range(0, self.n):
				# There's an empty field, we continue the game
				if (self.current_state[i][j] == '.'):
					return None
		# It's a tie!
		return '.'

	def check_end(self):
		global s_e1_wins
		global s_e2_wins
		self.result = self.is_end()
		# Printing the appropriate message if the game has ended
		if self.result != None:
			if self.result == 'X':
				if self.h1:
					s_e2_wins += 1
				else:
					s_e1_wins += 1
				print('The winner is X!')
				if self.record_game:
					self.open_gametrace()
					print('The winner is X!')
					print()
					print('6(b)i\tAverage evaluation time: ' + str(self.average_list(self.eTimes)) + 's')
					print('6(b)ii\tTotal heuristic evaluations: ' + str(self.sum_list(self.allHeurs)))
					print('6(b)iii\tEvaluations by depth: ' + self.sum_evals_by_depth())
					print('6(b)iv\tAverage evaluation depth: ' + str(self.average_list(self.avg_depths)))
					print('6(b)v\tAverage recursion depth: ' + str(self.average_list(self.recur_depths)))
					print('6(b)vi\tTotal moves: ' + str(self.turn_counter))
					print('----------------')
					self.close_gametrace()
			elif self.result == 'O':
				if self.h2:
					s_e2_wins += 1
				else:
					s_e1_wins += 1
				print('The winner is O!')
				if self.record_game:
					self.open_gametrace()
					print('The winner is O!')
					print()
					print('6(b)i\tAverage evaluation time: ' + str(self.average_list(self.eTimes)) + 's')
					print('6(b)ii\tTotal heuristic evaluations: ' + str(self.sum_list(self.allHeurs)))
					print('6(b)iii\tEvaluations by depth: ' + self.sum_evals_by_depth())
					print('6(b)iv\tAverage evaluation depth: ' + str(self.average_list(self.avg_depths)))
					print('6(b)v\tAverage recursion depth: ' + str(self.average_list(self.recur_depths)))
					print('6(b)vi\tTotal moves: ' + str(self.turn_counter))
					print('----------------')
					self.close_gametrace()
			elif self.result == '.':
				print("It's a tie!")
				if self.record_game:
					self.open_gametrace()
					print("It's a tie!")
					print()
					print('6(b)i\tAverage evaluation time: ' + str(self.average_list(self.eTimes)) + 's')
					print('6(b)ii\tTotal heuristic evaluations: ' + str(self.sum_list(self.allHeurs)))
					print('6(b)iii\tEvaluations by depth: ' + self.sum_evals_by_depth())
					print('6(b)iv\tAverage evaluation depth: ' + str(self.average_list(self.avg_depths)))
					print('6(b)v\tAverage recursion depth: ' + str(self.average_list(self.recur_depths)))
					print('6(b)vi\tTotal moves: ' + str(self.turn_counter))
					print('-----------------')
					self.close_gametrace()
		return self.result

	def input_move(self):
		while True:
			print(F'Player {self.player_turn}, enter your move:')
			px = int(ord(input('enter the x coordinate: '))-65)
			py = int(input('enter the y coordinate: '))
			if self.is_valid(px, py):
				return (px,py)
			else:
				print('The move is not valid! Try again.')

	def switch_player(self):
		if self.player_turn == 'X':
			self.player_turn = 'O'
		elif self.player_turn == 'O':
			self.player_turn = 'X'
		return self.player_turn
	
	#simple, fast, less accurate heuristic
	def e1(self, x=0, y=0, depth=0):
		self.heur_evals += 1
		if self.player_turn == 'X':
			self.heur_evals_depth1[self.d1-depth] += 1
		elif self.player_turn == 'O':
			self.heur_evals_depth2[self.d2-depth] += 1
		# Vertical win
		value = 0
		for k in range(0, self.n-y):
			if(self.current_state[x][y+k] == 'X'):
				value -= 1
			elif(self.current_state[x][y+k] == 'O'):
				value += 1
		# Horizontal win
		for k in range(0, self.n-x):
			if(self.current_state[x+k][y] == 'X'):
				value -= 1
			elif(self.current_state[x+k][y] == 'O'):
				value += 1
		if value > 0:
			return 1
		elif value < 0:
			return -1
		else:
			return 0

	#more complex, more accurate, slower heuristic
	def e2(self, x=0, y=0, depth=0):
		self.heur_evals += 1
		if self.player_turn == 'X':
			self.heur_evals_depth1[self.d1-depth] += 1
		elif self.player_turn == 'O':
			self.heur_evals_depth2[self.d2-depth] += 1
		value = 0
		#test vertical win
		v_value = 0
		for i in range(0, self.n):
			for j in range(0, (self.n-self.s)+1):
				if(self.current_state[i][j] != 'B'):
					for k in range(0, self.s):
						if(self.current_state[i][j+k] == 'O' or self.current_state[i][j+k] == '.'):
							v_value = 1
						elif(self.current_state[i][j+k] == 'X'):
							v_value = -1
							break
						elif(self.current_state[i][j+k] == 'B'):
							v_value = 0
							break
		#test horizontal win
		h_value = 0
		for i in range(0, (self.n-self.s)+1):
			for j in range(0, self.n):
				if(self.current_state[i][j] != 'B'):
					for k in range(0, self.s):
						if(self.current_state[i+k][j] == 'O' or self.current_state[i+k][j] == '.'):
							h_value = 1
						elif(self.current_state[i+k][j] == 'X'):
							h_value = -1
							break
						elif(self.current_state[i+k][j] == 'B'):
							h_value = 0
							break
		#test first diagonal win
		d1_value = 0
		for i in range(0, (self.n-self.s)+1):
			for j in range(0, (self.n-self.s)+1):
				if(self.current_state[i][j] != 'B'):
					for k in range(0, self.s):
						if(self.current_state[i+k][j+k] == 'O' or self.current_state[i+k][j+k] == '.'):
							d1_value = 1
						elif(self.current_state[i+k][j+k] == 'X'):
							d1_value = -1
							break
						elif(self.current_state[i+k][j+k] == 'B'):
							d1_value = 0
							break
		#test second diagonal win
		d2_value = 0
		for i in range(0, (self.n-self.s)+1):
			for j in range(self.s-1, (self.n-self.s)+1):
				if(self.current_state[i][j] != 'B'):
					for k in range(0, self.s):
						if(self.current_state[i+k][j-k] == 'O' or self.current_state[i+k][j-k] == '.'):
							d2_value = 1
						elif(self.current_state[i+k][j-k] == 'X'):
							d2_value = -1
							break
						elif(self.current_state[i+k][j-k] == 'B'):
							d2_value = 0
							break
		value = v_value + h_value + d1_value + d2_value
		if(value > 0):
			return 1
		elif(value < 0):
			return -1
		else:
			return 0

	def minimax(self, max=False, depth=3, max_depth=3, heur=False):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		#is max is True, player_turn = 'O'
		list_deps = []

		elapsed = 0
		value = 2
		if max:
			value = -2
		x = None
		y = None
		
		start = time.time()
		result = self.is_end()
		self.heur_evals += 1
		if self.player_turn == 'X':
			self.heur_evals_depth1[self.d1-depth] += 1
		elif self.player_turn == 'O':
			self.heur_evals_depth2[self.d2-depth] += 1
		end = time.time()
		elapsed = end-start
		
		#check if winning condition
		if result == 'X':
			return (-1, x, y, elapsed, max_depth-depth)
		elif result == 'O':
			return (1, x, y, elapsed, max_depth-depth)
		elif result == '.':
			return (0, x, y, elapsed, max_depth-depth)
		#explore nodes
		for i in range(0, self.n):
			for j in range(0, self.n):
				#check depth first
				if(depth == 0 and max):
					if heur:
						value = self.e2(depth=depth)
					else:
						value = self.e1(x=i, y=j, depth=depth)
					return (value, x, y, elapsed, max_depth-depth)
				elif(depth == 0):
					if heur:
						value = self.e2(depth=depth)
					else:
						value = self.e1(x=i, y=j, depth=depth)
					return (value, x, y, elapsed, max_depth-depth)
				#check time
				if(((self.t-elapsed) < (self.t/2)) and max):
					if heur:
						value = self.e2(depth=depth)
					else:
						value = self.e1(x=i, y=j, depth=depth)
					return (value, x, y, elapsed, max_depth-depth)
				elif((self.t-elapsed) < (self.t/2)):
					if heur:
						value = self.e2(depth=depth)
					else:
						value = self.e1(x=i, y=j, depth=depth)
					return (value, x, y, elapsed, max_depth-depth)
				elif self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _, checkTime, dep) = self.minimax(max=False, depth=depth-1, max_depth=max_depth)
						list_deps.append(dep)
						elapsed += checkTime
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _, checkTime, dep) = self.minimax(max=True, depth=depth-1, max_depth=max_depth)
						list_deps.append(dep)
						elapsed += checkTime
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
		temp = 0
		for d in range(0, len(list_deps)):
			temp += list_deps[d]
		avg_depth = temp/len(list_deps)
		return (value, x, y, elapsed, avg_depth)

	def alphabeta(self, alpha=-2, beta=2, max=False, depth=3, max_depth=3, heur=False):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		#if max is True, player_turn = 'O'
		list_deps = []

		elapsed = 0
		value = 2
		if max:
			value = -2
		x = None
		y = None

		start = time.time()
		result = self.is_end()
		if self.player_turn == 'X':
			self.heur_evals_depth1[self.d1-depth] += 1
		elif self.player_turn == 'O':
			self.heur_evals_depth2[self.d2-depth] += 1
		self.heur_evals += 1
		end = time.time()
		elapsed = end - start
		#check end
		if result == 'X':
			return (-1, x, y, elapsed, max_depth-depth)
		elif result == 'O':
			return (1, x, y, elapsed, max_depth-depth)
		elif result == '.':
			return (0, x, y, elapsed, max_depth-depth)
		for i in range(0, self.n):
			for j in range(0, self.n):
				#check depth first
				if(depth == 0 and max):
					if heur:
						value = self.e2(depth=depth)
					else:
						value = self.e1(x=i, y=j, depth=depth)
					return (value, x, y, elapsed, max_depth-depth)
				elif(depth == 0):
					if heur:
						value = self.e2(depth=depth)
					else:
						value = self.e1(x=i, y=j, depth=depth)
					return (value, x, y, elapsed, max_depth-depth)
				#check time
				if(((self.t-elapsed) < (self.t/2)) and max):
					if heur:
						value = self.e2(depth=depth)
					else:
						value = self.e1(x=i, y=j, depth=depth)
					return (value, x, y, elapsed, max_depth-depth)
				elif((self.t-elapsed) < (self.t/2)):
					if heur:
						value = self.e2(depth=depth)
					else:
						value = self.e1(x=i, y=j, depth=depth)
					return (1, x, y, elapsed, max_depth-depth)
				#check nodes
				elif self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _, checkTime, dep) = self.alphabeta(alpha, beta, max=False, depth=depth-1, max_depth=max_depth)
						list_deps.append(dep)
						elapsed += checkTime
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _, checkTime, dep) = self.alphabeta(alpha, beta, max=True, depth=depth-1, max_depth=max_depth)
						list_deps.append(dep)
						elapsed += checkTime
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
					if max: 
						if value >= beta:
							return (value, x, y, elapsed, max_depth-depth)
						if value > alpha:
							alpha = value
					else:
						if value <= alpha:
							return (value, x, y, elapsed, max_depth-depth)
						if value < beta:
							beta = value
		temp = 0
		for d in range(0, len(list_deps)):
			temp += list_deps[d]
		avg_depth = temp/len(list_deps)
		return (value, x, y, elapsed, avg_depth)

	def open_gametrace(self):
		self.original_out = sys.stdout
		self.file = open(self.gameTrace, "a")
		sys.stdout = self.file

	def close_gametrace(self):
		self.file.close()
		sys.stdout = self.original_out

	def add_to_statistics(self):
		s_moves.append(self.turn_counter)
		s_eTimes.append(self.average_list(self.eTimes))
		s_allHeurs.append(self.sum_list(self.allHeurs))
		s_evals_by_depth.append(self.tempList)
		s_avg_depths.append(self.average_list(self.avg_depths))
		s_recur_depths.append(self.average_list(self.recur_depths))

	def play(self,player_x=None,player_o=None,record=False):
		self.reset_base_defaults()
		self.record_game = record
		if record:
			self.output_beginning()
		if player_x == None:
			player_x = self.HUMAN
		if player_o == None:
			player_o = self.HUMAN
		while True:
			self.turn_counter += 1
			self.heur_evals = 0
			for d in range(0, len(self.heur_evals_depth1)):
				self.heur_evals_depth1[d] = 0
			for d in range(0, len(self.heur_evals_depth2)):
				self.heur_evals_depth2[d] = 0
			self.draw_board()
			if record:
				self.open_gametrace()
				self.draw_board()
				self.close_gametrace()
			if self.check_end():
				self.add_to_statistics()
				return
			start = time.time()
			if self.player_turn == 'X':
				if self.a1:
					(m, x, y, _, dep) = self.alphabeta(max=True, depth=self.d1, max_depth=self.d1, heur=self.h1)
				else:
					(_, x, y, _, dep) = self.minimax(max=True, depth=self.d1, max_depth=self.d1, heur=self.h1)
			else:
				if self.a2:
					(m, x, y, _, dep) = self.alphabeta(max=False, depth=self.d2, max_depth=self.d2, heur=self.h2)
				else:
					(_, x, y, _, dep) = self.minimax(max=False, depth=self.d2, max_depth=self.d2, heur=self.h2)
			end = time.time()
			if (self.player_turn == 'X' and player_x == self.HUMAN) or (self.player_turn == 'O' and player_o == self.HUMAN):
					if self.recommend:
						print(F'Evaluation time: {round(end - start, 7)}s')
						print(F'Recommended move: x = {chr(x+65)}, y = {y}')
					(x,y) = self.input_move()
					if record:
						self.open_gametrace()
						print(F'Player {self.player_turn} under HUMAN control plays: x = {chr(x+65)}, y = {y}')
						print()
						print(F'i\tEvaluation time: {round(end - start, 2)}s')
						print(F'ii\tHeuristic evaluations: {self.heur_evals}')
						print(F'iii\tEvaluations by depth: {self.get_heur_by_depth()}')
						print(F'iv\tAverage evaluation depth: {self.get_avergae_heur_depth()}')
						print(F'v\tAverage recursion depth: {round(dep, 2)}')
						self.close_gametrace()
			if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
						print(F'Evaluation time: {round(end - start, 7)}s')
						if(round(end - start, 7) > self.t and self.player_turn == 'X'):
							self.forceLose = [True, 'O']
							if self.check_end():
								self.add_to_statistics()
								return
						if(round(end - start, 7) >self.t and self.player_turn == 'O'):
							self.forceLose = [True, 'X']
							if self.check_end():
								self.add_to_statistics()
								return
						print(F'Player {self.player_turn} under AI control plays: x = {chr(x+65)}, y = {y}')
						if record:
							self.open_gametrace()
							print(F'Player {self.player_turn} under AI control plays: x = {chr(x+65)}, y = {y}')
							print()
							print(F'i\tEvaluation time: {round(end - start, 2)}s')
							print(F'ii\tHeuristic evaluations: {self.heur_evals}')
							print(F'iii\tEvaluations by depth: {self.get_heur_by_depth()}')
							print(F'iv\tAverage evaluation depth: {self.get_avergae_heur_depth()}')
							print(F'v\tAverage recursion depth: {round(dep, 2)}')
							self.close_gametrace()
			self.eTimes.append(round(end-start, 2))
			self.allHeurs.append(self.heur_evals)
			if self.player_turn == 'X':
				self.evals_by_depth.append(self.heur_evals_depth1)
			else:
				self.evals_by_depth.append(self.heur_evals_depth2)
			self.avg_depths.append(self.get_avergae_heur_depth())
			self.recur_depths.append(round(dep, 2))
			self.current_state[x][y] = self.player_turn
			self.switch_player()

s_n = 0
s_b = 0
s_s = 0
s_t = 0
s_d1 = 0
s_d2 = 0
s_a1 = False
s_a2 = False
s_nbGames = 0
s_e1_wins = 0
s_e2_wins = 0
S_FILENAME = "scoreboard.txt"
s_file = None
s_original_out = sys.stdout
s_game_count = 0

s_moves = []
s_eTimes = []
s_allHeurs = []
s_evals_by_depth = []
s_avg_depths = []
s_recur_depths = []

def reset_defaults():
	global s_n
	global s_b
	global s_s
	global s_t
	global s_d1
	global s_d2
	global s_a1
	global s_a2
	global s_nbGames
	global s_e1_wins
	global s_e2_wins
	global s_game_count
	global s_moves
	global s_eTimes
	global s_allHeurs
	global s_evals_by_depth
	global s_avg_depths
	global s_recur_depths
	s_n = 0
	s_b = 0
	s_s = 0
	s_t = 0
	s_d1 = 0
	s_d2 = 0
	s_a1 = False
	s_a2 = False
	s_nbGames = 0
	s_e1_wins = 0
	s_e2_wins = 0
	s_game_count = 0
	s_moves = []
	s_eTimes = []
	s_allHeurs = []
	s_evals_by_depth = []
	s_avg_depths = []
	s_recur_depths = []

def s_open_file():
	global s_original_out
	global s_file
	s_original_out = sys.stdout
	s_file = open(S_FILENAME, "a")
	sys.stdout = s_file

def s_close_file():
	global s_original_out
	global s_file
	s_file.close()
	sys.stdout = s_original_out

def get_game_values(game: Game):
	global s_n
	global s_b
	global s_s
	global s_t
	global s_d1
	global s_d2
	global s_a1
	global s_a2
	if(game==None):
		return
	else:
		s_n = game.n
		s_b = game.b
		s_s = game.s
		s_t = game.t
		s_d1 = game.d1
		s_d2 = game.d2
		s_a1 = game.a1
		s_a2 = game.a2

def s_average_list(lst=[]):
	temp = 0
	if len(lst) != 0:
		for l in range(0, len(lst)):
			temp += lst[l]
		avg = temp/len(lst)
		return avg
	else:
		return 0

def s_sum_list(lst=[]):
	temp = 0
	for l in range(0, len(lst)):
		temp += lst[l]
	return temp

def s_sum_evals_by_depth():
	s_tempList = []
	for i in range(0, len(s_evals_by_depth)):
		for j in range(0, len(s_evals_by_depth[i])):
			if(j>=len(s_tempList)):
				s_tempList.append(s_evals_by_depth[i][j])
			else:
				s_tempList[j] += s_evals_by_depth[i][j]
	myStr = ""
	for k in range(0, len(s_tempList)):
		myStr += str(k) + ': ' + str(s_tempList[k]) + ', '
	return myStr

def write_to_scoreboard():
	s_open_file()
	print('n=' + str(s_n) + ' b=' + str(s_b) + ' s=' + str(s_s) + ' t=' + str(s_t))
	print()
	print('Player 1: d=' + str(s_d1) + ' a=' + str(s_a1))
	print('Player 2: d=' + str(s_d2) + ' a=' + str(s_a2))
	print()
	print(str(s_game_count) + ' games')
	print()
	print('Total wins for heuristic e1: ' + str(s_e1_wins) + '(' + str(round((s_e1_wins/s_game_count)*100, 2)) + ') (fast, simple, inaccurate)')
	print('Total wins for heuristic e2: ' + str(s_e2_wins) + '(' + str(round((s_e2_wins/s_game_count)*100, 2)) + ') (slow, complex, accurate)')
	print()
	print('6(b)i\tAverage evaluation time: ' + str(s_average_list(s_eTimes)) + 's')
	print('6(b)ii\tTotal heuristic evaluations: ' + str(s_sum_list(s_allHeurs)))
	print('6(b)iii\tEvaluations by depth: ' + s_sum_evals_by_depth())
	print('6(b)iv\tAverage evaluation depth: ' + str(s_average_list(s_avg_depths)))
	print('6(b)v\tAverage recursion depth: ' + str(s_average_list(s_recur_depths)))
	print('6(b)vi\tAverage moves per game: ' + str(s_average_list(s_moves)))
	print('-------------------------------------------')
	s_close_file()

def input_player(number):
	while True:
		playerInt = int(input('Should player ' + str(number) + ' be AI (0) or HUMAN (1)?: '))
		if(playerInt==0 or playerInt==1):
			return playerInt
		else:
			print('Invalid input! Please try again')

def main():
	global s_game_count
	g = Game(recommend=True)
	playerOne = input_player(1)
	playerTwo = input_player(2)
	if(playerOne==0):
		playerX = Game.AI
	else:
		playerX = Game.HUMAN
	if(playerTwo==0):
		playerO = Game.AI
	else:
		playerO = Game.HUMAN
		do_record = False
	for j in range(0, 1):
		g.initialize_game()
		for i in range(0, 6):
			if i==0:
				do_record = True
			else:
				do_record = False
			if i == 3:
				g.swap_heuristics()
			g.play(player_x=playerX,player_o=playerO, record=do_record)
			s_game_count += 1
			get_game_values(g)
			g.reset_base_defaults()
		
		write_to_scoreboard()
		reset_defaults()

if __name__ == "__main__":
	main()

