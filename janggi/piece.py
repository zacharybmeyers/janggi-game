import os
import logging
import pygame

from janggi.utils import numeric_to_algebraic, algebraic_to_numeric, invert_coordinates


class Piece:
    """Represents a Piece for use in the Game class"""
    def __init__(self, board, color, worth, name, image):
        """
        initializes game, color, and position
        @type board: janggi.board.Board
        """
        self._board = board
        self._color = color
        self._worth = worth
        self._position = None
        self._name = name
        self._image = image

    def get_name(self):
        """getter for name"""
        return self._name

    def get_image(self):
        """getter for image"""
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            color = (255, 0, 0)
            if 'b' == self._color:
                color = (0, 0, 255)
            return pygame.font.SysFont("timesnewroman", 30).render(self._name[1:], True, color)
        return self._image

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
        numeric_pos = algebraic_to_numeric(algebraic_pos)
        return numeric_pos

    def get_valid_moves(self):
        raise NotImplementedError()

    def get_valid_moves_algebraic(self):
        moves = []
        for n in self.get_valid_moves():
            moves.append(numeric_to_algebraic(n))
        return moves

    def set_position(self, alg_coord):
        """setter for position, takes an algebraic coordinate ie 'b1'"""
        self._position = alg_coord


class Chariot(Piece):
    """
    Inherits from the Piece superclass.
    Move type: as many squares as desired along straight lines of board,
                or diagonal lines if in the fortress
    Uses super() to initialize the color and receive the Game class.
    Creates an 'image' data member: uses 'name' to access the correct .svg from /assets,
    creates a pygame image for use with JanggiGUI.py
    """
    def __init__(self, board, color):
        name = color + "Ch"
        filename = name + ".svg"
        image = pygame.image.load(os.path.join("assets", filename))
        super().__init__(board, color, 13, name, image)

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
        valid_square = True
        while valid_square:
            if self._board.on_game_board((next_row, next_column)):  # if next piece is on the board
                # get next piece
                next_piece = self._board.get_contents_numeric((next_row, next_column))
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
        blue_fortress = self._board.get_blue_fortress()
        fortress = blue_fortress
        fort_corners = self._board.get_blue_fortress_corners()
        fort_center = self._board.get_blue_fortress_center()

        # if the chariot is not in the blue fortress, invert to red fortress coordinates
        if chariot_pos not in blue_fortress:
            invert_coordinates(fortress)
            invert_coordinates(fort_corners)
            invert_coordinates(fort_center)

        potential_moves = list()
        # if chariot is in the center or a corner, can move one square diagonally
        if chariot_pos in fort_center or chariot_pos in fort_corners:
            potential_moves.append((row_index + 1, col_index + 1))  # diagonal 1 down/right
            potential_moves.append((row_index + 1, col_index - 1))  # diagonal 1 down/left
            potential_moves.append((row_index - 1, col_index + 1))  # diagonal 1 up/right
            potential_moves.append((row_index - 1, col_index - 1))  # diagonal 1 up/left

        # if chariot is in a fortress corner, and if the center is empty, can move two squares diagonally
        alg_center = numeric_to_algebraic(fort_center[0])
        center_obj = self._board.get_contents_algebraic(alg_center)
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

        return self._board.filter_moves_same_color(fortress_moves, self.get_color())   # remove any squares that are friendly

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
    Uses super() to initialize the color and receive the Game class.
    Creates an 'image' data member: uses 'name' to access the correct .svg from /assets,
    creates a pygame image for use with JanggiGUI.py
    """
    def __init__(self, board, color):
        name = color + "El"
        filename = name + ".svg"
        image = pygame.image.load(os.path.join("assets", filename))
        super().__init__(board, color, 3, name, image)

    def elephant_diagonal_moves(self, direction):
        """
        helper function returns a list of possible diagonal moves 2 squares away
        from the current position based on the direction given.
        verifies the moves aren't blocked, and that they are on the game board with
        the use of on_game_board() and filter_moves_out_of_bounds() helper functions.
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
        if self._board.on_game_board((next_row, next_column)):  # if in bounds
            ortho_square = (next_row, next_column)
            ortho_square_alg = numeric_to_algebraic(ortho_square)
            ortho_obj = self._board.get_contents_algebraic(ortho_square_alg)
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
                for first_diag in self._board.filter_moves_out_of_bounds(first_diagonals):
                    first_diag_alg = numeric_to_algebraic(first_diag)
                    first_diag_obj = self._board.get_contents_algebraic(first_diag_alg)
                    if first_diag_obj is None:  # if empty (clear)
                        # iterate through second diagonals that are on the board
                        for second_diag in self._board.filter_moves_out_of_bounds(second_diagonals):
                            second_diag_alg = numeric_to_algebraic(second_diag)
                            second_diag_obj = self._board.get_contents_algebraic(second_diag_alg)
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
    Uses super() to initialize the color and receive the Game class.
    Creates an 'image' data member: uses 'name' to access the correct .svg from /assets,
    creates a pygame image for use with JanggiGUI.py
    """
    def __init__(self, board, color):
        name = color + "Hs"
        filename = name + ".svg"
        image = pygame.image.load(os.path.join("assets", filename))
        super().__init__(board, color, 5, name, image)

    def horse_diagonal_moves(self, direction):
        """
        helper function returns a list of possible diagonal moves 1 square away
        based on the direction given.
        verifies the moves aren't blocked, and that they are on the game board with
        the use of the on_game_board() and filter_moves_out_of_bounds() helper functions.
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
        if self._board.on_game_board((next_row, next_column)):  # if in bounds
            ortho_square = (next_row, next_column)
            ortho_square_alg = numeric_to_algebraic(ortho_square)
            ortho_obj = self._board.get_contents_algebraic(ortho_square_alg)
            if ortho_obj is None:  # if orthogonal square is not blocked
                # make list of 2 possible diagonals (depending on direction)
                diagonals = None
                if direction == "up" or direction == "down":
                    diagonals = [(next_row+step, next_column+1), (next_row+step, next_column-1)]
                if direction == "right" or direction == "left":
                    diagonals = [(next_row+1, next_column+step), (next_row-1, next_column+step)]
                # iterate only through the diagonals that are on the game board
                for diagonal in self._board.filter_moves_out_of_bounds(diagonals):
                    diagonal_alg = numeric_to_algebraic(diagonal)
                    diagonal_obj = self._board.get_contents_algebraic(diagonal_alg)
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
    Uses super() to initialize the color and receive the Game class.
    Creates an 'image' data member: uses 'name' to access the correct .svg from /assets,
    creates a pygame image for use with JanggiGUI.py
    """
    def __init__(self, board, color):
        name = color + "Gd"
        filename = name + ".svg"
        image = pygame.image.load(os.path.join("assets", filename))
        super().__init__(board, color, 3, name, image)

    def get_valid_moves(self):
        """
        returns a list of valid moves for the Guard based on the current position,
        uses helper functions filter_moves_same_color for moves blocked by friendly pieces
        """
        guard_pos = self.get_numeric_position()
        row_index, col_index = guard_pos

        # initialize to blue fortress
        blue_fortress = self._board.get_blue_fortress()
        fortress = blue_fortress
        fort_corners = self._board.get_blue_fortress_corners()
        fort_center = self._board.get_blue_fortress_center()

        # if the guard is not in the blue fortress, invert to red fortress coordinates
        if guard_pos not in blue_fortress:
            invert_coordinates(fortress)
            invert_coordinates(fort_corners)
            invert_coordinates(fort_center)

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

        all_moves = self._board.filter_moves_same_color(fortress_moves, self.get_color())  # remove any squares that are friendly

        # add guard's current position (pass move) to valid moves
        all_moves.append(guard_pos)

        return all_moves


class General(Piece):
    """
    Inherits from the Piece superclass.
    Move type: confined to fortress, moves one square orthogonally, or one
                diagonally if in the center or on a corner
    Uses super() to initialize the color and receive the Game class.
    Creates an 'image' data member: uses 'name' to access the correct .svg from /assets,
    creates a pygame image for use with JanggiGUI.py
    """
    def __init__(self, board, color):
        name = color + "Gn"
        filename = name + ".svg"
        image = pygame.image.load(os.path.join("assets", filename))
        super().__init__(board, color, 99, name, image)

    def get_valid_moves(self):
        """
        returns a list of valid moves for the General based on the current position,
        uses helper functions filter_moves_same_color for moves blocked by friendly pieces
        and invert_coordinates from the game class for red vs blue Generals
        """
        gen_pos = self.get_numeric_position()
        row_index, col_index = gen_pos

        # initialize to blue fortress
        blue_fortress = self._board.get_blue_fortress()
        fortress = blue_fortress
        fort_corners = self._board.get_blue_fortress_corners()
        fort_center = self._board.get_blue_fortress_center()

        # if the general is not in the blue fortress, invert to red fortress coordinates
        if gen_pos not in blue_fortress:
            invert_coordinates(fortress)
            invert_coordinates(fort_corners)
            invert_coordinates(fort_center)

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
        current_valid_moves = self._board.filter_moves_same_color(fortress_moves, self.get_color())

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
    Uses super() to initialize the color and receive the Game class.
    Creates an 'image' data member: uses 'name' to access the correct .svg from /assets,
    creates a pygame image for use with JanggiGUI.py
    """
    def __init__(self, board, color):
        name = color + "Cn"
        filename = name + ".svg"
        image = pygame.image.load(os.path.join("assets", filename))
        super().__init__(board, color, 7, name, image)

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

        # get next piece if it's on the board, until off the board
        # or a different piece is found...
        if self._board.on_game_board((next_row, next_column)):
            next_piece = self._board.get_contents_numeric((next_row, next_column))
            # while next square is empty and on game board, keep moving along straight line
            while next_piece is None and self._board.on_game_board((next_row, next_column)):
                if direction == "right" or direction == "left":  # move across board based on direction
                    next_column += step
                elif direction == "down" or direction == "up":
                    next_row += step
                if self._board.on_game_board((next_row, next_column)):
                    next_piece = self._board.get_contents_numeric((next_row, next_column))
            # a piece has been found, or we're off the board
            if self._board.on_game_board((next_row, next_column)):     # if still on game board...
                # if not a cannon, can jump over!
                if next_piece is not None and "Cn" not in next_piece.get_name():
                    if direction == "right" or direction == "left":  # move across board based on direction
                        next_column += step
                    elif direction == "down" or direction == "up":
                        next_row += step
                    if self._board.on_game_board((next_row, next_column)):
                        next_piece = self._board.get_contents_numeric((next_row, next_column))
                        # while each next square is empty and on the board,
                        # keep moving along straight line AND ADD VALID MOVES
                        while next_piece is None and self._board.on_game_board((next_row, next_column)):
                            orthogonal_moves.append((next_row, next_column))
                            if direction == "right" or direction == "left":  # move across board based on direction
                                next_column += step
                            elif direction == "down" or direction == "up":
                                next_row += step
                            if self._board.on_game_board((next_row, next_column)):
                                next_piece = self._board.get_contents_numeric((next_row, next_column))
                        # a piece has been found, or we're off the board
                        if self._board.on_game_board((next_row, next_column)):     # if still on game board...
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
        blue_fortress = self._board.get_blue_fortress()
        fortress = blue_fortress
        fort_corners = self._board.get_blue_fortress_corners()
        fort_center = self._board.get_blue_fortress_center()     # list with tuple coord of fort center

        # if the cannon is not in the blue fortress, invert to red fortress coordinates
        if cannon_pos not in blue_fortress:
            invert_coordinates(fortress)
            invert_coordinates(fort_corners)
            invert_coordinates(fort_center)

        # get the object in the fortress center (either a Piece or None)
        fort_center_alg = numeric_to_algebraic(fort_center[0])
        fort_center_obj = self._board.get_contents_algebraic(fort_center_alg)

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
            square_alg = numeric_to_algebraic(square)
            square_obj = self._board.get_contents_algebraic(square_alg)
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
    Uses super() to initialize the color and receive the Game class.
    Creates an 'image' data member: uses 'name' to access the correct .svg from /assets,
    creates a pygame image for use with JanggiGUI.py
    """
    def __init__(self, board, color):
        name = color + "Sd"
        filename = name + ".svg"
        image = pygame.image.load(os.path.join("assets", filename))
        super().__init__(board, color, 2, name, image)

    def get_valid_moves(self):
        """
        returns a list of valid moves for the Soldier based on the current position,
        uses helper functions filter_moves_out_of_bounds, filter_moves_same_color for moves blocked
        by friendly pieces, and invert_coordinates from the game class for red vs blue Soldiers
        """
        sold_pos = self.get_numeric_position()
        row_index, col_index = sold_pos      # unpack tuple

        # initialize to blue fortress
        blue_fortress = self._board.get_blue_fortress()
        fort_inner_corners = [(7, 3), (7, 5)]
        fort_outer_corners = [(9, 3), (9, 5)]
        fort_center = [(8, 4)]

        # if soldier is not in blue fortress, invert to red fortress coordinates
        if sold_pos not in blue_fortress:
            invert_coordinates(fort_inner_corners)
            invert_coordinates(fort_outer_corners)
            invert_coordinates(fort_center)

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
        in_bounds_moves = self._board.filter_moves_out_of_bounds(sold_moves)
        # don't include any moves that have a piece with the same color as the current turn (blocked)
        all_valid_moves = self._board.filter_moves_same_color(in_bounds_moves, self.get_color())

        # add soldier's current position (pass move) to valid moves
        all_valid_moves.append(sold_pos)

        return all_valid_moves
