class Face(object):
	def __init__(self, value=None):
		self.value = value
		self.neighbours = [None] * 4

	def set_neighbour(self, other, neighbour_index):
		self.neighbours[neighbour_index] = other
		other.neighbours[(neighbour_index + 2) % 4] = self

	def __str__(self):
		return '|%s|' % self.value


class DieOnBoard(object):
	NEW_TOP = {'north': 2, 'south': 0, 'east': 3, 'west': 1}
	NEW_NORTH = {'north': 2, 'south': 0}
	def __init__(self, top_value=None):
		# 1 indexed so that this matches a D6.
		faces = [None] + [Face() for i in range(6)]
		side_faces = [4, 5, 3, 2]
		for i, n in enumerate(side_faces):
			faces[1].set_neighbour(faces[n], i)
			faces[6].set_neighbour(faces[n], (i + 2) % 4)
			faces[n].set_neighbour(faces[side_faces[(i + 1) % 4]], 1)
		self._top = faces[1]
		self._top.value = top_value
		self._north = faces[4]

	def top_if_move(self, direction):
		return self._top.neighbours[self.NEW_TOP[direction]].value

	def move(self, direction):
		self._top = self._top.neighbours[self.NEW_TOP[direction]]
		self._north = self._north.neighbours[self.NEW_NORTH[direction]] if direction in self.NEW_NORTH else self._north

	def set_top(self, value):
		ret = True if self._top.value is None else False
		self._top.value = value
		return ret

	def __str__(self):
		return 'Die(top:%s, rest:%s,%s,%s,%s' % ((self._top,) + tuple(self._top.neighbours))