# Author:       Zachary Meyers
# Date:         2021-03-23
# Description:

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
        img = font.render(a_string.upper(), 1, black)
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


def main():
    # create a Janggi Game instance
    game = JanggiGame()
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
    #for alg_coord, my_rect in board_rectangles.items():
    #    pygame.draw.rect(screen, "blue", my_rect)

    # initialize boolean to control main loop
    running = True
    # initialize start and end for click detection
    start = None
    end = None
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
                                print(f"A starting rectangle was clicked! {start}")
                            elif start is not None and end is None:     # if second collision, set end
                                end = alg_coord
                                print(f"An ending rectangle was clicked! {end}")
            # make move inside loop
            if start is not None and end is not None:
                game.make_move(start, end)
                # update display
                blit_current_board(game, screen)
                # reset start and end for next turn, continue loop
                start = None
                end = None


if __name__ == "__main__":
    main()
