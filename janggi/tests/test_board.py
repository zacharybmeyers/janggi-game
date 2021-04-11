#!/usr/bin/env python3

# Author:       Zachary Meyers
# Date:         2021-03-01
# Description:  Unit tests for Game, namely all the potential moves and methods.

import unittest

from janggi.board import Board
from janggi.piece import Soldier


class TestBoard(unittest.TestCase):
    def test_get_square_contents(self):
        board = Board()
        self.assertEqual(board.get_board()[0][0], board.get_square_contents("a1"))

    def test_set_square_contents(self):
        board = Board()
        # assign a new red soldier to an empty square
        new_sold = Soldier(board, "r")
        board.set_square_contents("d9", new_sold)
        self.assertEqual(new_sold, board.get_square_contents("d9"))


if __name__ == '__main__':
    unittest.main()

