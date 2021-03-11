# Author:       Zachary Meyers
# Date:         2021-03-01
# Description:  Unit tests for JanggiGame, namely all the potential moves and methods.

import unittest
from JanggiGame import JanggiGame, Soldier, Chariot, Horse, Elephant


class UnitTests(unittest.TestCase):
    def test_algebraic_to_numeric(self):
        game = JanggiGame()
        alg1 = "a1"
        alg2 = "e5"
        alg3 = "d10"
        self.assertEqual((0, 0), game.algebraic_to_numeric(alg1))
        self.assertEqual((4, 4), game.algebraic_to_numeric(alg2))
        self.assertEqual((9, 3), game.algebraic_to_numeric(alg3))

    def test_numeric_to_algebraic(self):
        game = JanggiGame()
        num1 = (0, 0)
        num2 = (4, 4)
        num3 = (9, 3)
        self.assertEqual("a1", game.numeric_to_algebraic(num1))
        self.assertEqual("e5", game.numeric_to_algebraic(num2))
        self.assertEqual("d10", game.numeric_to_algebraic(num3))

    def test_get_square_contents(self):
        game = JanggiGame()
        board = game.get_board()
        self.assertEqual(board[0][0], game.get_square_contents("a1"))

    def test_set_square_contents(self):
        game = JanggiGame()
        # assign a new red soldier to an empty square
        new_sold = Soldier(game, "r")
        game.set_square_contents("d9", new_sold)
        self.assertEqual(new_sold, game.get_square_contents("d9"))

    def test_solider_blocked_by_same_color(self):
        game = JanggiGame()
        # blue soldier at b7 can't move to c7 (occupied by another blue soldier)
        game.make_move("a7", "b7")                     # move a7 to b7
        game.set_turn("b")                             # reset turn
        b7_valid_moves = [(5, 1), (6, 0), (6, 1)]
        b7_b_sold = game.get_square_contents("b7")     # get piece object
        self.assertEqual(b7_valid_moves, b7_b_sold.get_valid_moves())

    def test_soldier_stays_on_board(self):
        game = JanggiGame()
        # blue soldier at A7 can't move off board
        a7_b_sold = game.get_square_contents("a7")
        blue_moves = [(5, 0), (6, 1), (6, 0)]
        self.assertCountEqual(blue_moves, a7_b_sold.get_valid_moves())

        # red soldier at A4 can't move off board
        a4_r_sold = game.get_square_contents("a4")
        red_moves = [(4, 0), (3, 1), (3, 0)]
        self.assertEqual(red_moves, a4_r_sold.get_valid_moves())

    def test_soldier_diagonal_fortress_center(self):
        game = JanggiGame()
        # make blue soldier at red fortress inner corner
        b_sold = Soldier(game, "b")
        game.set_square_contents("d3", b_sold)
        b_sold.set_position("d3")
        # check move diagonal to red fortress center is valid
        self.assertIn((1, 4), b_sold.get_valid_moves())

    def test_soldier_diagonal_fortress_corner(self):
        game = JanggiGame()
        # make blue soldier at red fortress center
        b_sold = Soldier(game, "b")
        game.set_square_contents("e2", b_sold)
        b_sold.set_position("e2")
        # check moves diagonal to red fortress outer corners are valid
        outer_corners = [(0, 3), (0, 5)]
        self.assertIn(outer_corners[0], b_sold.get_valid_moves())
        self.assertIn(outer_corners[1], b_sold.get_valid_moves())

    def test_soldier_capture(self):
        game = JanggiGame()
        game.make_move("a7", "a6")     # bSd to A6
        game.make_move("a4", "a5")     # rSd to A5
        game.make_move("a6", "a5")     # bSd capture A5
        a5_sd = game.get_square_contents("a5")
        self.assertEqual("b", a5_sd.get_color())

    def test_blue_general_moves(self):
        game = JanggiGame()
        # blue center to outer
        self.assertTrue(game.make_move("e9", "d8"))
        game.make_move("e9", "d8")
        game.set_turn("b")
        # blue outer back to center
        self.assertTrue(game.make_move("d8", "e9"))
        game.make_move("d8", "e9")
        game.set_turn("b")
        # blue center to guard position (same color, blocked)
        self.assertFalse(game.make_move("e9", "d10"))

    def test_red_general_moves(self):
        game = JanggiGame()
        # diagonal fortress move
        game.set_turn("r")
        self.assertTrue(game.make_move("e2", "d3"))

    def test_general_pass_valid(self):
        game = JanggiGame()
        self.assertTrue(game.make_move("e9", "e9"))

    def test_guard_moves(self):
        game = JanggiGame()
        # blue guard to d9
        game.make_move("d10", "d9")
        game.set_turn("b")
        # blue guard tries to leave fortress, False
        self.assertFalse(game.make_move("d9", "c9"))
        game.set_turn("b")
        # blue guard tries to occupy General's piece
        self.assertFalse(game.make_move("d9", "e9"))
        game.set_turn("b")

    def test_guard_capture_clears_check(self):
        game = JanggiGame()
        # blue guard captures enemy soldier
        red_sold = Soldier(game, "r")                  # make new red soldier
        game.set_square_contents("d9", red_sold)       # move it to d9 (causing check!)
        red_sold.set_position("d9")
        self.assertTrue(game.make_move("d10", "d9"))   # move guard to capture red soldier and remove check

    def test_chariot_orthogonal_moves(self):
        game = JanggiGame()
        b_char = Chariot(game, "b")                    # make new blue chariot
        game.set_square_contents("e6", b_char)         # move it to e6
        b_char.set_position("e6")
        valid_moves = [(5, 0), (5, 1), (5, 2), (5, 3), (5, 5), (5, 6), (5, 7), (5, 8), (4, 4), (3, 4), (5, 4)]
        self.assertCountEqual(valid_moves, b_char.get_valid_moves())

    def test_chariot_diagonal_to_center(self):
        game = JanggiGame()
        b_char = Chariot(game, "b")                # make new blue chariot
        game.set_square_contents("d3", b_char)     # move it to d3 (fortress corner)
        b_char.set_position("d3")

        red_gen = game.get_square_contents("e2")   # get rGn
        game.set_square_contents("e2", None)       # clear rGn at e2
        game.set_square_contents("f2", red_gen)    # move to f2
        red_gen.set_position("f2")

        self.assertTrue(game.make_move("d3", "e2"))

    def test_chariot_diagonal_two_squares(self):
        game = JanggiGame()
        b_char = Chariot(game, "b")  # make new blue chariot
        game.set_square_contents("d3", b_char)  # move it to d3 (fortress corner)
        b_char.set_position("d3")

        red_gen = game.get_square_contents("e2")  # get rGn
        game.set_square_contents("e2", None)  # clear rGn at e2
        game.set_square_contents("f2", red_gen)  # move to f2
        red_gen.set_position("f2")

        self.assertTrue(game.make_move("d3", "f1"))

    def test_horse_capture_move(self):
        game = JanggiGame()
        # blue horse at d4
        b_horse = Horse(game, "b")
        game.set_square_contents("d4", b_horse)
        b_horse.set_position("d4")
        self.assertIn((1, 4), b_horse.get_valid_moves())

    def test_horse_orthogonal_in_bounds_diagonal_out_of_bounds(self):
        game = JanggiGame()
        b_horse = Horse(game, "b")
        game.set_square_contents("c9", b_horse)    # create blue horse at c9
        b_horse.set_position("c9")                      # set position
        game.set_square_contents("c10", None)      # clear horse at c10
        valid_moves = [(6, 1), (6, 3), (9, 4), (7, 4), (7, 0), (8, 2)]
        self.assertCountEqual(valid_moves, b_horse.get_valid_moves())

    def test_elephant_moves(self):
        game = JanggiGame()
        b_ele = Elephant(game, "b")
        game.set_square_contents("d5", b_ele)
        b_ele.set_position("d5")
        valid_moves = [(1, 5), (1, 1), (2, 0), (2, 6), (4, 3)]
        self.assertCountEqual(valid_moves, b_ele.get_valid_moves())

    def test_cannon_jump_over_friendly_color(self):
        game = JanggiGame()
        # make arbitrary moves
        game.make_move("a7", "b7")
        game.make_move("c1", "d3")
        game.make_move("b7", "a7")
        self.assertTrue(game.make_move("b3", "e3"))    # make sure cannon can jump over same color
        game.display_board()
