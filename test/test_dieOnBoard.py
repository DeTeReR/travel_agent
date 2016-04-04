from unittest import TestCase
import unittest

from src.die import DieOnBoard


class TestDieOnBoard(TestCase):
	def setUp(self):
		self._die = DieOnBoard()
		for i in range(1, 7):
			self._die._faces[i] = i

	def test_top_if_move(self):
		for direction in ['east', 'west', 'north' , 'south']:
			for i in range(4):
				self._die.move(direction)
			self.assertEqual(self._die.top(), 1)

	# def test_move(self):
	# 	self.fail()
	#
	# def test_set_top(self):
	# 	self.fail()

if __name__ == '__main__':
	unittest.main()
