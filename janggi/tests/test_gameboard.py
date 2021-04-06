#!/usr/bin/env python3

# Author:       Zachary Meyers
# Date:         2021-03-01
# Description:  Unit tests for JanggiGame, namely all the potential moves and methods.

import unittest

from janggi.gameboard import JanggiGame
from janggi.piece     import Soldier


class TestGameboard(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()

