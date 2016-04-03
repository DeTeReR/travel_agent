from copy import copy, deepcopy

import functools32 as functools32
from board import Board, BoardError


class Face(object):
	def __init__(self, value=None):
		self.value = value
		self.neighbours = [None] * 4

	def set_neighbour(self, other, neighbour_index):
		self.neighbours[neighbour_index] = other
		other.neighbours[(neighbour_index + 2) % 4] = self

class DieOnBoard(object):
	def __init__(self, top_value=None):
		# 1 indexed so that this matches a D6.
		faces = [None] + [Face()] * 6

		for i, n in enumerate([4, 5, 3, 2]):
			faces[1].set_neighbour(faces[n], i)
			faces[6].set_neighbour(faces[n], (i + 2) % 4)

		self.top = top_value
		self.east = self.west = self.north = self.south = self._bottom = None

	def move(self, direction):
		if direction == 'north':


	def __str__(self):
		return ', '.join([str(x) for x in self.top, self.north, self.east, self.south, self.west, self._bottom])

MOVES = {
	'north': 	(1, 0),
	'south': 	(-1, 0),
	'east': 	(0, 1),
	'west': 	(0, -1)
}
SPACE_VALUES = set(range(1, 10))

class State(object):
	def __init__(self, board_values):
		self.board = Board(board_values)
		self._die_location = (0, 0)
		self.die = DieOnBoard(top_value=self.board.space(*self._die_location).value)


	def __str__(self):
		return 'Die:%s\nScore:%s\nBoard:%s' % (str(self.die), self.score(), str(self.board))

	def __cmp__(self, other):
		return cmp(self.score(), other.score())

	def next_states(self):
		row, col = self._die_location
		states = []
		for move, (row_move, col_move) in MOVES.iteritems():
			new_row = row + row_move
			new_col = col + col_move
			if not self.board.can_visit(new_row, new_col):
				continue

			space = self.board.space(new_row, new_col)
			die_face = getattr(self.die, move)
			if space.value is None:
				if die_face is None:
					states.extend([self.new_state(move, value) for value in SPACE_VALUES])
				else:
					states.append(self.new_state(move, die_face))
			elif die_face is None:
				states.append(self.new_state(move, space.value))
			elif die_face == space.value:
				states.append(self.new_state(move))
		return states

	def new_state(self, move, value=None):
		state = deepcopy(self)
		state.move(move)
		if value:
			self.die.top = self.die.top if self.die.top is not None else value
			try:
				self.board.set_value(value, *self._die_location)
			except BoardError:
				pass
		return state

	def move(self, direction):
		self._die_location = (self._die_location[0] + MOVES[direction][0],
							  self._die_location[1] + MOVES[direction][1])
		self.board.visit(*self._die_location)
		self.die.move(direction)

	def __hash__(self):
		return hash((self.die, self.board))

	def __eq__(self, other):
		return self.die == other.die and self.board == other.board

	@functools32.lru_cache(1)
	def score(self):
		if self._die_location != self.board.limit():
			return None
		product = 1
		for space in (s for s in self.board.all_spaces() if s.visited):
			product *= space.value
		return product

	def finished(self):
		return self.board.die_location == self.board.limit()


@functools32.lru_cache(None)
def solve(state):
	if state.finished():
		return state
	next_states = state.next_states()
	if not next_states:
		return None
	return max(solve(s) for s in next_states)


def main():
	initial_state = State([
		[3, 4, 1, 7, 5],
		[1, 2, 4, 3, 5],
		[2, 4, 3, 6, 2],
		[9, 5, 7, 2, 3],
		[5, 8, 3, 4, 1],
	])
	print solve(initial_state)

if __name__ == '__main__':
	main()