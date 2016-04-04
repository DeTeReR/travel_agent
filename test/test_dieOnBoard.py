from unittest import TestCase
import unittest

from src.die import DieOnBoard


class TestDieOnBoard(TestCase):
	def setUp(self):
		self._die = DieOnBoard(1)

	def test_top_if_move(self):
		print self._die
		for i in range(2, 7):
			self._die._faces[i] = i

		self._die.move('east')
		print self._die

	# def test_move(self):
	# 	self.fail()
	#
	# def test_set_top(self):
	# 	self.fail()

if __name__ == '__main__':
	unittest.main()
