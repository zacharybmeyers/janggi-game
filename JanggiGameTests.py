# Author:       Zachary Meyers
# Date:         2021-03-01
# Description:

import unittest
from JanggiGame import JanggiGame, algebraic_to_numeric, numeric_to_algebraic


class UnitTests(unittest.TestCase):
    def setUp(self):
        self.game = JanggiGame()

    def test_algebraic_to_numeric(self):
        alg1 = "a1"
        alg2 = "e5"
        self.assertEqual((0, 0), algebraic_to_numeric(alg1))
        self.assertEqual((4, 4), algebraic_to_numeric(alg2))

    def test_numeric_to_algebraic(self):
        num1 = (0, 0)
        num2 = (4, 4)
        self.assertEqual("a1", numeric_to_algebraic(num1))
        self.assertEqual("e5", numeric_to_algebraic(num2))

    def test_get_square_contents(self):
        board = self.game.get_board()
        self.assertEqual(board[0][0], self.game.get_square_contents("a1"))

    def test_solider_blocked_by_same_color(self):
        # blue soldier at b7 can't move to c7 (occupied by another blue soldier)
        self.game.make_move("a7", "b7")                     # move a7 to b7
        self.game.set_turn("b")                             # reset turn
        b7_valid_moves = [(5, 1), (6, 0)]
        b7_b_sold = self.game.get_square_contents("b7")     # get piece object
        self.assertEqual(b7_valid_moves, b7_b_sold.get_valid_moves())

    def test_soldier_stays_on_board(self):
        # blue soldier at A7 can't move off board
        a7_b_sold = self.game.get_square_contents("a7")
        blue_moves = [(5, 0), (6, 1)]
        self.assertEqual(blue_moves, a7_b_sold.get_valid_moves())

        # red soldier at A4 can't move off board
        a4_r_sold = self.game.get_square_contents("a4")
        red_moves = [(4, 0), (3, 1)]
        self.assertEqual(red_moves, a4_r_sold.get_valid_moves())

    def test_soldier_diagonal_fortress(self):
        # move blue soldier from C7 to D3 (red fortress inner corner)
        self.game.make_move("c7", "d7")
        self.game.set_turn("b")
        self.game.make_move("d7", "d6")
        self.game.set_turn("b")
        self.game.make_move("d6", "d5")
        self.game.set_turn("b")
        self.game.make_move("d5", "d4")
        self.game.set_turn("b")
        self.game.make_move("d4", "d3")
        self.game.set_turn("b")
        d3_b_sold = self.game.get_square_contents("d3")
        # check move diagonal to red fortress center is valid
        self.assertIn((1, 4), d3_b_sold.get_valid_moves())

        # move the same blue solider into red fortress center
        self.game.make_move("d3", "e2")
        self.game.set_turn("b")
        e2_b_sold = self.game.get_square_contents("e2")
        # check moves diagonal to red fortress outer corners are valid
        outer_corners = [(0, 3), (0, 5)]
        self.assertIn(outer_corners[0], e2_b_sold.get_valid_moves())
        self.assertIn(outer_corners[1], e2_b_sold.get_valid_moves())

    def test_soldier_capture(self):
        self.game.make_move("a7", "a6")     # bSd to A6
        self.game.make_move("a4", "a5")     # rSd to A5
        self.game.make_move("a6", "a5")     # bSd capture A5
        a5_sd = self.game.get_square_contents("a5")
        self.assertEqual("b", a5_sd.get_color())

    def test_general_moves(self):
        # blue center to outer
        self.assertTrue(self.game.make_move("e9", "d8"))
        self.game.make_move("e9", "d8")
        self.game.set_turn("b")
        # blue outer back to center
        self.assertTrue(self.game.make_move("d8", "e9"))
        self.game.make_move("d8", "e9")
        self.game.set_turn("b")
        # blue center to guard position (same color, blocked)
        self.assertFalse(self.game.make_move("e9", "d10"))
