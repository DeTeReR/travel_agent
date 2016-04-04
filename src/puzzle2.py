import logging
from collections import namedtuple, OrderedDict
from copy import copy, deepcopy

from die import DieOnBoard
from functools32 import functools32
from puzzle import MOVES

logger = logging.getLogger(__name__)


def solve(game_static, game_state):
	if game_state.die_location[-1] == game_static.end_location:
		return deepcopy(game_state)
	next_state_modifiers = game_static.next_state_modifiers(game_state)
	if not next_state_modifiers:
		return None
	solution = None
	for modifier in next_state_modifiers:
		game_state.modify(modifier)
		solution = solve(game_static, game_state) if solution is None else max(solution,
		                                                                       solve(game_static, game_state))
		game_state.unmod(modifier)
	return solution


class GameStateTuple(object):
	def __init__(self, die_north_index=None, die_top_index=None, die_location=None, visited=None, die_face_values=None):
		self.die_north_index = die_north_index
		self.die_top_index = die_top_index
		self.die_location = die_location
		self.visited = visited
		self.die_face_values = die_face_values


class GameState(GameStateTuple):
	MAIN_STATE_NAMES = ('die_north_index', 'die_top_index', 'die_location')
	def modify(self, modifier):
		for attribute_name in self.MAIN_STATE_NAMES:
			getattr(self, attribute_name).append(getattr(modifier, attribute_name))
		row_col, die_face_index = modifier.visited
		self.visited[row_col] = die_face_index
		if modifier.die_face_values:
			face_index, face_value = modifier.die_face_values
			self.die_face_values[face_index] = face_value

	def unmod(self, modifier):
		for attribute_name in self.MAIN_STATE_NAMES:
			getattr(self, attribute_name).pop()
		self.visited.popitem()
		if modifier.die_face_values:
			self.die_face_values.popitem()

	def __cmp__(self, other):
		if other is None:
			return 1
		return cmp(self.score(), other.score())

	@functools32.lru_cache(1)
	def score(self):
		product = 1
		for die_face_index in self.visited.values():
			space_value = self.die_face_values.get(die_face_index, 0)
			if space_value == 0:
				self.die_face_values[die_face_index] = space_value = 9
			product *= space_value
		return product

class GameStateModifier(GameStateTuple):
	pass


'''
	def next_states(self):
		row, col = self._die_location
		states = []
		for move, (row_move, col_move) in MOVES.iteritems():
			new_row = row + row_move
			new_col = col + col_move
			if not self.board.can_visit(new_row, new_col):
				continue

			space = self.board.space(new_row, new_col)
			die_face = self.die.top_if_move(move)
			if space.value is None:
				if die_face is None:
					# Do better.
					states.extend([self.new_state(move, value) for value in SPACE_VALUES])
				else:
					states.append(self.new_state(move, die_face))
			elif die_face is None:
				states.append(self.new_state(move, space.value))
			elif die_face == space.value:
				states.append(self.new_state(move))
		return states
'''


class GameStatic(object):
	def __init__(self, board_values):
		self.board = board_values
		self._die = DieOnBoard()
		self.end_location = len(board_values) - 1, len(board_values[0]) - 1

	def next_state_modifiers(self, game_state):
		row, col = game_state.die_location[-1]
		modifiers = []
		for move, (row_move, col_move) in MOVES.iteritems():
			new_row = row + row_move
			new_col = col + col_move
			if not ((self.end_location[0] >= new_row >= 0) and (self.end_location[1] >= new_col >= 0)):
				continue
			if (new_row, new_col) in game_state.visited:
				continue
			board_value = self.board[new_row][new_col]
			die_top_index, die_north_index = self._die.result_of_move(
				move,
				top_index=game_state.die_top_index[-1],
				north_index=game_state.die_north_index[-1])
			die_top_value = game_state.die_face_values.get(die_top_index, 0)
			if board_value is 0 or die_top_value == board_value:
				modifiers.append(GameStateModifier(die_north_index=die_north_index,
				                                   die_top_index=die_top_index,
				                                   die_location=(new_row, new_col),
				                                   visited=((new_row, new_col), die_top_index)))
			elif die_top_value is 0:
				modifiers.append(GameStateModifier(die_north_index=die_north_index,
				                                   die_top_index=die_top_index,
				                                   die_location=(new_row, new_col),
				                                   visited=((new_row, new_col), die_top_index),
				                                   die_face_values=(die_top_index, board_value)))
		return modifiers


def main():
	logger.warning('Starting.')

	example_static = GameStatic([
		[3, 4, 1, 7, 5],
		[1, 2, 4, 3, 5],
		[2, 4, 3, 6, 2],
		[9, 5, 7, 2, 3],
		[5, 8, 3, 4, 1],
	])
	big_static = GameStatic([
		[1, 5, 5, 5, 6, 1, 1, 4, 1, 3, 7, 5],
		[3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
		[4, 0, 6, 4, 1, 8, 1, 4, 2, 1, 0, 3],
		[7, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 2],
		[1, 0, 1, 0, 6, 1, 6, 2, 0, 2, 0, 1],
		[8, 0, 4, 0, 1, 0, 0, 8, 0, 3, 0, 5],
		[4, 0, 2, 0, 5, 0, 0, 3, 0, 5, 0, 2],
		[8, 0, 5, 0, 1, 1, 2, 3, 0, 4, 0, 6],
		[6, 1, 0, 0, 0, 0, 0, 0, 0, 3, 0, 6],
		[3, 0, 6, 3, 6, 5, 4, 3, 4, 5, 0, 1],
		[6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
		[2, 1, 6, 6, 4, 5, 2, 1, 1, 1, 7, 1]
	])
	practise_static = GameStatic([
		[3, 4, 1, 7, 5],
		[1, 2, 0, 3, 5],
		[0, 4, 3, 0, 2],
		[0, 5, 0, 2, 3],
		[5, 0, 0, 4, 1],
	])
	static = big_static
	initial_state = GameState(die_north_index=[2],
	                          die_top_index=[1],
	                          die_location=[(0, 0)],
	                          visited=OrderedDict([((0, 0), 1)]),
	                          die_face_values=OrderedDict([(1, static.board[0][0])]))
	result = solve(static, initial_state)
	logger.warning('Solved: score%s\n%s', result.score(), result)


if __name__ == '__main__':
	logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
	main()
