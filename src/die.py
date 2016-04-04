class Face(object):
	def __init__(self, value=None):
		self.value = value
		self.neighbours = [None] * 4

	def set_neighbour(self, other, neighbour_index):
		self.neighbours[neighbour_index] = other

	def __str__(self):
		return '|%s|' % self.value


class DieOnBoard(object):

	THING = {'north': 2, 'south': 0, 'east': 3, 'west': 1}
	DIE_FACE_MAPPINGS = {1: (2, 3, 5, 4),
						 2: (6, 3, 1, 4),
						 3: (1, 2, 6, 5),
						 4: (1, 5, 6, 2),
						 5: (1, 3, 6, 4),
						 6: (5, 3, 2, 4)}

	def __init__(self, top_value=None):
		# 1 indexed so that this matches a D6.
		self._faces = [None] + [None for i in range(6)]
		self._top_index = 1
		self._faces[self._top_index] = top_value
		self._north_index = 2

	def top_if_move(self, direction):
		_, new_top_index = self._roll_dir_and_new_top_index(direction)
		return self._faces[new_top_index]

	def move(self, direction):
		roll_dir, self._top_index = self._roll_dir_and_new_top_index(direction)
		move_north_marker = direction in {'north', 'south'}
		if move_north_marker:
			self._north_index = self.DIE_FACE_MAPPINGS[self._north_index][roll_dir]

	def _roll_dir_and_new_top_index(self, direction):
		north_from_top_index = self.DIE_FACE_MAPPINGS[self._top_index].index(self._north_index)
		roll_dir = (north_from_top_index + self.THING[direction]) % 4
		new_top_index = self.DIE_FACE_MAPPINGS[self._top_index][roll_dir]
		return roll_dir, new_top_index

	def set_top(self, value):
		ret = True if self._faces[self._top_index] is None else False
		self._faces[self._top_index] = value
		return ret

	def top(self):
		return self._faces[self._top_index]

	def __str__(self):
		neighbours = self.DIE_FACE_MAPPINGS[self._top_index]
		return 'Die(top:%s, neighbours:%s,%s,%s,%s)' % \
			   (self._faces[self._top_index],
				neighbours[0],
				neighbours[1],
				neighbours[2],
				neighbours[3],)
