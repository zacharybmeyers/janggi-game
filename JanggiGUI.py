# Author:       Zachary Meyers
# Date:         2021-03-23
# Description:

import pygame
import os


def main():
    # initialize pygame module
    pygame.init()

    # set caption
    pygame.display.set_caption("first blit")

    # create a surface on screen that is 240 x 180
    screen = pygame.display.set_mode((675, 750))

    # load a background board image, scale to board size, blit to screen
    bgd_image = pygame.image.load(os.path.join("assets", "JanggiWood.svg"))
    screen.blit(bgd_image, (0, 0))

    # load a game piece image, blit to screen
    general_image = pygame.image.load(os.path.join("assets", "blue_general.svg"))
    screen.blit(general_image, (300, 75))

    # refresh screen
    pygame.display.flip()

    # initialize boolean to control main loop
    running = True

    # main loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


if __name__ == "__main__":
    main()
