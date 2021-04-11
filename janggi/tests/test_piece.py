#!/usr/bin/env python3

import unittest

from janggi.game import Game
from janggi.piece import Soldier, Chariot, Horse, Elephant


class TestSoldier(unittest.TestCase):
    def test_solider_blocked_by_same_color(self):
        game = Game()
        # blue soldier at b7 can't move to c7 (occupied by another blue soldier)
        game.make_move("a7", "b7")                     # move a7 to b7
        game.set_turn("b")                             # reset turn
        b7_valid_moves = [(5, 1), (6, 0), (6, 1)]
        b7_b_sold = game.get_board().get_square_contents("b7")     # get piece object
        self.assertEqual(b7_valid_moves, b7_b_sold.get_valid_moves())

    def test_soldier_stays_on_board(self):
        game = Game()
        # blue soldier at A7 can't move off board
        a7_b_sold = game.get_board().get_square_contents("a7")
        blue_moves = [(5, 0), (6, 1), (6, 0)]
        self.assertCountEqual(blue_moves, a7_b_sold.get_valid_moves())

        # red soldier at A4 can't move off board
        a4_r_sold = game.get_board().get_square_contents("a4")
        red_moves = [(4, 0), (3, 1), (3, 0)]
        self.assertEqual(red_moves, a4_r_sold.get_valid_moves())

    def test_soldier_diagonal_fortress_center(self):
        game = Game()
        # make blue soldier at red fortress inner corner
        b_sold = Soldier(game.get_board(), "b")
        game.get_board().set_square_contents("d3", b_sold)
        b_sold.set_position("d3")
        # check move diagonal to red fortress center is valid
        self.assertIn((1, 4), b_sold.get_valid_moves())

    def test_soldier_diagonal_fortress_corner(self):
        game = Game()
        # make blue soldier at red fortress center
        b_sold = Soldier(game.get_board(), "b")
        game.get_board().set_square_contents("e2", b_sold)
        b_sold.set_position("e2")
        # check moves diagonal to red fortress outer corners are valid
        outer_corners = [(0, 3), (0, 5)]
        self.assertIn(outer_corners[0], b_sold.get_valid_moves())
        self.assertIn(outer_corners[1], b_sold.get_valid_moves())

    def test_soldier_capture(self):
        game = Game()
        game.make_move("a7", "a6")     # bSd to A6
        game.make_move("a4", "a5")     # rSd to A5
        game.make_move("a6", "a5")     # bSd capture A5
        a5_sd = game.get_board().get_square_contents("a5")
        self.assertEqual("b", a5_sd.get_color())


class TestGeneral(unittest.TestCase):
    def test_blue_general_moves(self):
        game = Game()
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
        game = Game()
        # diagonal fortress move
        game.set_turn("r")
        self.assertTrue(game.make_move("e2", "d3"))

    def test_general_pass_valid(self):
        game = Game()
        self.assertTrue(game.make_move("e9", "e9"))

    def test_general_cannot_place_itself_in_check(self):
        game = Game()
        game.make_move("e9", "e9")
        game.make_move("e4", "e5")
        game.make_move("e9", "e9")
        game.make_move("e5", "e6")
        game.make_move("e9", "e9")
        game.make_move("e6", "e7")
        self.assertFalse(game.make_move("e9", "e8"))


class TestGuard(unittest.TestCase):
    def test_guard_moves(self):
        game = Game()
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
        game = Game()
        # blue guard captures enemy soldier
        red_sold = Soldier(game.get_board(), "r")                  # make new red soldier
        game.get_board().set_square_contents("d9", red_sold)       # move it to d9 (causing check!)
        red_sold.set_position("d9")
        self.assertTrue(game.make_move("d10", "d9"))   # move guard to capture red soldier and remove check


class TestChariot(unittest.TestCase):
    def test_chariot_orthogonal_moves(self):
        game = Game()
        b_char = Chariot(game.get_board(), "b")                    # make new blue chariot
        game.get_board().set_square_contents("e6", b_char)         # move it to e6
        b_char.set_position("e6")
        valid_moves = [(5, 0), (5, 1), (5, 2), (5, 3), (5, 5), (5, 6), (5, 7), (5, 8), (4, 4), (3, 4), (5, 4)]
        self.assertCountEqual(valid_moves, b_char.get_valid_moves())

    def test_chariot_diagonal_to_center(self):
        game = Game()
        b_char = Chariot(game.get_board(), "b")                # make new blue chariot
        game.get_board().set_square_contents("d3", b_char)     # move it to d3 (fortress corner)
        b_char.set_position("d3")

        red_gen = game.get_board().get_square_contents("e2")   # get rGn
        game.get_board().set_square_contents("e2", None)       # clear rGn at e2
        game.get_board().set_square_contents("f2", red_gen)    # move to f2
        red_gen.set_position("f2")

        self.assertTrue(game.make_move("d3", "e2"))

    def test_chariot_diagonal_two_squares(self):
        game = Game()
        b_char = Chariot(game.get_board(), "b")  # make new blue chariot
        game.get_board().set_square_contents("d3", b_char)  # move it to d3 (fortress corner)
        b_char.set_position("d3")

        red_gen = game.get_board().get_square_contents("e2")  # get rGn
        game.get_board().set_square_contents("e2", None)  # clear rGn at e2
        game.get_board().set_square_contents("f2", red_gen)  # move to f2
        red_gen.set_position("f2")

        self.assertTrue(game.make_move("d3", "f1"))


class TestHorse(unittest.TestCase):
    def test_horse_capture_move(self):
        game = Game()
        # blue horse at d4
        b_horse = Horse(game.get_board(), "b")
        game.get_board().set_square_contents("d4", b_horse)
        b_horse.set_position("d4")
        self.assertIn((1, 4), b_horse.get_valid_moves())

    def test_horse_orthogonal_in_bounds_diagonal_out_of_bounds(self):
        game = Game()
        b_horse = Horse(game.get_board(), "b")
        game.get_board().set_square_contents("c9", b_horse)    # create blue horse at c9
        b_horse.set_position("c9")                      # set position
        game.get_board().set_square_contents("c10", None)      # clear horse at c10
        valid_moves = [(6, 1), (6, 3), (9, 4), (7, 4), (7, 0), (8, 2)]
        self.assertCountEqual(valid_moves, b_horse.get_valid_moves())


class TestElephant(unittest.TestCase):
    def test_elephant_moves(self):
        game = Game()
        b_ele = Elephant(game.get_board(), "b")
        game.get_board().set_square_contents("d5", b_ele)
        b_ele.set_position("d5")
        valid_moves = [(1, 5), (1, 1), (2, 0), (2, 6), (4, 3)]
        self.assertCountEqual(valid_moves, b_ele.get_valid_moves())


class TestCannon(unittest.TestCase):
    def test_cannon_jump_over_friendly_color(self):
        game = Game()
        # make arbitrary moves
        game.make_move("a7", "b7")
        game.make_move("c1", "d3")
        game.make_move("b7", "a7")
        self.assertTrue(game.make_move("b3", "e3"))    # make sure cannon can jump over same color
        game.get_board().display_board()


if __name__ == '__main__':
    unittest.main()

