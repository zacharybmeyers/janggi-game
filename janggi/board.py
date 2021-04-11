#!/usr/bin/env python3

# Author:       Zachary Meyers
# Date:         2021-03-10
# Description:  Portfolio Project for playing a game of Janggi (Korean Chess).
#                   The Game class sets up a board for play (list of lists) with all
#               appropriate Pieces, and has methods for making moves, determining check, etc.
#               and numerous helper methods for converting coordinates, displaying and
#               changing the game board, etc.
#                   The Piece class is the parent class for all specific pieces on the board.
#               each piece has a color and a position, and each piece uses composition with the
#               Game class to make use of its methods.
#                   Each specific child of the Piece class (ie Soldier(), General(), Cannon(), etc.)
#               inherits from the Piece class, and additionally has a name
#               (combination of color and abbreviation, ie bGn for a blue General) and a method
#               get_valid_moves() -- this is very important. There may be helper methods within each
#               child of the Piece class that help determine the valid move set of that specific Piece.
#                   The Game class has an important method, make_move(), which allows for play of
#               the game and validation of moves based on the player's turn, if a move causes check, if
#               a player is in checkmate, etc. It uses the get_valid_moves() method from the Piece to be
#               moved as part of its validation, so it is important that each child of the Piece class
#               has a get_valid_moves() method that is specific to that Piece's move set.

from janggi.piece import *
from janggi.utils import algebraic_to_numeric, numeric_to_algebraic


class Board:
    """Represents the board in a game of Janggi"""
    def __init__(self):
        """
        Initializes private data members for:
            fortress coordinates, game board
        Sets up the positions for every Piece.
        """
        # initialize blue fortress coordinates for use in each Piece subclass,
        # can be converted to red fortress coordinates with use of helper method invert_coordinates()
        self._b_fortress = [(7, 3), (8, 3), (9, 3), (7, 4), (8, 4), (9, 4), (7, 5), (8, 5), (9, 5)]
        self._b_fort_corners = [(7, 3), (7, 5), (9, 3), (9, 5)]
        self._b_fort_center = [(8, 4)]
        self._board = [
            [Chariot(self, "r"), Elephant(self, "r"), Horse(self, "r"), Guard(self, "r"), None,
             Guard(self, "r"), Elephant(self, "r"), Horse(self, "r"), Chariot(self, "r")],
            [None, None, None, None, General(self, "r"), None, None, None, None],
            [None, Cannon(self, "r"), None, None, None, None, None, Cannon(self, "r"), None],
            [Soldier(self, "r"), None, Soldier(self, "r"), None, Soldier(self, "r"), None,
             Soldier(self, "r"), None, Soldier(self, "r")],
            [None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None],
            [Soldier(self, "b"), None, Soldier(self, "b"), None, Soldier(self, "b"), None,
             Soldier(self, "b"), None, Soldier(self, "b")],
            [None, Cannon(self, "b"), None, None, None, None, None, Cannon(self, "b"), None],
            [None, None, None, None, General(self, "b"), None, None, None, None],
            [Chariot(self, "b"), Elephant(self, "b"), Horse(self, "b"), Guard(self, "b"), None,
             Guard(self, "b"), Elephant(self, "b"), Horse(self, "b"), Chariot(self, "b")],
        ]
        # set starting positions for game pieces
        self.setup_piece_positions()

    def get_board(self):
        """getter for board"""
        return self._board

    def indexed_piece_objects(self):
        """
        generator yields all the piece objects from the game board along
        with associated row/column indexes
        """
        for ridx,row in enumerate(self.get_board()):
            for cidx,piece_obj in enumerate(row):
                if piece_obj is not None:
                    yield (ridx,cidx,piece_obj)

    def all_pieces(self):
        for (ridx,cidx,piece) in self.indexed_piece_objects():
            yield piece

    def pieces_by_color(self, color):
        """
        generator extends all_pieces to yield all piece objects from the
        game board of a specified color ('b' or 'r')
        """
        for piece_obj in self.all_pieces():
            if piece_obj.get_color() == color:
                yield piece_obj

    def setup_piece_positions(self):
        """helper function gives an algebraic position to every Piece on the board"""
        # set starting positions for game pieces
        for (row_index,col_index,piece_obj) in self.indexed_piece_objects():
            num_coord = (row_index, col_index)                  # create coordinate
            alg_coord = numeric_to_algebraic(num_coord)    # convert to algebraic
            piece_obj.set_position(alg_coord)                   # set the position

    def get_blue_fortress(self):
        """getter for blue fortress coordinates"""
        return self._b_fortress

    def get_blue_fortress_corners(self):
        """getter for blue fortress corners"""
        return self._b_fort_corners

    def get_blue_fortress_center(self):
        """getter for blue fortress center"""
        return self._b_fort_center


    def display_board(self):
        """
        Displays the game board with letters A-I as a header
        and rows 1-10 as column labels.
        Uses the list_format helper function to pretty print.
        """
        header = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
        print("   ", list_format(header))                          # print header
        for num, row in enumerate(self.get_board()):               # print each row of the board
            if num+1 != 10:
                print(num+1, " ", list_format(row), " ", num+1)    # add extra space for single digit rows
            else:
                print(num+1, "", list_format(row), "", num+1)      # print row 10 as normal
        print("   ", list_format(header))                          # print footer (header)

    def get_square_contents(self, alg_coord):
        """
        Returns whatever is found at the given square's position in the game board
        (either a Piece or None)
        :param alg_coord: in string format ie 'b1'
        :return: the object in the square (or None)
        """
        row_index, col_index = algebraic_to_numeric(alg_coord)
        board = self.get_board()
        return board[row_index][col_index]

    def set_square_contents(self, alg_coord, piece_obj):
        """
        For debugging/testing, overrides a square on the board with a given Piece
        """
        row_index, col_index = algebraic_to_numeric(alg_coord)
        board = self.get_board()
        board[row_index][col_index] = piece_obj

    def get_general(self, color):
        """
        helper function returns the General object found on the board
        with a specified color
        """
        general_name = color + "Gn"
        # iterate through all pieces on the game board
        for piece_obj in self.all_pieces():
            if general_name in piece_obj.get_name():
                return piece_obj

    def all_player_moves(self, color):
        """
        helper function returns a large dictionary of all the possible moves a player (color)
        can make with their current set of pieces on the game board
        key = piece's position
        val = list of valid moves
        """
        all_valid_moves = dict()
        # iterate through the player's pieces
        for piece_obj in self.pieces_by_color(color):
            all_valid_moves[piece_obj.get_numeric_position()] = piece_obj.get_valid_moves()
        return all_valid_moves

    def is_in_check(self, color):
        """
        Takes a color for the player in question.
        Use all_player_moves to create a large list of all of the enemy's possible next moves.
        If the friendly General's position is in this list of enemy_valid_moves (able to be captured),
        they are in check, return True.
        Otherwise, return False.
        """
        # initialize colors
        if color == "blue":
            friendly_color = "b"
            enemy_color = "r"
        else:
            friendly_color = "r"
            enemy_color = "b"

        # get all the enemy's valid moves
        enemy_valid_moves = []
        for move_list in self.all_player_moves(enemy_color).values():
            enemy_valid_moves.extend(move_list)

        # get the friendly general
        general_obj = self.get_general(friendly_color)
        # get the general's position
        general_pos = general_obj.get_numeric_position()

        # if the general's position can be captured by the opposite player
        # on the next turn, they are in check
        if general_pos in enemy_valid_moves:
            logging.debug(f'{color} in check!')
            return True
        else:
            return False

    def hypothetical_move(self, start, end):
        """
            Helper function checks the validity of a potential move
        (invalid if it puts or leaves the player in check). It is used for testing
        checkmate on all of a General's valid moves at the end of make_move.
            Takes a Piece's current position and a hypothetical end position,
        (assumes start and end position have already been validated in make_move).
        temporarily sets the game board to this scenario.
            If the move would cause the player to be in check, returns False,
        otherwise return True.
        """
        # get Piece from start position
        piece_obj = self.get_square_contents(start)
        # get object from end position (either a Piece or None)
        end_obj = self.get_square_contents(end)
        # clear start position
        self.set_square_contents(start, None)
        # set General to end position
        self.set_square_contents(end, piece_obj)
        piece_obj.set_position(end)

        # get color from starting piece
        check_color = None
        if piece_obj.get_color() == "r":
            check_color = "red"
        elif piece_obj.get_color() == "b":
            check_color = "blue"

        # run is_in_check on the current player,
        # if in check, set valid_move to FALSE
        # else set valid_move to TRUE
        if self.is_in_check(check_color):
            valid_move = False
        else:
            valid_move = True

        # set end position back to end_obj
        self.set_square_contents(end, end_obj)
        if end_obj is not None:
            end_obj.set_position(end)
        # set Piece back to start position
        self.set_square_contents(start, piece_obj)
        piece_obj.set_position(start)

        # return whether or not this hypothetical move caused the player to be in check
        return valid_move


# HELPER FUNCTIONS


def list_format(a_list):
    """
    helper function takes a list and returns a printable string
    with the proper column width (9) for each list element
    """
    print_str = ""
    for elem in a_list:
        if type(elem) in Piece.__subclasses__():  # if child of Piece class, use 3 letter name
            elem_str = elem.get_name()
            spaces = "   "  # 3 spaces for either side
        elif elem is None:  # if empty, use "---"
            elem_str = "---"
            spaces = "   "
        else:  # header letter ie 'A'
            elem_str = str(elem)
            spaces = "    "  # 4 spaces for either side
        print_str += spaces
        print_str += elem_str
        print_str += spaces
    return print_str


# test move sequences below
def main():
    board = Board()
    for piece in board.all_pieces():
        print(piece.get_name())


if __name__ == "__main__":
    main()
