class DieOnBoard(object):
	THING = {'north': 2, 'south': 0, 'east': 3, 'west': 1}
	DIE_FACE_MAPPINGS = {1: (2, 3, 5, 4),
						 2: (6, 3, 1, 4),
						 3: (1, 2, 6, 5),
						 4: (1, 5, 6, 2),
						 5: (1, 3, 6, 4),
						 6: (5, 3, 2, 4)}

	def _roll_dir_and_new_top_index(cls, direction, top_index, north_index):
		north_from_top_index = cls.DIE_FACE_MAPPINGS[top_index].index(north_index)
		roll_dir = (north_from_top_index + cls.THING[direction]) % 4
		new_top_index = cls.DIE_FACE_MAPPINGS[top_index][roll_dir]
		return roll_dir, new_top_index

	def result_of_move(cls, move, top_index, north_index):
		roll_dir, new_top_index = cls._roll_dir_and_new_top_index(move, top_index, north_index)
		if move == 'north':
			new_north_index = top_index
		elif move == 'south':
			top_from_north_index = cls.DIE_FACE_MAPPINGS[north_index].index(top_index)
			new_north_index = cls.DIE_FACE_MAPPINGS[north_index][(top_from_north_index + 2) % 4]
		else:
			new_north_index = north_index
		return new_top_index, new_north_index,

