#!/usr/bin/env python3

# Author:       Zachary Meyers
# Date:         2021-03-23
# Description:  This module creates a simple GUI with pygame for playing a game of Janggi,
#               and makes use of the logic from the JanggiGame module.
#               All images used in the assets directory are public domain.
#               Each child instance of the Piece class in JanggiGame has a data member
#               pointing to a corresponding piece image in assets.
#               There are various helper functions that...:
#                   --determine where to blit game pieces
#                   --set boundaries (rectangles) for valid mouse clicks
#                   --create images for desired text to display
#                   --blit the current state of the game board
#               The main function has a while loop that...:
#                   --displays/refreshes the game board
#                   --makes moves (if valid)
#                   --displays a message if a move is invalid
#                   --displays a winning message when the game is finished
#               The game window is not resizeable.

import pygame
import os
from JanggiGame import JanggiGame


def get_pixel_coordinates():
    """
    helper function returns a dictionary with key = algebraic position
    and val = pixel coordinate for the GUI
    """
    # loop to get pixel coordinates for each algebraic position
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    pixel_dict = dict()
    y_coord = 33 + 50
    for i in range(1, 11):
        x_coord = 33 + 45
        for letter in letters:
            alg_coord = letter + str(i)
            if x_coord <= 561 + 45:
                pixel_dict[alg_coord] = (x_coord, y_coord)
            x_coord += 66
        y_coord += 66
    return pixel_dict


def get_board_rectangles():
    """
    helper function returns a dictionary with key = algebraic coordinate,
    val = 40x40 Rectangle for that square (used for determining mouse clicks)
    """
    pixel_dict = get_pixel_coordinates()
    board_rectangles = dict()
    for alg_coord, pixel_coord in pixel_dict.items():
        cx, cy = pixel_coord
        # create a 40x40 rectangle around the current center position
        rect = pygame.Rect(0, 0, 40, 40)
        rect.center = cx, cy
        board_rectangles[alg_coord] = rect
    return board_rectangles


def get_string_images(list_of_strings):
    """
    helper functions takes a list of strings and returns a
    dictionary with key = letter,
    val = pygame Surface object
    """
    image_dict = dict()
    pygame.init()
    font = pygame.font.SysFont("timesnewroman", 30)
    for a_string in list_of_strings:
        black = (0, 0, 0)
        img = font.render(a_string.upper(), True, black)
        image_dict[a_string] = img
    return image_dict


def blit_current_board(game, screen):
    """
    helper function takes a current instance of the JanggiGame class,
    iterates through the pieces and blits each one to the current pygame screen
    """
    # fill background with orange color
    screen.fill((247, 147, 30))
    # load a background board image (594x660), blit to screen
    bgd_image = pygame.image.load(os.path.join("assets", "JanggiOrange.svg"))
    screen.blit(bgd_image, (45, 50))

    # blit each column header here
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
    letter_images = get_string_images(letters)
    x_coord = 33 + 45
    y_coord = 25
    for img in letter_images.values():
        rect = img.get_rect()
        rect.center = (x_coord, y_coord)
        screen.blit(img, rect.topleft)
        x_coord += 66

    # blit each row number along left side here
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    number_images = get_string_images(numbers)
    x_coord = 25
    y_coord = 33 + 45
    for img in number_images.values():
        rect = img.get_rect()
        rect.center = (x_coord, y_coord)
        screen.blit(img, rect.topleft)
        y_coord += 66

    # blit each row number along right side here
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    number_images = get_string_images(numbers)
    x_coord = 684 - 25
    y_coord = 33 + 45
    for img in number_images.values():
        rect = img.get_rect()
        rect.center = (x_coord, y_coord)
        screen.blit(img, rect.topleft)
        y_coord += 66

    # blit each game piece image here!!!!
    pixel_dict = get_pixel_coordinates()
    board = game.get_board()
    for row in board:
        for piece_obj in row:
            if piece_obj is not None:
                # get the piece's position, image and associated rectangle
                pos = piece_obj.get_position()
                image = piece_obj.get_image()
                rect = image.get_rect()
                # set rectangle center to pixel position
                rect.center = pixel_dict[pos]
                # blit image to screen using rectangle's top left coordinate
                screen.blit(image, rect.topleft)

    # draw a colored circle to indicate turn
    if game.get_turn() == "b":
        color = "blue"
    else:
        color = "red"
    pygame.draw.circle(screen, color, (342, 731), 10)

    # refresh display
    pygame.display.flip()


def blit_ending_message(game, screen):
    """
    helper function takes the current instance of the JanggiGame class
    and the current pygame screen, then blits a rectangle declaring
    the winner to the center of the screen
    """
    # draw a grey rectangle in the center of the screen
    cx, cy = 342, 380
    my_rect = pygame.Rect(0, 0, 400, 200)
    my_rect.center = cx, cy
    pygame.draw.rect(screen, "grey", my_rect)

    # get winning color
    if game.get_game_state() == "BLUE_WON":
        color = "blue"
    else:
        color = "red"

    # create image for ending message, blit to screen
    font = pygame.font.SysFont("timesnewroman", 30)
    win_str = f"CHECKMATE, {color.upper()} WINS!"
    win_img = font.render(win_str, True, color)
    rect = win_img.get_rect()
    rect.center = cx, cy
    screen.blit(win_img, rect.topleft)

    # refresh display
    pygame.display.flip()


def blit_invalid_move(screen):
    """
    helper function takes the current pygame screen object and blits
    an invalid move message to the bottom corner
    """
    # create image for ending message, blit to screen
    font = pygame.font.SysFont("timesnewroman", 20)
    invalid_str = "Invalid move, try again!"
    black = 0, 0, 0
    invalid_img = font.render(invalid_str, True, black)
    rect = invalid_img.get_rect()
    rect.center = 145, 731
    screen.blit(invalid_img, rect.topleft)
    # refresh display
    pygame.display.flip()


def perform_set_of_moves(game):
    game.make_move('e7', 'e6')
    game.make_move('e2', 'e2')
    game.make_move('e6', 'e5')
    game.make_move('e2', 'e2')
    game.make_move('e5', 'e4')
    game.make_move('e2', 'e2')
    game.make_move('e4', 'd4')
    game.make_move('e2', 'e2')
    game.make_move('d4', 'c4')
    game.make_move('e2', 'e2')
    game.make_move('a10', 'a9')
    game.make_move('e2', 'e2')
    game.make_move('a9', 'd9')
    game.make_move('e2', 'e2')
    game.make_move('d9', 'd8')
    game.make_move('e2', 'e2')
    game.make_move('d8', 'd7')
    game.make_move('e2', 'e2')
    game.make_move('d7', 'd6')
    game.make_move('i1', 'i2')
    game.make_move('e9', 'e9')
    game.make_move('i2', 'g2')
    game.make_move('e9', 'e9')
    game.make_move('i4', 'h4')
    game.make_move('e9', 'e9')
    game.make_move('h3', 'h5')
    game.make_move('i10', 'i9')
    game.make_move('e2', 'e2')
    game.make_move('i9', 'g9')
    game.make_move('e2', 'e2')
    game.make_move('g9', 'g8')
    game.make_move('e2', 'e2')
    game.make_move('h8', 'f8')
    game.make_move('f1', 'e1')
    game.make_move('g7', 'f7')
    game.make_move('e2', 'e2')
    game.make_move('i7', 'i6')
    game.make_move('e2', 'e2')
    game.make_move('g10', 'i7')
    game.make_move('e2', 'e2')
    game.make_move('i7', 'f5')
    game.make_move('e2', 'e2')
    game.make_move('f5', 'd8')
    game.make_move('e2', 'e2')
    game.make_move('d8', 'b5')
    game.make_move('e2', 'e2')
    game.make_move('c4', 'd4')
    game.make_move('e2', 'e2')
    game.make_move('d4', 'e4')
    game.make_move('e2', 'e2')
    # game.make_move('e4', 'e3')  # checkmate


def main():
    # create a Janggi Game instance
    game = JanggiGame()

    # if desired, perform a predetermined set of moves here
    # perform_set_of_moves(game)

    # initialize pygame module
    pygame.init()
    # set caption
    pygame.display.set_caption("Janggi")
    # create a surface called screen that is 684 x 760
    screen = pygame.display.set_mode((684, 760))

    # blit the current game pieces
    blit_current_board(game, screen)

    # create a dictionary of coordinates/rectangles for each game square
    # blit each one to the screen for now to debug
    board_rectangles = get_board_rectangles()
    # FOR DEBUGGING: prints all board rectangles for visualization
    #for alg_coord, my_rect in board_rectangles.items():
    #    pygame.draw.rect(screen, "blue", my_rect)
    #pygame.display.flip()

    # initialize boolean to control main loop
    running = True
    # initialize start and end for click detection, valid_move
    start = None
    end = None
    valid_move = None
    # main loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:   # left mouse button
                    # iterate through every board square's rectangle
                    for alg_coord, my_rect in board_rectangles.items():
                        if my_rect.collidepoint(event.pos):
                            if start is None and end is None:   # if first collision, set start
                                start = alg_coord
                                # DEBUG:
                                # print(f"A starting rectangle was clicked! {start}")
                                # if previous move was invalid, reset screen after first new click
                                if not valid_move:
                                    blit_current_board(game, screen)
                            elif start is not None and end is None:     # if second collision, set end
                                end = alg_coord
                                # DEBUG:
                                # print(f"An ending rectangle was clicked! {end}")
            # make move inside loop
            if start is not None and end is not None:
                # make move and assign the validity
                valid_move = game.make_move(start, end)
                # update display
                blit_current_board(game, screen)
                if not valid_move:
                    # display invalid move prompt
                    blit_invalid_move(screen)
                # reset start and end for next turn, continue loop
                start = None
                end = None
            # if game is finished, display winner and end
            if game.get_game_state() != "UNFINISHED":
                blit_ending_message(game, screen)


if __name__ == "__main__":
    main()
