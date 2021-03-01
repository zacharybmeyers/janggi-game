# Author:       Zachary Meyers
# Date:         2021-02-24
# Description:

class Piece:
    """Represents a game piece"""
    def __init__(self, color):
        """initializes name, color, and position"""
        self._color = color
        self._position = None

    def get_color(self):
        """getter for color"""
        return self._color

    def get_position(self):
        """getter for position"""
        return self._position

    def set_position(self, tup):
        """setter for position, takes a tuple of coordinates (row_index, col_index)"""
        self._position = tup

    def remove_out_of_bounds(self, moves_list):
        """
        helper function takes a list of tuples of potential moves
        and returns a list without any moves that are off the game board
        """
        valid_moves = []
        for coord in moves_list:
            row, col = coord        # unpack tuple
            if 0 <= row <= 9 and 0 <= col <= 8:    # if column is in [A...I] and row is in [0...9]
                valid_moves.append(coord)          # add to valid moves
        return valid_moves


class Chariot(Piece):
    """inherits from the piece superclass"""
    def __init__(self, color):
        super().__init__(color)
        self._name = color + "Ch"

    def get_name(self):
        """getter for name"""
        return self._name


class Elephant(Piece):
    """inherits from the piece superclass"""
    def __init__(self, color):
        super().__init__(color)
        self._name = color + "El"

    def get_name(self):
        """getter for name"""
        return self._name


class Horse(Piece):
    """inherits from the piece superclass"""
    def __init__(self, color):
        super().__init__(color)
        self._name = color + "Hs"

    def get_name(self):
        """getter for name"""
        return self._name


class Guard(Piece):
    """inherits from the piece superclass"""
    def __init__(self, color):
        super().__init__(color)
        self._name = color + "Gd"

    def get_name(self):
        """getter for name"""
        return self._name


class General(Piece):
    """inherits from the piece superclass"""
    def __init__(self, color):
        super().__init__(color)
        self._name = color + "Gn"

    def get_name(self):
        """getter for name"""
        return self._name


class Cannon(Piece):
    """inherits from the piece superclass"""
    def __init__(self, color):
        super().__init__(color)
        self._name = color + "Cn"

    def get_name(self):
        """getter for name"""
        return self._name


class Soldier(Piece):
    """
    inherits from the piece superclass
    can move forward or sideways one square
    """
    def __init__(self, color):
        super().__init__(color)
        self._name = color + "Sd"

    def get_name(self):
        """getter for name"""
        return self._name

    def get_valid_moves(self):
        """
        returns a list of valid moves based on the current position,
        uses helper function from Piece superclass remove_out_of_bounds
        """
        # if soldier is red, vertical direction is positive (move down game board),
        # if soldier is blue, vertical direction is negative (move up game board)
        vertical = 1
        if self.get_color() == "b":
            vertical = -1
        sold_moves = []
        row_index, col_index = self.get_position()              # unpack tuple
        sold_moves.append((row_index+vertical, col_index))      # forward one
        sold_moves.append((row_index, col_index-1))             # left one
        sold_moves.append((row_index, col_index+1))             # right one
        valid_moves = self.remove_out_of_bounds(sold_moves)     # remove any moves that are off the board
        return valid_moves


class JanggiGame:
    """Represents a game of Janggi"""
    def __init__(self):
        """initializes private data members"""
        self._game_state = "UNFINISHED"
        self._in_check = None
        self._turn = "b"
        self._board = [
            [Chariot("r"), Elephant("r"), Horse("r"), Guard("r"), None,
             Guard("r"), Horse("r"), Elephant("r"), Chariot("r")],
            [None, None, None, None, General("r"), None, None, None, None],
            [None, Cannon("r"), None, None, None, None, None, Cannon("r"), None],
            [Soldier("r"), None, Soldier("r"), None, Soldier("r"), None,
             Soldier("r"), None, Soldier("r")],
            [None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None],
            [Soldier("b"), None, Soldier("b"), None, Soldier("b"), None,
             Soldier("b"), None, Soldier("b")],
            [None, Cannon("b"), None, None, None, None, None, Cannon("b"), None],
            [None, None, None, None, General("b"), None, None, None, None],
            [Chariot("b"), Elephant("b"), Horse("b"), Guard("b"), None,
             Guard("b"), Horse("b"), Elephant("b"), Chariot("b")],
        ]
        # set starting positions for game pieces
        row_index = 0
        for row in self._board:
            col_index = 0
            for elem in row:
                if type(elem) in Piece.__subclasses__():        # if element is a Piece
                    elem.set_position((row_index, col_index))   # set the position
                col_index += 1
            row_index += 1

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

    def list_format(self, alist):
        """
        helper function takes a list and returns a
        string with the proper column width (9) between
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

    def display_board(self):
        """
        displays the game board with the help
        of the list_format helper function
        """
        header = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
        print("   ", self.list_format(header))                          # print header
        for num, row in enumerate(self.get_board()):                    # print each row of the board
            if num+1 != 10:
                print(num+1, " ", self.list_format(row), " ", num+1)    # add extra space for single digit rows
            else:
                print(num+1, "", self.list_format(row), "", num+1)      # print row 10 as normal
        print("   ", self.list_format(header))                          # print footer (header)

    def play_game(self):
        """helper function to play the game"""
        while self.get_game_state() == "UNFINISHED":
            self.display_board(8)
            start = input("start square: ")
            end = input("end square: ")
            self.make_move(start, end)
            keep_playing = input("continue (Y/N)? ")
            if keep_playing == "N":
                self.set_game_state("BLUE_WON")

    def algebraic_to_numeric(self, alg_coord):
        """
        helper function converts algebraic coordinates to numeric coordinates
        :param square: in string format ie 'b1'
        :return: the tuple with integer (x, y) coordinates
        """
        column = alg_coord[0]
        row = alg_coord[1]
        row_index = int(row) - 1
        columns = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
        for index, letter in enumerate(columns):
            if letter == column:
                col_index = index
        return row_index, col_index

    def get_square_contents(self, alg_coord):
        """
        Returns whatever is found at the given square's position in the game board.
        :param alg_coord: in string format ie 'b1'
        :return: the object in the square (or None)
        """
        row_index, col_index = self.algebraic_to_numeric(alg_coord)
        board = self.get_board()
        return board[row_index][col_index]

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
        end_tup = self.algebraic_to_numeric(end)
        if end_tup not in piece_obj.get_valid_moves():  # invalid if end position is not valid for this piece
            return False

        # otherwise, valid move
        start_tup = self.algebraic_to_numeric(start)
        start_row, start_col = start_tup
        end_row, end_col = end_tup              # unpack new square tup
        board = self.get_board()                # get board
        board[end_row][end_col] = piece_obj     # move Piece object to new square
        piece_obj.set_position(end_tup)         # store new position as tuple
        board[start_row][start_col] = None      # clear old square

        # NEED TO VERIFY MAKE MOVE IS WORKING FOR RED SOLDIERS
        # REMOVE ANY CAPTURED PIECE IF NECESSARY
        # UPDATE GAME STATE IF NECESSARY (win check)

        # update turn
        if self.get_turn() == "b":
            self.set_turn("r")
        elif self.get_turn() == "r":
            self.set_turn("b")
        return True


def main():
    game = JanggiGame()
    game.display_board()
    print(game.get_square_contents('e2'))
    game.make_move('a7', 'a6')
    game.display_board()

    # NEED TO VERIFY MAKE MOVE IS WORKING FOR RED SOLDIERS


if __name__ == "__main__":
    main()