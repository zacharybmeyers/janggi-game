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
        """setter for position, takes a tuple of x,y coordinates"""
        self._position = tup


class Chariot(Piece):
    """inherits from the piece superclass"""
    def __init__(self, color):
        super().__init__(color)
        self._name = color + "Char"

    def get_name(self):
        """getter for name"""
        return self._name


class Elephant(Piece):
    """inherits from the piece superclass"""
    def __init__(self, color):
        super().__init__(color)
        self._name = color + "Ele"

    def get_name(self):
        """getter for name"""
        return self._name


class Horse(Piece):
    """inherits from the piece superclass"""
    def __init__(self, color):
        super().__init__(color)
        self._name = color + "Horse"

    def get_name(self):
        """getter for name"""
        return self._name


class Guard(Piece):
    """inherits from the piece superclass"""
    def __init__(self, color):
        super().__init__(color)
        self._name = color + "Guard"

    def get_name(self):
        """getter for name"""
        return self._name


class General(Piece):
    """inherits from the piece superclass"""
    def __init__(self, color):
        super().__init__(color)
        self._name = color + "Gen"

    def get_name(self):
        """getter for name"""
        return self._name


class Cannon(Piece):
    """inherits from the piece superclass"""
    def __init__(self, color):
        super().__init__(color)
        self._name = color + "Cann"

    def get_name(self):
        """getter for name"""
        return self._name


class Soldier(Piece):
    """inherits from the piece superclass"""
    def __init__(self, color):
        super().__init__(color)
        self._name = color + "Sold"

    def get_name(self):
        """getter for name"""
        return self._name


class JanggiGame:
    """Represents a game of Janggi"""
    def __init__(self):
        """initializes private data members"""
        self._board = [
            ["1", Chariot("r"), Elephant("r"), Horse("r"), Guard("r"), None,
             Guard("r"), Horse("r"), Elephant("r"), Chariot("r")],
            ["2", None, None, None, None, General("red"), None, None, None, None],
            ["3", None, Cannon("r"), None, None, None, None, None, Cannon("r"), None],
            ["4", Soldier("r"), None, Soldier("r"), None, Soldier("r"), None,
             Soldier("r"), None, Soldier("r")],
            ["5", None, None, None, None, None, None, None, None, None],
            ["6", None, None, None, None, None, None, None, None, None],
            ["7", Soldier("b"), None, Soldier("b"), None, Soldier("b"), None,
             Soldier("b"), None, Soldier("b")],
            ["8", None, Cannon("b"), None, None, None, None, None, Cannon("b"), None],
            ["9", None, None, None, None, General("b"), None, None, None, None],
            ["10", Chariot("b"), Elephant("b"), Horse("b"), Guard("b"), None,
             Guard("b"), Horse("b"), Elephant("b"), Chariot("b")],
        ]

        # set starting positions for game pieces
        row_index = 0
        for row in self._board:
            col_index = 0
            for elem in row:
                if type(elem) in Piece.__subclasses__():        # if element is a Piece
                    elem.set_position((col_index, row_index))   # set the position
                col_index += 1
            row_index += 1

        self._turn = "Blue"

    def get_turn(self):
        """getter for turn"""
        return self._turn

    def set_turn(self, color):
        """setter for turn"""
        self._turn = color

    def get_board(self):
        """getter for board"""
        return self._board

    def list_format(self, alist, col_width):
        """
        helper function takes a list and column width and
        returns a string with the proper column width between
        for each list element
        """
        print_str = ""
        for elem in alist:
            if type(elem) in Piece.__subclasses__():    # if child of Piece class, use name
                elem_str = elem.get_name()
            elif elem is None:                  # if None, use "x"
                elem_str = "x"
            else:                               # else cast element to string
                elem_str = str(elem)
            square_len = len(elem_str)
            space_len = col_width - square_len  # amount of spaces = desired column width - length of current square
            print_str += elem_str               # add current string to print_str
            for i in range(space_len):
                print_str += " "                # add the desired amount of spaces
        return print_str

    def display_board(self, col_width):
        """
        displays the game board with the specified column width
        with the use of the list_format helper function
        """
        header = ["0", "A", "B", "C", "D", "E", "F", "G", "H", "I"]
        print(self.list_format(header, col_width))     # print header
        for row in self.get_board():
            print(self.list_format(row, col_width))    # print each row of the board


game = JanggiGame()
game.display_board(8)
