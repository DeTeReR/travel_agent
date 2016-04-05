# ODDLY FAST but wrong?

import logging
from copy import deepcopy

from die import DieOnBoard

logger = logging.getLogger(__name__)

MOVES = {
	'north': 	(1, 0),
	'south': 	(-1, 0),
	'east': 	(0, 1),
	'west': 	(0, -1)
}

class GameState(object):
	def __init__(self, die_north_index=None, die_top_index=None, die_location=None, visited=None, die_face_values=None):
		self.die_north_index = die_north_index
		self.die_top_index = die_top_index
		self.die_location = die_location
		self.visited = visited
		self.die_face_values = die_face_values

	def __str__(self):
		return 'Die:%s\nScore:%s\nVisited:\n%s' % (str(self.die_face_values), self.score(), str(self.visited))

	def score(self):
		product = 1
		for die_face_index in self.visited.values():
			space_value = self.die_face_values.get(die_face_index, 0)
			if space_value == 0:
				space_value = 9
			product *= space_value
		return product


class GameStatic(object):
	def __init__(self, board_values):
		self.board = board_values
		self._die = DieOnBoard()
		self._end_location_row = len(board_values) - 1
		self._end_location_col = len(board_values[0]) - 1

	def next_state_modifiers(self, game_state):
		row, col = game_state.die_location
		modifiers = []
		for move, (row_move, col_move) in MOVES.iteritems():
			new_row = row + row_move
			new_col = col + col_move
			if not ((self._end_location_row >= new_row >= 0) and (self._end_location_col >= new_col >= 0)):
				continue
			if (new_row, new_col) in game_state.visited:
				continue
			board_value = self.board[new_row][new_col]
			die_top_index, die_north_index = self._die.result_of_move(
				move,
				top_index=game_state.die_top_index,
				north_index=game_state.die_north_index)
			die_top_value = game_state.die_face_values.get(die_top_index, 0)
			if board_value is 0 or die_top_value == board_value:
				modifiers.append((die_north_index,
								  die_top_index,
								  (new_row, new_col),
								  None))
			elif die_top_value is 0:
				modifiers.append((die_north_index,
								  die_top_index,
								  (new_row, new_col),
								  board_value))
		return modifiers


def main():
	logger.warning('Starting.')

	example_static = GameStatic([
		[3, 4, 1, 7, 5],
		[1, 2, 4, 3, 5],
		[2, 4, 3, 6, 2],
		[9, 5, 7, 2, 3],
		[5, 8, 3, 4, 1],
	])  # 276480
	big_static = GameStatic([
		[1, 5, 4, 4, 6, 1, 1, 4, 1, 3, 7, 5],
		[3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
		[4, 0, 6, 4, 1, 8, 1, 4, 2, 1, 0, 3],
		[7, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 2],
		[1, 0, 1, 0, 6, 1, 6, 2, 0, 2, 0, 1],
		[8, 0, 4, 0, 1, 0, 0, 8, 0, 3, 0, 5],
		[4, 0, 2, 0, 5, 0, 0, 3, 0, 5, 0, 2],
		[8, 0, 5, 0, 1, 1, 2, 3, 0, 4, 0, 6],
		[6, 0, 1, 0, 0, 0, 0, 0, 0, 3, 0, 6],
		[3, 0, 6, 3, 6, 5, 4, 3, 4, 5, 0, 1],
		[6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
		[2, 1, 6, 6, 4, 5, 2, 1, 1, 1, 7, 1],
	])  # 3354674163673461017691780032809373762464467910656
	medium_static = GameStatic([
		[4, 0, 6, 4, 1, 8, 1, 4, 2, 1, 0, 3],
		[7, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 2],
		[1, 0, 1, 0, 6, 1, 6, 2, 0, 2, 0, 1],
		[8, 0, 4, 0, 1, 0, 0, 8, 0, 3, 0, 5],
		[4, 0, 2, 0, 5, 0, 0, 3, 0, 5, 0, 2],
		[8, 0, 5, 0, 1, 1, 2, 3, 0, 4, 0, 6],
		[6, 1, 0, 0, 0, 0, 0, 0, 0, 3, 0, 6],
		[3, 0, 6, 3, 6, 5, 4, 3, 4, 5, 0, 1],
	])  # 10223359979859933659136  / 113592888665110373990400000000?
	practise_static = GameStatic([
		[3, 4, 1, 7, 5],
		[1, 2, 0, 3, 5],
		[0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0],
		[0, 4, 3, 0, 2],
		[0, 5, 0, 2, 3],
		[5, 0, 0, 4, 1],
	])  # 816293376000
	static_one_zero = GameStatic([
		[3, 4, 1, 7, 5],
		[1, 2, 0, 3, 5],
		[2, 4, 3, 6, 2],
		[9, 5, 7, 2, 3],
		[5, 8, 3, 4, 1],
	])  # 622080
	mini_static = GameStatic([[0, 0, 0]])

	static = big_static

	initial_state = GameState(die_north_index=2,
							  die_top_index=1,
							  die_location=(0, 0),
							  visited={(0, 0): 1},
							  die_face_values={1: static.board[0][0]})

	best_solution = [None]

	def solve(game_static, game_state):
		if game_state.die_location == (game_static._end_location_row, game_static._end_location_col):
			if best_solution[0] is None or game_state.score() > best_solution[0].score():
				best_solution[0] = deepcopy(game_state)
		next_state_modifiers = game_static.next_state_modifiers(game_state)
		if not next_state_modifiers:
			return None
		for die_north_index, die_top_index, die_location, new_die_face_value in next_state_modifiers:
			game_state.die_north_index = die_north_index
			game_state.die_top_index = die_top_index
			game_state.die_location = die_location
			game_state.visited[die_location] = die_top_index
			if new_die_face_value:
				game_state.die_face_values[die_top_index] = new_die_face_value
			solve(game_static, game_state)

			del game_state.visited[die_location]
			if new_die_face_value:
				del game_state.die_face_values[die_top_index]

	solve(static, initial_state)

	logger.warning('Solved: %s', best_solution[0])


if __name__ == '__main__':
	logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
	main()
