# Author:       Zachary Meyers
# Date:         2021-03-23
# Description:

import pygame
import os

# initialize pygame module
pygame.init()

# set caption
pygame.display.set_caption("Janggi")

# create a surface on screen that is 675 x 750
screen = pygame.display.set_mode((675, 750))

# load a background board image, blit to screen
bgd_image = pygame.image.load(os.path.join("assets", "JanggiWood.svg"))
screen.blit(bgd_image, (0, 0))

# load a game piece image
general_image = pygame.image.load(os.path.join("assets", "blue_general.svg"))
# get Rectangle
gen_rect = general_image.get_rect()

# load a game piece image
guard_image = pygame.image.load((os.path.join("assets", "blue_guard.svg")))
# get Rectangle
guard_rect = guard_image.get_rect()

# loop to test printing a game piece at every position
y_coord = 38
for i in range(10):
    x_coord = 38
    while x_coord <= 638:
        # set Rectangle center to desired position
        guard_rect.center = (x_coord, y_coord)
        # blit to screen using Rectangle's top left coordinate
        screen.blit(guard_image, guard_rect.topleft)
        # update x
        x_coord += 75
    y_coord += 75

# refresh screen
pygame.display.flip()

# initialize boolean to control main loop
running = True

# main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


def main():
    pass


if __name__ == "__main__":
    main()
