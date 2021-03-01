# Author:       Zachary Meyers
# Date:         2021-03-01
# Description:

import unittest
from JanggiGame import Piece, Soldier, JanggiGame


class UnitTests(unittest.TestCase):
    def setUp(self):
        self.p1 = Piece("b")
        self.bSold = Soldier("b")
        self.rSold = Soldier("r")
        self.game = JanggiGame()

    def test_remove_out_of_bounds(self):
        # only the first tuple in moves is on the board, all others should be removed
        moves = [(0, 8), (0, -1), (0, 9), (-1, 8), (10, 8)]
        self.assertEqual([(0, 8)], self.p1.remove_out_of_bounds(moves))

    def test_soldier_valid_moves(self):
        # blue soldier in column A
        self.bSold.set_position((6, 0))
        blue_moves = [(5, 0), (6, 1)]
        self.assertEqual(blue_moves, self.bSold.get_valid_moves())
        # red soldier in column A
        self.rSold.set_position((3, 0))
        red_moves = [(4, 0), (3, 1)]
        self.assertEqual(red_moves, self.rSold.get_valid_moves())

    def test_algebraic_to_numeric(self):
        alg1 = "a1"
        alg2 = "e5"
        self.assertEqual((0, 0), self.game.algebraic_to_numeric(alg1))
        self.assertEqual((4, 4), self.game.algebraic_to_numeric(alg2))
