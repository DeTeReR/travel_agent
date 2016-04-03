
class Space(object):
	def __init__(self, value):
		self.value = value
		self.visited = False

	def __str__(self):
		return '%s%s' % (self.value, '_' if self.visited else ' ')

	def __eq__(self, other):
		return self.value == other.value and self.visited == other.visited

	def __hash__(self):
		return hash((self.value, self.visited))


class BoardError(ValueError):
	pass


class Board(object):
	def __init__(self, input_values):
		self.spaces = []
		for row in input_values:
			self.spaces.append([])
			for value in row:
				self.spaces[-1].append(Space(value))

	def __str__(self):
		return '\n'.join(row for row in self.spaces)

	def __eq__(self, other):
		return all(m == o for m, o in zip(self.all_spaces(), other.all_spaces()))

	def __hash__(self):
		return hash(tuple(self.all_spaces()))

	def all_spaces(self):
		for row in self.spaces:
			for space in row:
				yield space

	def limit(self):
		return len(self.spaces), len(self.spaces[0])

	def can_visit(self, row, col):
		try:
			space = self.spaces[row][col]
			return space.visited
		except IndexError:
			return False

	def space(self, row, col):
		return self.spaces[row][col]

	def visit(self, row, col):
		self.spaces[row][col].visited = True
	
	def set_value(self, value, row, col):
		space = self.spaces[row][col]
		if space.value is None:
			space.value = value
		else:
			raise BoardError('Trying to set value of %s to %s' % (space, value))
