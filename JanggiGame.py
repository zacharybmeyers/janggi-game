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

import pygame
import os
import logging
import random


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

    def setup_piece_positions(self):
        """helper function gives an algebraic position to every Piece on the board"""
        # set starting positions for game pieces
        row_index = 0
        for row in self.get_board():
            col_index = 0
            for piece_obj in row:
                if piece_obj is not None:                               # if element is a Piece
                    num_coord = (row_index, col_index)                  # create coordinate
                    alg_coord = self.numeric_to_algebraic(num_coord)    # convert to algebraic
                    piece_obj.set_position(alg_coord)                   # set the position
                col_index += 1
            row_index += 1

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
        board = self.get_board()
        # iterate through all pieces on the game board
        for row in board:
            for piece_obj in row:
                # if not empty...
                if piece_obj is not None:
                    # if general, return general
                    if general_name in piece_obj.get_name():
                        return piece_obj

    def all_player_moves(self, color):
        """
        helper function returns a large list of all the possible moves a player (color)
        can make with their current set of pieces on the game board
        """
        all_valid_moves = dict()
        board = self.get_board()
        # iterate through all pieces on the game board
        for row in board:
            for piece_obj in row:
                # if not empty...
                if piece_obj is not None:
                    # if color
                    if color in piece_obj.get_name():
                        # get the valid moves and add them to the enemy list
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

        # initialize colors for the current and next player,
        # convert single letters to full words to use with is_in_check() method
        current_color = self.get_turn()
        if current_color == "b":
            current_color_for_check = "blue"
            next_color = "r"
            next_color_for_check = "red"
        else:
            current_color_for_check = "red"
            next_color = "b"
            next_color_for_check = "blue"

        # If the move places the current player in check, invalid move
        if self.hypothetical_move(start, end) is False:
            return False

        # At this point, the current player's move is in their valid move set, but...
        #   if the current player is in check...
        #       and if their hypothetical move is False (puts or leaves their general in check),
        #           invalid move
        if self.is_in_check(current_color_for_check):
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
        if self.is_in_check(next_color_for_check):
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


class Piece:
    """Represents a Piece for use in the JanggiGame class"""
    def __init__(self, game_class, color, worth):
        """initializes game, color, and position"""
        self._game = game_class
        self._color = color
        self._worth = worth
        self._position = None

    def get_color(self):
        """getter for color"""
        return self._color

    def get_worth(self):
        """getter for worth"""
        return self._worth

    def get_position(self):
        """getter for position"""
        return self._position

    def get_numeric_position(self):
        """
        helper function converts the algebraic position to a
        numeric position (tuple) and returns it
        """
        algebraic_pos = self.get_position()
        numeric_pos = self._game.algebraic_to_numeric(algebraic_pos)
        return numeric_pos

    def set_position(self, alg_coord):
        """setter for position, takes an algebraic coordinate ie 'b1'"""
        self._position = alg_coord

    def remove_out_of_bounds(self, moves_list):
        """
        helper function takes a list of tuples of potential moves for
        any child of the Piece instance.
        Returns: a list without any moves that are off the game board
        """
        board = self._game.get_board()
        num_rows = len(board)
        num_cols = len(board[0])
        valid_moves = []
        for coord in moves_list:
            row, col = coord  # unpack tuple
            if 0 <= row < num_rows and 0 <= col < num_cols:  # if column is in [A...I] and row is in [0...9]
                valid_moves.append(coord)                    # add to valid moves
        return valid_moves

    def remove_same_color(self, tup_list):
        """
        helper function takes a list of tuples of potential moves for
        any child of the Piece instance.
        Returns: a list without any moves that are occupied by a piece
        of the same color as the current Piece instance (blocked)
        """
        valid_moves = []
        board = self._game.get_board()
        for coord in tup_list:
            row_index, col_index = coord
            piece_obj = board[row_index][col_index]
            if piece_obj is None:
                valid_moves.append(coord)           # valid if empty
            elif piece_obj.get_color() != self.get_color():
                valid_moves.append(coord)           # valid if opposite player color
        return valid_moves

    def on_game_board(self, tup_coord):
        """
        helper function takes a tuple coordinate and
        returns true if it's on the game board, false otherwise
        """
        board = self._game.get_board()
        row_len = len(board[0])
        col_len = len(board)

        row, col = tup_coord
        if 0 <= col < row_len and 0 <= row < col_len:
            return True
        else:
            return False


class Chariot(Piece):
    """
    Inherits from the Piece superclass.
    Move type: as many squares as desired along straight lines of board,
                or diagonal lines if in the fortress
    Uses super() to initialize the color and receive the JanggiGame class.
    Creates an 'image' data member: uses 'name' to access the correct .svg from /assets,
    creates a pygame image for use with JanggiGUI.py
    """
    def __init__(self, game_class, color):
        super().__init__(game_class, color, 13)
        self._name = color + "Ch"
        filename = self._name + ".svg"
        self._image = pygame.image.load(os.path.join("assets", filename))

    def get_image(self):
        """getter for image"""
        return self._image

    def get_name(self):
        """getter for name"""
        return self._name

    def orthogonal_moves(self, direction):
        """
        helper function returns a list of possible orthogonal moves
        based on the direction given.
        uses helper function on_game_board()
        :param direction: either 'right', 'left', 'down', or 'up'
        :returns: orthogonal_moves
        """
        chariot_pos = self.get_numeric_position()
        row_index, col_index = chariot_pos

        step = None
        next_row = None
        next_column = None
        if direction == "right" or direction == "left":     # if horizontal direction
            if direction == "right":
                step = 1
            if direction == "left":
                step = -1
            next_column = col_index + step                      # move column index either right or left
            next_row = row_index                                # row index unchanged
        if direction == "down" or direction == "up":        # if vertical direction
            if direction == "down":
                step = 1
            if direction == "up":
                step = -1
            next_column = col_index                             # column index unchanged
            next_row = row_index + step                         # move row index either down or up

        orthogonal_moves = list()
        board = self._game.get_board()
        valid_square = True
        while valid_square:
            if self.on_game_board((next_row, next_column)):  # if next piece is on the board
                # get next piece
                next_piece = board[next_row][next_column]
                if next_piece is None:                                      # if empty, valid move
                    orthogonal_moves.append((next_row, next_column))
                    if direction == "right" or direction == "left":         # move across board based on direction
                        next_column += step
                    elif direction == "down" or direction == "up":
                        next_row += step
                elif next_piece.get_color() != self.get_color():            # if enemy, valid move, stop loop
                    orthogonal_moves.append((next_row, next_column))
                    valid_square = False
                else:                                                       # if friendly, invalid move, stop loop
                    valid_square = False
            else:                                                   # if not on the board, stop loop
                valid_square = False
        return orthogonal_moves

    def fortress_moves(self):
        """helper function returns a list of possible moves a Chariot can make in a fortress"""
        chariot_pos = self.get_numeric_position()
        row_index, col_index = chariot_pos

        # initialize to blue fortress
        blue_fortress = self._game.get_blue_fortress()
        fortress = blue_fortress
        fort_corners = self._game.get_blue_fortress_corners()
        fort_center = self._game.get_blue_fortress_center()

        # if the chariot is not in the blue fortress, invert to red fortress coordinates
        if chariot_pos not in blue_fortress:
            self._game.invert_coordinates(fortress)
            self._game.invert_coordinates(fort_corners)
            self._game.invert_coordinates(fort_center)

        potential_moves = list()
        # if chariot is in the center or a corner, can move one square diagonally
        if chariot_pos in fort_center or chariot_pos in fort_corners:
            potential_moves.append((row_index + 1, col_index + 1))  # diagonal 1 down/right
            potential_moves.append((row_index + 1, col_index - 1))  # diagonal 1 down/left
            potential_moves.append((row_index - 1, col_index + 1))  # diagonal 1 up/right
            potential_moves.append((row_index - 1, col_index - 1))  # diagonal 1 up/left

        # if chariot is in a fortress corner, and if the center is empty, can move two squares diagonally
        alg_center = self._game.numeric_to_algebraic(fort_center[0])
        center_obj = self._game.get_square_contents(alg_center)
        if chariot_pos in fort_corners and center_obj is None:
            potential_moves.append((row_index + 2, col_index + 2))  # diagonal 2 down/right
            potential_moves.append((row_index + 2, col_index - 2))  # diagonal 2 down/left
            potential_moves.append((row_index - 2, col_index + 2))  # diagonal 2 up/right
            potential_moves.append((row_index - 2, col_index - 2))  # diagonal 2 up/left

        # at this point a lot of extra moves are in potential moves that aren't confined to the fortress
        fortress_moves = list()
        for coord in potential_moves:
            if coord in fortress:
                fortress_moves.append(coord)    # only add moves that are in the fortress

        return self.remove_same_color(fortress_moves)   # remove any squares that are friendly

    def get_valid_moves(self):
        """
        returns a list of valid moves for the Chariot based on the current position
        """
        # can move horizontally or vertically unless off board or blocked
        chariot_moves = list()

        # get orthogonal moves
        right_moves = self.orthogonal_moves("right")
        left_moves = self.orthogonal_moves("left")
        down_moves = self.orthogonal_moves("down")
        up_moves = self.orthogonal_moves("up")

        # add to running list
        chariot_moves.extend(right_moves)
        chariot_moves.extend(left_moves)
        chariot_moves.extend(down_moves)
        chariot_moves.extend(up_moves)

        # use helper to get fortress moves, add to running list
        chariot_moves.extend(self.fortress_moves())

        # add current position (pass move) to valid moves
        chariot_pos = self.get_numeric_position()
        chariot_moves.append(chariot_pos)

        return chariot_moves


class Elephant(Piece):
    """
    Inherits from the Piece superclass.
    Move type: forward, backward, left, or right one square, then diagonal
                outward 2 squares. Can be blocked at any point along this path.
    Uses super() to initialize the color and receive the JanggiGame class.
    Creates an 'image' data member: uses 'name' to access the correct .svg from /assets,
    creates a pygame image for use with JanggiGUI.py
    """
    def __init__(self, game_class, color):
        super().__init__(game_class, color, 3)
        self._name = color + "El"
        filename = self._name + ".svg"
        self._image = pygame.image.load(os.path.join("assets", filename))

    def get_image(self):
        """getter for image"""
        return self._image

    def get_name(self):
        """getter for name"""
        return self._name

    def elephant_diagonal_moves(self, direction):
        """
        helper function returns a list of possible diagonal moves 2 squares away
        from the current position based on the direction given.
        verifies the moves aren't blocked, and that they are on the game board with
        the use of on_game_board() and remove_out_of_bounds() helper functions.
        :param direction: either 'right', 'left', 'down', or 'up'
        :returns: diagonal_moves
        """
        elephant_pos = self.get_numeric_position()
        row_index, col_index = elephant_pos

        step = None
        next_row = None
        next_column = None
        if direction == "right" or direction == "left":  # if horizontal direction
            if direction == "right":
                step = 1
            if direction == "left":
                step = -1
            next_column = col_index + step  # move column index either right or left
            next_row = row_index  # row index unchanged
        if direction == "down" or direction == "up":  # if vertical direction
            if direction == "down":
                step = 1
            if direction == "up":
                step = -1
            next_column = col_index  # column index unchanged
            next_row = row_index + step  # move row index either down or up

        diagonal_moves = list()
        if self.on_game_board((next_row, next_column)):  # if in bounds
            ortho_square = (next_row, next_column)
            ortho_square_alg = self._game.numeric_to_algebraic(ortho_square)
            ortho_obj = self._game.get_square_contents(ortho_square_alg)
            if ortho_obj is None:  # if orthogonal square is not blocked
                # make two lists for possible diagonals 1 square away and
                # 2 squares away (depending on direction)
                first_diagonals = None
                second_diagonals = None
                if direction == "up" or direction == "down":
                    first_diagonals = [(next_row+step, next_column+1), (next_row+step, next_column-1)]
                    second_diagonals = [(next_row+step+step, next_column+2), (next_row+step+step, next_column-2)]
                if direction == "right" or direction == "left":
                    first_diagonals = [(next_row+1, next_column+step), (next_row-1, next_column+step)]
                    second_diagonals = [(next_row+2, next_column+step+step), (next_row-2, next_column+step+step)]
                # iterate only through the first diagonals that are on the game board
                for first_diag in self.remove_out_of_bounds(first_diagonals):
                    first_diag_alg = self._game.numeric_to_algebraic(first_diag)
                    first_diag_obj = self._game.get_square_contents(first_diag_alg)
                    if first_diag_obj is None:  # if empty (clear)
                        # iterate through second diagonals that are on the board
                        for second_diag in self.remove_out_of_bounds(second_diagonals):
                            second_diag_alg = self._game.numeric_to_algebraic(second_diag)
                            second_diag_obj = self._game.get_square_contents(second_diag_alg)
                            if second_diag_obj is None or second_diag_obj.get_color() != self.get_color():
                                # if empty or enemy, add to valid moves
                                diagonal_moves.append(second_diag)
        # the nested call above will add duplicate valid moves to the list, remove these before returning
        return list(set(diagonal_moves))

    def get_valid_moves(self):
        """
        returns a list of valid moves for the Elephant based on the current position,
        uses helper function diagonal_moves() to get the valid moves that are 2 diagonal
        squares away
        """
        elephant_moves = list()
        elephant_moves.extend(self.elephant_diagonal_moves("up"))
        elephant_moves.extend(self.elephant_diagonal_moves("down"))
        elephant_moves.extend(self.elephant_diagonal_moves("right"))
        elephant_moves.extend(self.elephant_diagonal_moves("left"))

        # add elephant's current position (pass move) as a valid move
        elephant_pos = self.get_numeric_position()
        elephant_moves.append(elephant_pos)

        return elephant_moves


class Horse(Piece):
    """
    Inherits from the Piece superclass.
    Move type: forward, backward, left, or right one square, then diagonal
                outward 1 square. Can be blocked at any point along this path.
    Uses super() to initialize the color and receive the JanggiGame class.
    Creates an 'image' data member: uses 'name' to access the correct .svg from /assets,
    creates a pygame image for use with JanggiGUI.py
    """
    def __init__(self, game_class, color):
        super().__init__(game_class, color, 5)
        self._name = color + "Hs"
        filename = self._name + ".svg"
        self._image = pygame.image.load(os.path.join("assets", filename))

    def get_image(self):
        """getter for image"""
        return self._image

    def get_name(self):
        """getter for name"""
        return self._name

    def horse_diagonal_moves(self, direction):
        """
        helper function returns a list of possible diagonal moves 1 square away
        based on the direction given.
        verifies the moves aren't blocked, and that they are on the game board with
        the use of the on_game_board() and remove_out_of_bounds() helper functions.
        :param direction: either 'right', 'left', 'down', or 'up'
        :returns: diagonal_moves
        """
        horse_pos = self.get_numeric_position()
        row_index, col_index = horse_pos

        step = None
        next_row = None
        next_column = None
        if direction == "right" or direction == "left":  # if horizontal direction
            if direction == "right":
                step = 1
            if direction == "left":
                step = -1
            next_column = col_index + step  # move column index either right or left
            next_row = row_index  # row index unchanged
        if direction == "down" or direction == "up":  # if vertical direction
            if direction == "down":
                step = 1
            if direction == "up":
                step = -1
            next_column = col_index  # column index unchanged
            next_row = row_index + step  # move row index either down or up

        diagonal_moves = list()
        if self.on_game_board((next_row, next_column)):  # if in bounds
            ortho_square = (next_row, next_column)
            ortho_square_alg = self._game.numeric_to_algebraic(ortho_square)
            ortho_obj = self._game.get_square_contents(ortho_square_alg)
            if ortho_obj is None:  # if orthogonal square is not blocked
                # make list of 2 possible diagonals (depending on direction)
                diagonals = None
                if direction == "up" or direction == "down":
                    diagonals = [(next_row+step, next_column+1), (next_row+step, next_column-1)]
                if direction == "right" or direction == "left":
                    diagonals = [(next_row+1, next_column+step), (next_row-1, next_column+step)]
                # iterate only through the diagonals that are on the game board
                for diagonal in self.remove_out_of_bounds(diagonals):
                    diagonal_alg = self._game.numeric_to_algebraic(diagonal)
                    diagonal_obj = self._game.get_square_contents(diagonal_alg)
                    if diagonal_obj is None or diagonal_obj.get_color() != self.get_color():  # if empty or enemy
                        diagonal_moves.append(diagonal)  # add coordinate to valid moves
        return diagonal_moves

    def get_valid_moves(self):
        """
        returns a list of valid moves for the Horse based on the current position,
        uses helper function horse_diagonal_moves()
        """
        horse_moves = list()
        horse_moves.extend(self.horse_diagonal_moves("up"))
        horse_moves.extend(self.horse_diagonal_moves("down"))
        horse_moves.extend(self.horse_diagonal_moves("right"))
        horse_moves.extend(self.horse_diagonal_moves("left"))

        # add horse's current position (pass move) to valid moves
        horse_pos = self.get_numeric_position()
        horse_moves.append(horse_pos)

        return horse_moves


class Guard(Piece):
    """
    Inherits from the Piece superclass.
    Move type: confined to fortress, moves one square oly, or one
                diagonally if in the center or on a corner
    Uses super() to initialize the color and receive the JanggiGame class.
    Creates an 'image' data member: uses 'name' to access the correct .svg from /assets,
    creates a pygame image for use with JanggiGUI.py
    """
    def __init__(self, game_class, color):
        super().__init__(game_class, color, 3)
        self._name = color + "Gd"
        filename = self._name + ".svg"
        self._image = pygame.image.load(os.path.join("assets", filename))

    def get_image(self):
        """getter for image"""
        return self._image

    def get_name(self):
        """getter for name"""
        return self._name

    def get_valid_moves(self):
        """
        returns a list of valid moves for the Guard based on the current position,
        uses helper functions remove_same_color for moves blocked by friendly pieces
        """
        guard_pos = self.get_numeric_position()
        row_index, col_index = guard_pos

        # initialize to blue fortress
        blue_fortress = self._game.get_blue_fortress()
        fortress = blue_fortress
        fort_corners = self._game.get_blue_fortress_corners()
        fort_center = self._game.get_blue_fortress_center()

        # if the guard is not in the blue fortress, invert to red fortress coordinates
        if guard_pos not in blue_fortress:
            self._game.invert_coordinates(fortress)
            self._game.invert_coordinates(fort_corners)
            self._game.invert_coordinates(fort_center)

        guard_moves = list()
        # all positions in the fortress can move up/down or left/right (within the fortress)
        if guard_pos in fortress:
            guard_moves.append((row_index + 1, col_index))  # down
            guard_moves.append((row_index - 1, col_index))  # up
            guard_moves.append((row_index, col_index + 1))  # right
            guard_moves.append((row_index, col_index - 1))  # left
        # if the guard is in the center or corner, can also move diagonally
        if guard_pos in fort_corners or guard_pos in fort_center:
            guard_moves.append((row_index + 1, col_index + 1))  # diagonal down/right
            guard_moves.append((row_index + 1, col_index - 1))  # diagonal down/left
            guard_moves.append((row_index - 1, col_index + 1))  # diagonal up/right
            guard_moves.append((row_index - 1, col_index - 1))  # diagonal up/left

        # at this point: a lot of extra moves are in gen_moves
        # that aren't confined to the fortress, remove these
        fortress_moves = list()
        for coord in guard_moves:
            if coord in fortress:
                fortress_moves.append(coord)  # only add coordinates that are in the fortress

        all_moves = self.remove_same_color(fortress_moves)  # remove any squares that are friendly

        # add guard's current position (pass move) to valid moves
        all_moves.append(guard_pos)

        return all_moves


class General(Piece):
    """
    Inherits from the Piece superclass.
    Move type: confined to fortress, moves one square orthogonally, or one
                diagonally if in the center or on a corner
    Uses super() to initialize the color and receive the JanggiGame class.
    Creates an 'image' data member: uses 'name' to access the correct .svg from /assets,
    creates a pygame image for use with JanggiGUI.py
    """
    def __init__(self, game_class, color):
        super().__init__(game_class, color, 99)
        self._name = color + "Gn"
        filename = self._name + ".svg"
        self._image = pygame.image.load(os.path.join("assets", filename))

    def get_image(self):
        """getter for image"""
        return self._image

    def get_name(self):
        """getter for name"""
        return self._name

    def get_valid_moves(self):
        """
        returns a list of valid moves for the General based on the current position,
        uses helper functions remove_same_color for moves blocked by friendly pieces
        and invert_coordinates from the game class for red vs blue Generals
        """
        gen_pos = self.get_numeric_position()
        row_index, col_index = gen_pos

        # initialize to blue fortress
        blue_fortress = self._game.get_blue_fortress()
        fortress = blue_fortress
        fort_corners = self._game.get_blue_fortress_corners()
        fort_center = self._game.get_blue_fortress_center()

        # if the general is not in the blue fortress, invert to red fortress coordinates
        if gen_pos not in blue_fortress:
            self._game.invert_coordinates(fortress)
            self._game.invert_coordinates(fort_corners)
            self._game.invert_coordinates(fort_center)

        gen_moves = list()
        # all positions in the fortress can move up/down or left/right (within the fortress)
        if gen_pos in fortress:
            gen_moves.append((row_index+1, col_index))      # down
            gen_moves.append((row_index-1, col_index))      # up
            gen_moves.append((row_index, col_index+1))      # right
            gen_moves.append((row_index, col_index-1))      # left
        # if the general is in the center or corner, can also move diagonally
        if gen_pos in fort_corners or gen_pos in fort_center:
            gen_moves.append((row_index+1, col_index+1))    # diagonal down/right
            gen_moves.append((row_index+1, col_index-1))    # diagonal down/left
            gen_moves.append((row_index-1, col_index+1))    # diagonal up/right
            gen_moves.append((row_index-1, col_index-1))    # diagonal up/left

        # at this point: a lot of extra moves are in gen_moves
        # that aren't confined to the fortress, remove these
        fortress_moves = list()
        for coord in gen_moves:
            if coord in fortress:
                fortress_moves.append(coord)  # only add coordinates that are in the fortress
        # don't include any moves that have a piece with the same color as the current turn (blocked)
        current_valid_moves = self.remove_same_color(fortress_moves)

        # add the general's current position (pass move) as a valid move
        current_valid_moves.append(gen_pos)

        return current_valid_moves


class Cannon(Piece):
    """
    Inherits from the Piece superclass.
    Move type: as many squares as desired along straight lines of board,
                or diagonal lines if in the fortress. Must jump over a piece
                to move (not blocked), can't jump over another cannon (friend or foe),
                can't capture another cannon.
    Uses super() to initialize the color and receive the JanggiGame class.
    Creates an 'image' data member: uses 'name' to access the correct .svg from /assets,
    creates a pygame image for use with JanggiGUI.py
    """
    def __init__(self, game_class, color):
        super().__init__(game_class, color, 7)
        self._name = color + "Cn"
        filename = self._name + ".svg"
        self._image = pygame.image.load(os.path.join("assets", filename))

    def get_image(self):
        """getter for image"""
        return self._image

    def get_name(self):
        """getter for name"""
        return self._name

    def orthogonal_moves(self, direction):
        """
        helper function returns a list of possible orthogonal moves
        based on the direction given
        :param direction: either 'right', 'left', 'down', or 'up'
        :returns: orthogonal_moves
        """
        cannon_pos = self.get_numeric_position()
        row_index, col_index = cannon_pos

        step = None
        next_row = None
        next_column = None
        if direction == "right" or direction == "left":     # if horizontal direction
            if direction == "right":
                step = 1
            if direction == "left":
                step = -1
            next_column = col_index + step                      # move column index either right or left
            next_row = row_index                                # row index unchanged
        if direction == "down" or direction == "up":        # if vertical direction
            if direction == "down":
                step = 1
            if direction == "up":
                step = -1
            next_column = col_index                             # column index unchanged
            next_row = row_index + step                         # move row index either down or up

        orthogonal_moves = list()
        board = self._game.get_board()

        # get next piece if it's on the board, until off the board
        # or a different piece is found...
        if self.on_game_board((next_row, next_column)):
            next_piece = board[next_row][next_column]
            # while next square is empty and on game board, keep moving along straight line
            while next_piece is None and self.on_game_board((next_row, next_column)):
                if direction == "right" or direction == "left":  # move across board based on direction
                    next_column += step
                elif direction == "down" or direction == "up":
                    next_row += step
                if self.on_game_board((next_row, next_column)):
                    next_piece = board[next_row][next_column]
            # a piece has been found, or we're off the board
            if self.on_game_board((next_row, next_column)):     # if still on game board...
                # if not a cannon, can jump over!
                if next_piece is not None and "Cn" not in next_piece.get_name():
                    if direction == "right" or direction == "left":  # move across board based on direction
                        next_column += step
                    elif direction == "down" or direction == "up":
                        next_row += step
                    if self.on_game_board((next_row, next_column)):
                        next_piece = board[next_row][next_column]
                        # while each next square is empty and on the board,
                        # keep moving along straight line AND ADD VALID MOVES
                        while next_piece is None and self.on_game_board((next_row, next_column)):
                            orthogonal_moves.append((next_row, next_column))
                            if direction == "right" or direction == "left":  # move across board based on direction
                                next_column += step
                            elif direction == "down" or direction == "up":
                                next_row += step
                            if self.on_game_board((next_row, next_column)):
                                next_piece = board[next_row][next_column]
                        # a piece has been found, or we're off the board
                        if self.on_game_board((next_row, next_column)):     # if still on game board...
                            # if not a cannon and if an enemy piece, add to valid moves, end loop
                            if next_piece is not None:
                                if "Cn" not in next_piece.get_name() and next_piece.get_color() != self.get_color():
                                    orthogonal_moves.append((next_row, next_column))
        return orthogonal_moves

    def fortress_moves(self):
        """helper function returns a list of possible moves a Cannon can make in a fortress"""
        cannon_pos = self.get_numeric_position()
        row_index, col_index = cannon_pos

        # initialize to blue fortress
        blue_fortress = self._game.get_blue_fortress()
        fortress = blue_fortress
        fort_corners = self._game.get_blue_fortress_corners()
        fort_center = self._game.get_blue_fortress_center()     # list with tuple coord of fort center

        # if the cannon is not in the blue fortress, invert to red fortress coordinates
        if cannon_pos not in blue_fortress:
            self._game.invert_coordinates(fortress)
            self._game.invert_coordinates(fort_corners)
            self._game.invert_coordinates(fort_center)

        # get the object in the fortress center (either a Piece or None)
        fort_center_alg = self._game.numeric_to_algebraic(fort_center[0])
        fort_center_obj = self._game.get_square_contents(fort_center_alg)

        potential_moves = list()
        # if cannon is in a corner, and the center is not empty and not a cannon,
        # can potentially move two squares diagonally
        # (this includes squares outside the fortress which are removed later)
        if cannon_pos in fort_corners and fort_center_obj is not None:
            if "Cn" not in fort_center_obj.get_name():
                potential_moves.append((row_index + 2, col_index + 2))  # diagonal 2 down/right
                potential_moves.append((row_index + 2, col_index - 2))  # diagonal 2 down/left
                potential_moves.append((row_index - 2, col_index + 2))  # diagonal 2 up/right
                potential_moves.append((row_index - 2, col_index - 2))  # diagonal 2 up/left

        # remove any squares not in the fortress
        fortress_moves = list()
        for square in potential_moves:
            if square in fortress:
                fortress_moves.append(square)

        valid_fortress_moves = list()
        for square in fortress_moves:
            # get object found at each square (either Piece or None)
            square_alg = self._game.numeric_to_algebraic(square)
            square_obj = self._game.get_square_contents(square_alg)
            # if empty, valid move
            if square_obj is None:
                valid_fortress_moves.append(square)
            # if not a cannon and an enemy, valid move
            elif "Cn" not in square_obj.get_name() and square_obj.get_color() != self.get_color():
                valid_fortress_moves.append(square)
        return valid_fortress_moves

    def get_valid_moves(self):
        """
        returns a list of valid moves for the Cannon based on the current position,
        uses helper function orthogonal_moves
        """
        cannon_moves = list()
        cannon_moves.extend(self.orthogonal_moves("up"))
        cannon_moves.extend(self.orthogonal_moves("down"))
        cannon_moves.extend(self.orthogonal_moves("right"))
        cannon_moves.extend(self.orthogonal_moves("left"))
        cannon_moves.extend(self.fortress_moves())

        # add cannon's current position (pass move) to valid moves
        cannon_pos = self.get_numeric_position()
        cannon_moves.append(cannon_pos)

        return cannon_moves


class Soldier(Piece):
    """
    Inherits from the Piece superclass.
    Move type: can move forward, left, or right one square, and
                can move diagonally forward if on a fortress corner/center
    Uses super() to initialize the color and receive the JanggiGame class.
    Creates an 'image' data member: uses 'name' to access the correct .svg from /assets,
    creates a pygame image for use with JanggiGUI.py
    """
    def __init__(self, game_class, color):
        super().__init__(game_class, color, 2)
        self._name = color + "Sd"
        filename = self._name + ".svg"
        self._image = pygame.image.load(os.path.join("assets", filename))

    def get_image(self):
        """getter for image"""
        return self._image

    def get_name(self):
        """getter for name"""
        return self._name

    def get_valid_moves(self):
        """
        returns a list of valid moves for the Soldier based on the current position,
        uses helper functions remove_out_of_bounds, remove_same_color for moves blocked
        by friendly pieces, and invert_coordinates from the game class for red vs blue Soldiers
        """
        sold_pos = self.get_numeric_position()
        row_index, col_index = sold_pos      # unpack tuple

        # initialize to blue fortress
        blue_fortress = self._game.get_blue_fortress()
        fort_inner_corners = [(7, 3), (7, 5)]
        fort_outer_corners = [(9, 3), (9, 5)]
        fort_center = [(8, 4)]

        # if soldier is not in blue fortress, invert to red fortress coordinates
        if sold_pos not in blue_fortress:
            self._game.invert_coordinates(fort_inner_corners)
            self._game.invert_coordinates(fort_outer_corners)
            self._game.invert_coordinates(fort_center)

        # if soldier is red, vertical direction is positive (move down game board),
        # if soldier is blue, vertical direction is negative (move up game board)
        if self.get_color() == "r":
            vertical = 1
        else:
            vertical = -1

        sold_moves = list()
        sold_moves.append((row_index+vertical, col_index))      # forward one
        sold_moves.append((row_index, col_index-1))             # left one
        sold_moves.append((row_index, col_index+1))             # right one

        # if in fortress inner corner, can move diagonal to center
        # if in fortress center, can move diagonal to outer corners
        if sold_pos in fort_inner_corners:
            sold_moves.append(fort_center[0])
        if sold_pos in fort_center:
            for corner in fort_outer_corners:
                sold_moves.append(corner)

        # don't include any moves that are off the board
        in_bounds_moves = self.remove_out_of_bounds(sold_moves)
        # don't include any moves that have a piece with the same color as the current turn (blocked)
        all_valid_moves = self.remove_same_color(in_bounds_moves)

        # add soldier's current position (pass move) to valid moves
        all_valid_moves.append(sold_pos)

        return all_valid_moves


# test move sequences below
def main():
    game = JanggiGame()
    game.make_move("e9", "e9")
    game.make_move("e4", "e5")
    game.make_move("e9", "e9")
    game.make_move("e5", "e6")
    game.make_move("e9", "e9")
    game.make_move("e6", "e7")
    print(game.make_move("e9", "e8"))
    game.display_board()


if __name__ == "__main__":
    main()
