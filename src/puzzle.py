from copy import deepcopy
import logging
import functools32 as functools32

from board import Board, BoardError
from die import DieOnBoard

logger = logging.getLogger(__name__)

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
		self.board.visit(*self._die_location)
		self.die = DieOnBoard(top_value=self.board.space(*self._die_location).value)

	def __str__(self):
		return 'Die:%s\nScore:%s\nBoard:\n%s' % (str(self.die), self.score(), str(self.board))

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

	def new_state(self, move, value=None):
		state = deepcopy(self)
		state.move(move)
		if value:
			state.die.set_top(value)
			try:
				state.board.set_value(value, *state._die_location)
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
		return self._die_location == self.board.limit()


#@functools32.lru_cache(None)
def solve(state):
	if state.finished():
		return state
	next_states = state.next_states()
	if not next_states:
		return None
	solutions = [s for s in (solve(s) for s in next_states) if s is not None]
	if not solutions:
		return None
	return max(solutions)


def main():
	initial_state = State([
		[3, 4, 1, 7, 5],
		[1, 2, 4, 3, 5],
		[2, 4, 3, 6, 2],
		[9, 5, 7, 2, 3],
		[5, 8, 3, 4, 1],
	])
	big_state = State([
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
	practise_state = State([
		[3, 4, 1, 7, 5],
		[1, 2, 0, 3, 5],
		[0, 4, 3, 0, 2],
		[0, 5, 0, 2, 3],
		[5, 0, 0, 4, 1],
	])
	logger.warning('Starting.')
	logger.warning('Solved: %s', solve(practise_state))

if __name__ == '__main__':
	logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
	main()