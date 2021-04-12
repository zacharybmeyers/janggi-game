#!/usr/bin/env python3

# Author:       Zachary Meyers
# Date:         2021-03-10
# Description:  Portfolio Project for playing a game of Janggi (Korean Chess).
#                   The JanggiGame class sets up a board for play (list of lists) with all
#               appropriate Pieces, and has methods for making moves, determining check, etc.
#               and numerous helper methods for converting coordinates, displaying and
#               changing the game board, etc.
#                   The Piece class is the parent class for all specific pieces on the board.
#               each piece has a color and a position, and each piece uses composition with the
#               JanggiGame class to make use of its methods.
#                   Each specific child of the Piece class (ie Soldier(), General(), Cannon(), etc.)
#               inherits from the Piece class, and additionally has a name
#               (combination of color and abbreviation, ie bGn for a blue General) and a method
#               get_valid_moves() -- this is very important. There may be helper methods within each
#               child of the Piece class that help determine the valid move set of that specific Piece.
#                   The JanggiGame class has an important method, make_move(), which allows for play of
#               the game and validation of moves based on the player's turn, if a move causes check, if
#               a player is in checkmate, etc. It uses the get_valid_moves() method from the Piece to be
#               moved as part of its validation, so it is important that each child of the Piece class
#               has a get_valid_moves() method that is specific to that Piece's move set.

import logging
import random

from janggi.piece import *


class JanggiGame:
    """Represents a game of Janggi"""
    def __init__(self):
        """
        Initializes private data members for:
            game state, current turn, fortress coordinates, game board
        Sets up the positions for every Piece.
        """
        self._game_state = "UNFINISHED"
        self._turn = "b"        # blue starts the game
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
            alg_coord = self.numeric_to_algebraic(num_coord)    # convert to algebraic
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

    def get_game_state(self):
        """getter for game state"""
        return self._game_state

    def set_game_state(self, game_state):
        """setter for game state, where game_state is a string"""
        self._game_state = game_state

    def get_turn_long(self):
        return { 'b': 'blue', 'r': 'red' }[self._turn]

    def get_turn(self):
        """getter for turn"""
        return self._turn

    def set_turn(self, color):
        """setter for turn"""
        self._turn = color

    def get_next_turn(self):
        """getter returns the next player's turn"""
        if self._turn == "b":
            return "r"
        else:
            return "b"

    def update_turn(self):
        """helper function updates the turn from 'r' to 'b' and vice versa"""
        if self.get_turn() == "b":
            self.set_turn("r")
        elif self.get_turn() == "r":
            self.set_turn("b")

    # HELPER METHODS
    def algebraic_to_numeric(self, alg_coord):
        """
        helper function converts an algebraic coordinate to a numeric coordinate
        :param alg_coord: in string format ie 'b1'
        :return: the tuple with integer (x, y) coordinates
        """
        columns = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
        columns_dict = dict()
        # make dictionary where key = "letter" val = number (index)
        for index, letter in enumerate(columns):
            columns_dict[letter] = index
        column = alg_coord[0]
        row = alg_coord[1:]
        row_index = int(row) - 1
        col_index = columns_dict[column]
        return row_index, col_index

    def numeric_to_algebraic(self, num_coord):
        """
        helper function converts a numeric coordinate to an algebraic coordinate
        :param num_coord: in tuple format ie (1, 2)
        :return: the string with algebraic ie 'b1' coordinates
        """
        columns = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
        columns_dict = dict()
        # make dictionary where key = number (index) val = "letter"
        for index, letter in enumerate(columns):
            columns_dict[index] = letter
        alg_str = ""
        row_index = num_coord[0]
        col_index = num_coord[1]
        row_index += 1
        alg_str += columns_dict[col_index]
        alg_str += str(row_index)
        return alg_str

    def invert_coordinates(self, tup_list):
        """
        helper function inverts a list of coordinates (tuples) across the Janggi board.
        Returns: None
        """
        inverted_list = list()
        for coord in tup_list:
            row = coord[0]
            col = coord[1]
            inverted_coord = (9 - row, col)
            inverted_list.append(inverted_coord)  # add inverted coord
        tup_list.clear()
        tup_list.extend(inverted_list)

    def list_format(self, a_list):
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

    def display_board(self):
        """
        Displays the game board with letters A-I as a header
        and rows 1-10 as column labels.
        Uses the list_format helper function to pretty print.
        """
        header = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
        print("   ", self.list_format(header))                          # print header
        for num, row in enumerate(self.get_board()):               # print each row of the board
            if num+1 != 10:
                print(num+1, " ", self.list_format(row), " ", num+1)    # add extra space for single digit rows
            else:
                print(num+1, "", self.list_format(row), "", num+1)      # print row 10 as normal
        print("   ", self.list_format(header))                          # print footer (header)

    def get_square_contents(self, alg_coord):
        """
        Returns whatever is found at the given square's position in the game board
        (either a Piece or None)
        :param alg_coord: in string format ie 'b1'
        :return: the object in the square (or None)
        """
        row_index, col_index = self.algebraic_to_numeric(alg_coord)
        board = self.get_board()
        return board[row_index][col_index]

    def set_square_contents(self, alg_coord, piece_obj):
        """
        For debugging/testing, overrides a square on the board with a given Piece
        """
        row_index, col_index = self.algebraic_to_numeric(alg_coord)
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
        if color == "b":
            enemy_color = "r"
        else:
            enemy_color = "b"

        # get all the enemy's valid moves
        enemy_valid_moves = []
        for move_list in self.all_player_moves(enemy_color).values():
            enemy_valid_moves.extend(move_list)

        # get the friendly general
        general_obj = self.get_general(color)
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

        # run is_in_check on the current player,
        # if in check, set valid_move to FALSE
        # else set valid_move to TRUE
        if self.is_in_check(piece_obj.get_color()):
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

    def make_ai_move(self, level):
        assert(self.get_game_state() == "UNFINISHED")

        moves = self.all_player_moves(self.get_turn())
        invalid_moves = set()

        while True:
            start_num = None
            end_num = None

            # Find move that causes check
            #if level >= 20:
            #    for s,ends in moves.items():
            #        for e in ends:
            #            p = self.get_square_contents(e)
            #            if p is not None:
            #                pass
                
            # Find move with highest capture value
            if start_num is None and level >= 10:
                max_capture = 0
                for s,ends in moves.items():
                    for e in ends:
                        if (s,e) in invalid_moves:
                            continue  # skip previously tried invalid moves
                        if s == e:
                            continue  # skip pass moves
                        p = self.get_square_contents(self.numeric_to_algebraic(e))
                        if p is not None:
                            if p.get_worth() > max_capture:
                                (start_num, end_num) = (s, e)
                                max_capture = p.get_worth()
                if start_num is not None:
                    logging.debug('AI found max-capture={} with {} -> {}'.format(
                            max_capture, self.numeric_to_algebraic(start_num),
                            self.numeric_to_algebraic(end_num)))
                else:
                    logging.debug('AI failed to find max-capture')
                 
            # Find random move
            if start_num is None:
                assert (end_num is None)
                start_num = random.choice(list(moves.keys()))
                end_num = random.choice(moves[start_num])
                logging.debug('AI trying random move {} -> {}'.format(
                        self.numeric_to_algebraic(start_num),
                        self.numeric_to_algebraic(end_num)))

            if level > 0:
                # disallow pass moves for anything other than "easy" AI
                if len(moves[start_num]) > 1:
                    while start_num == end_num:
                        end_num = random.choice(moves[start_num])
                    logging.debug('AI avoiding pass move, new move {} -> {}'.format(
                            self.numeric_to_algebraic(start_num),
                            self.numeric_to_algebraic(end_num)))

            start = self.numeric_to_algebraic(start_num)
            end = self.numeric_to_algebraic(end_num)
            if self.make_move(start, end):
                break
            else:
                invalid_moves.add((start_num, end_num))

        return (start, end)

    def make_move(self, start, end):
        """
        Checks the validity of a move, uses get_valid_moves() from the Piece class instance
        found at the start square.
            Note:       each piece has a valid pass move in its set of valid moves.
                        it is treated like any other move, but won't remove the piece.
            Invalid if: start square is empty (None), not the starting square's turn,
                        game is finished, end square is not in the valid moves of the
                        Piece instance from the start square, the hypothetical move
                        causes the general to be in (or remain in) check.
                        Return False if any of the invalid conditions are True.
            If valid:   move Piece object from start square to end square
                        (removes opposing piece or fills empty square),
                        update moved Piece object's position, clear start square
            Win check:  Look for checkmate on opposite player's General, if True
                        update game_state accordingly to reflect current player won.
            End:        update turn for next player, return True
        :param start: algebraic coordinate for the start square
        :param end: algebraic coordinate for the end square
        :return: True if valid move, False otherwise
        """
        # for debugging
        logging.debug(f"Attempting: {start} -> {end}")

        # INVALID CONDITIONS
        # get the Piece from the start square
        piece_obj = self.get_square_contents(start)
        if piece_obj is None:
            return False                                # invalid move if there's no piece
        if self.get_turn() != piece_obj.get_color():    # invalid move if not starting square's turn
            return False
        if self.get_game_state() != "UNFINISHED":       # invalid move if game is finished
            return False
        end_tup = self.algebraic_to_numeric(end)
        if end_tup not in piece_obj.get_valid_moves():  # invalid if end position is not valid for this piece
            return False

        # initialize colors for the current and next player
        current_color = self.get_turn()
        next_color = self.get_next_turn()

        # At this point, the current player's move is in their valid move set, but...
        #   If this move ends with the current player's general in check, invalid move
        if self.hypothetical_move(start, end) is False:
            return False

        #  If the valid move is a pass move (and it hasn't put or left the player in check),
        #  simply update turn and return True
        if start == end:
            logging.info(f'{current_color} moved: pass')
            self.update_turn()
            return True

        # otherwise, VALID MOVE
        start_tup = self.algebraic_to_numeric(start)
        start_row, start_col = start_tup
        end_row, end_col = end_tup              # unpack end square tup
        board = self.get_board()                # get board

        # move Piece object to new square
        # (removes opposing piece or fills empty square)
        board[end_row][end_col] = piece_obj
        piece_obj.set_position(end)             # store new position (algebraic coordinate)
        board[start_row][start_col] = None      # clear start square

        # if the next player is in check...
        # try to determine checkmate: make use of hypothetical_move() helper
        checkmate = None
        if self.is_in_check(next_color):
            # initialize checkmate to True
            checkmate = True
            enemy_general = self.get_general(next_color)
            enemy_general_pos = enemy_general.get_position()
            for move in enemy_general.get_valid_moves():
                # try a hypothetical move
                potential_move_pos = self.numeric_to_algebraic(move)
                if self.hypothetical_move(enemy_general_pos, potential_move_pos):
                    checkmate = False       # if a general can hypothetically move, not in checkmate

        if checkmate:
            if self.get_turn() == "b":
                self.set_game_state("BLUE_WON")
            elif self.get_turn() == "r":
                self.set_game_state("RED_WON")

        # update turn
        logging.info(f'{current_color} moved: {start} -> {end}')
        self.update_turn()
        return True




# test move sequences below
def main():
    game = JanggiGame()
    for piece in game.all_pieces():
        print(piece.get_name())

if __name__ == "__main__":
    main()

