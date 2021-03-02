# Author:       Zachary Meyers
# Date:         2021-02-24
# Description:

class JanggiGame:
    """Represents a game of Janggi"""
    def __init__(self):
        """initializes private data members"""
        self._game_state = "UNFINISHED"
        self._in_check = None
        self._turn = "b"
        self._board = [
            [Chariot(self, "r"), Elephant(self, "r"), Horse(self, "r"), Guard(self, "r"), None,
             Guard(self, "r"), Horse(self, "r"), Elephant(self, "r"), Chariot(self, "r")],
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
             Guard(self, "b"), Horse(self, "b"), Elephant(self, "b"), Chariot(self, "b")],
        ]
        # set starting positions for game pieces
        row_index = 0
        for row in self._board:
            col_index = 0
            for elem in row:
                if type(elem) in Piece.__subclasses__():        # if element is a Piece
                    num_coord = (row_index, col_index)              # create coordinate
                    alg_coord = numeric_to_algebraic(num_coord)     # convert to algebraic
                    elem.set_position(alg_coord)                    # set the position
                col_index += 1
            row_index += 1

    def display_board(self):
        """
        displays the game board, uses the
        list_format helper function for pretty output
        """
        header = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
        print("   ", list_format(header))                          # print header
        for num, row in enumerate(self.get_board()):               # print each row of the board
            if num+1 != 10:
                print(num+1, " ", list_format(row), " ", num+1)    # add extra space for single digit rows
            else:
                print(num+1, "", list_format(row), "", num+1)      # print row 10 as normal
        print("   ", list_format(header))                          # print footer (header)

    def get_in_check(self):
        """getter for in check"""
        return self._in_check

    def set_in_check(self, color):
        """setter for in check, where color is a string for red or blue"""
        self._in_check = color

    def is_in_check(self, color):
        """Takes a color and returns True if in check, False otherwise"""
        if self.get_in_check() == color:
            return True
        else:
            return False

    def get_game_state(self):
        """getter for game state"""
        return self._game_state

    def set_game_state(self, game_state):
        """setter for game state, where game_state is a string"""
        self._game_state = game_state

    def get_turn(self):
        """getter for turn"""
        return self._turn

    def set_turn(self, color):
        """setter for turn"""
        self._turn = color

    def get_board(self):
        """getter for board"""
        return self._board

    def get_square_contents(self, alg_coord):
        """
        Returns whatever is found at the given square's position in the game board.
        :param alg_coord: in string format ie 'b1'
        :return: the object in the square (or None)
        """
        row_index, col_index = algebraic_to_numeric(alg_coord)
        board = self.get_board()
        return board[row_index][col_index]

    def play_game(self):
        """helper function to play the game"""
        self.display_board()
        while self.get_game_state() == "UNFINISHED":
            start = input("start square: ")
            end = input("end square: ")
            self.make_move(start, end)
            self.display_board()
            keep_playing = input("continue (Y/N)? ")
            if keep_playing == "N":
                self.set_game_state("BLUE_WON")

    def make_move(self, start, end):
        """

        :param start:
        :param end:
        :return:
        """
        # get the Piece from the start square
        piece_obj = self.get_square_contents(start)
        if piece_obj is None:
            return False                                # invalid move if there's no piece
        if self.get_turn() != piece_obj.get_color():    # invalid move if not starting square's turn
            return False
        if self.get_game_state() != "UNFINISHED":       # invalid move if game is finished
            return False
        end_tup = algebraic_to_numeric(end)
        if end_tup not in piece_obj.get_valid_moves():  # invalid if end position is not valid for this piece
            return False

        # otherwise, valid move
        start_tup = algebraic_to_numeric(start)
        start_row, start_col = start_tup
        end_row, end_col = end_tup              # unpack end square tup
        board = self.get_board()                # get board

        # move Piece object to new square
        # (removes opposing piece or fills empty square)
        board[end_row][end_col] = piece_obj
        piece_obj.set_position(end)             # store new position (algebraic coordinate)
        board[start_row][start_col] = None      # clear old square

        # UPDATE GAME STATE IF NECESSARY (win check)

        # update turn
        if self.get_turn() == "b":
            self.set_turn("r")
        elif self.get_turn() == "r":
            self.set_turn("b")
        return True


class Piece:
    """Represents a game piece"""
    def __init__(self, game_class, color):
        """initializes name, color, and position"""
        self._game = game_class
        self._color = color
        self._position = None

    def get_color(self):
        """getter for color"""
        return self._color

    def get_position(self):
        """getter for position"""
        return self._position

    def set_position(self, alg_coord):
        """setter for position, takes an algebraic coordinate ie 'b1'"""
        self._position = alg_coord

    def remove_out_of_bounds(self, moves_list):
        """
        helper function takes a list of tuples of potential moves
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
        helper function takes a list of valid tuple coordinates,
        removes any that are the same color as the current turn,
        and returns the new list
        """
        valid_moves = []
        board = self._game.get_board()
        for coord in tup_list:
            row_index, col_index = coord
            piece_obj = board[row_index][col_index]
            if piece_obj is None:
                valid_moves.append(coord)           # valid if empty
            elif piece_obj.get_color() != self._game.get_turn():
                valid_moves.append(coord)           # valid if opposite player color
        return valid_moves


class Chariot(Piece):
    """inherits from the piece superclass"""
    def __init__(self, game_class, color):
        super().__init__(game_class, color)
        self._name = color + "Ch"

    def get_name(self):
        """getter for name"""
        return self._name


class Elephant(Piece):
    """inherits from the piece superclass"""
    def __init__(self, game_class, color):
        super().__init__(game_class, color)
        self._name = color + "El"

    def get_name(self):
        """getter for name"""
        return self._name


class Horse(Piece):
    """inherits from the piece superclass"""
    def __init__(self, game_class, color):
        super().__init__(game_class, color)
        self._name = color + "Hs"

    def get_name(self):
        """getter for name"""
        return self._name


class Guard(Piece):
    """inherits from the piece superclass"""
    def __init__(self, game_class, color):
        super().__init__(game_class, color)
        self._name = color + "Gd"

    def get_name(self):
        """getter for name"""
        return self._name


class General(Piece):
    """inherits from the piece superclass"""
    def __init__(self, game_class, color):
        super().__init__(game_class, color)
        self._name = color + "Gn"

    def get_name(self):
        """getter for name"""
        return self._name

    def get_valid_moves(self):
        """

        :return:
        """
        # initialize to blue fortress
        fort_center = [(8, 4)]
        fort_outer = [(7, 3), (8, 3), (9, 3), (7, 4), (9, 4), (7, 5), (8, 5), (9, 5)]
        left_inner_corner = [(7, 3)]
        right_inner_corner = [(7, 5)]
        left_outer_corner = [(9, 3)]
        right_outer_corner = [(9, 5)]
        fort_midpoints = [(7, 4), (8, 3), (8, 5), (9, 4)]
        vertical_midpoint = 4   # unchanged whether blue or red
        horizontal_midpoint = 8

        # if general is red, invert fortress to red
        if self.get_color() == "r":
            invert_coordinates(fort_center)
            invert_coordinates(fort_outer)
            invert_coordinates(left_inner_corner)
            invert_coordinates(right_inner_corner)
            invert_coordinates(left_outer_corner)
            invert_coordinates(right_outer_corner)
            invert_coordinates(fort_midpoints)
            horizontal_midpoint = 9 - 8     # invert manually

        gen_moves = list()
        algebraic_pos = self.get_position()
        numeric_pos = algebraic_to_numeric(algebraic_pos)

        # CENTER/OUTER MOVEMENT
        # if pos is center fortress, all outer squares are valid moves
        if numeric_pos in fort_center:
            for pos in fort_outer:
                gen_moves.append(pos)
        # if pos is in outer squares, center fortress is valid move
        if numeric_pos in fort_outer:
            gen_moves.append(fort_center[0])

        # MIDPOINT MOVEMENT
        row_index, col_index = numeric_pos      # unpack tuple
        if numeric_pos not in fort_center:
            # if vertical midpoint of fortress, can move left or right
            if col_index == vertical_midpoint:
                gen_moves.append((row_index, col_index+1))
                gen_moves.append((row_index, col_index-1))
            # if horizontal midpoint of fortress (blue or red), can move up or down
            if row_index == horizontal_midpoint:
                gen_moves.append((row_index+1, col_index))
                gen_moves.append((row_index-1, col_index))

        # CORNER MOVEMENT
        # if left inner corner, row+1 or col+1 are valid
        if numeric_pos in left_inner_corner:
            gen_moves.append((row_index+1, col_index))
            gen_moves.append((row_index, col_index+1))
        # if right inner corner, row+1 or col-1 are valid
        if numeric_pos in right_inner_corner:
            gen_moves.append((row_index+1, col_index))
            gen_moves.append((row_index, col_index-1))
        # if left outer corner, row-1 or col+1 are valid
        if numeric_pos in left_outer_corner:
            gen_moves.append((row_index-1, col_index))
            gen_moves.append((row_index, col_index+1))
        # if right outer corner, row-1 or col-1 are valid
        if numeric_pos in right_outer_corner:
            gen_moves.append((row_index-1, col_index))
            gen_moves.append((row_index, col_index-1))

        # don't include any moves that are off the board
        in_bounds_moves = self.remove_out_of_bounds(gen_moves)
        # don't include any moves that have a piece with the same color as the current turn (blocked)
        all_valid_moves = self.remove_same_color(in_bounds_moves)

        return all_valid_moves


class Cannon(Piece):
    """inherits from the piece superclass"""
    def __init__(self, game_class, color):
        super().__init__(game_class, color)
        self._name = color + "Cn"

    def get_name(self):
        """getter for name"""
        return self._name


class Soldier(Piece):
    """
    inherits from the piece superclass
    can move forward or sideways one square,
    if in fortress can move diagonal one square in and out of the center
    """
    def __init__(self, game_class, color):
        super().__init__(game_class, color)
        self._name = color + "Sd"

    def get_name(self):
        """getter for name"""
        return self._name

    def get_valid_moves(self):
        """
        returns a list of valid moves based on the current position,
        uses helper functions remove_out_of_bounds and invert_coordinates
        (for cases of red or blue pieces)
        """
        algebraic_pos = self.get_position()
        numeric_pos = algebraic_to_numeric(algebraic_pos)
        row_index, col_index = numeric_pos      # unpack tuple

        # if soldier is red, vertical direction is positive (move down game board),
        # if soldier is blue, vertical direction is negative (move up game board)
        vertical = -1
        if self.get_color() == "r":
            vertical = 1

        sold_moves = list()
        sold_moves.append((row_index+vertical, col_index))      # forward one
        sold_moves.append((row_index, col_index-1))             # left one
        sold_moves.append((row_index, col_index+1))             # right one

        # assume piece is blue, initialize to red fortress
        fort_inner_corners = [(2, 3), (2, 5)]
        fort_outer_corners = [(0, 3), (0, 5)]
        fort_center = [(1, 4)]
        # invert rows if red piece in blue fortress
        if self.get_color() == "r":
            invert_coordinates(fort_inner_corners)
            invert_coordinates(fort_outer_corners)
            invert_coordinates(fort_center)
        # if in enemy fortress corner, can move diagonal to center
        # if in enemy fortress center, can move diagonal to outer corners
        if numeric_pos in fort_inner_corners:
            sold_moves.append(fort_center[0])
        if numeric_pos in fort_center:
            for corner in fort_outer_corners:
                sold_moves.append(corner)

        # don't include any moves that are off the board
        in_bounds_moves = self.remove_out_of_bounds(sold_moves)
        # don't include any moves that have a piece with the same color as the current turn (blocked)
        all_valid_moves = self.remove_same_color(in_bounds_moves)

        return all_valid_moves


def algebraic_to_numeric(alg_coord):
    """
    helper function converts algebraic coordinates to numeric coordinates
    :param alg_coord: in string format ie 'b1'
    :return: the tuple with integer (x, y) coordinates
    """
    column = alg_coord[0]
    row = alg_coord[1]
    row_index = int(row) - 1
    col_index = 0
    columns = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
    for index, letter in enumerate(columns):
        if letter == column:
            col_index = index
    return row_index, col_index


def numeric_to_algebraic(num_coord):
    """
    helper function converts numeric coordinates to algebraic coordinates
    :param num_coord: in tuple format ie (1, 2)
    :return: the string with algebraic ie 'b1' coordinates
    """
    alg_str = ""
    row_index = num_coord[0]
    row_index += 1
    col_index = num_coord[1]
    columns = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
    for index, letter in enumerate(columns):
        if index == col_index:
            alg_str += letter
    alg_str += str(row_index)
    return alg_str


def invert_coordinates(tup_list):
    """
    helper function inverts a list of coordinates (tuples) across the Janggi board.
    Returns: None
    """
    for index, coord in enumerate(tup_list):
        row = coord[0]
        col = coord[1]
        inverted_coord = (9 - row, col)
        del tup_list[index]                 # remove current coord
        tup_list.append(inverted_coord)     # add inverted coord


def list_format(alist):
    """
    helper function takes a list and returns a
    string with the proper column width (9) for
    each list element
    """
    print_str = ""
    for elem in alist:
        if type(elem) in Piece.__subclasses__():    # if child of Piece class, use 3 letter name
            elem_str = elem.get_name()
            spaces = "   "                          # 3 spaces for either side
        elif elem is None:                          # if empty, use "---"
            elem_str = "---"
            spaces = "   "
        else:                                       # header letter ie 'A'
            elem_str = str(elem)
            spaces = "    "                         # 4 spaces for either side
        print_str += spaces
        print_str += elem_str
        print_str += spaces
    return print_str


def main():
    game = JanggiGame()
    # game.play_game()
    game.display_board()


if __name__ == "__main__":
    main()
