def algebraic_to_numeric(alg_coord: str) -> (int, int):
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


def numeric_to_algebraic(num_coord: (int, int)) -> str:
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


def invert_coordinates(tup_list: list[(int, int)]) -> None:
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


def swap_color(color: str) -> str:
    return 'b' == color and 'r' or 'b'
