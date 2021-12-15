#! /usr/bin/python3

"""
game of life application (uses GOL class)

J. Knerr
Nov 2021
"""

import time
from os import environ
import click
import pygame
from pygame.locals import (KEYDOWN, K_ESCAPE, K_q)
import gol
# stop the "welcome to pygame" message from being displayed
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


@click.command()
@click.option("--res", default=5, help="grid resolution")
@click.option("--nts", default=10, help="number of time steps")
@click.option("--term", is_flag=True, default=False,
              help="display game to terminal")
@click.option("--pyg", is_flag=True, default=False,
              help="display game to pygame graphics")
def main(res, nts, term, pyg):
    """make a game object, play the game"""
    rows = res
    cols = res
    game = gol.GOL(rows, cols)
    timestep = 0
    tstart = time.time()
    game.initialconditions("random")
#   game.initialconditions("oscillator")
#   game.initialconditions("glider")
    if pyg:
        pygame.init()
        pgdisplay = pygame.display.set_mode((rows, cols))
    display(game, term, timestep)
    running = True
    while running:
        if pyg:
            for event in pygame.event.get():
                if event.type == KEYDOWN and \
                  (event.key == K_ESCAPE or event.key == K_q):
                    running = False
                if event.type == pygame.QUIT:
                    running = False
        game.step()
        timestep += 1
        display(game, term, timestep)
        if timestep >= nts:
            running = False
        if pyg:
            # change values so colors can be seen in pygame
            new = game.grid*255
            pygame.surfarray.blit_array(pgdisplay, new)
            pygame.display.flip()
    tfinish = time.time()
    endstats(game, timestep, tfinish - tstart)
    if pyg:
        pygame.quit()


def display(game, term, timestep):
    """show how the game is progressing"""
    print(timestep)
    if term:
        RED = u"\033[1;31m"
        BLUE = u"\033[1;34m"
        RESET = u"\033[0;0m"
        CIRCLE = u"\u25CF"

        RED_DISK = RED + CIRCLE + RESET
        BLUE_DISK = BLUE + CIRCLE + RESET
        for i in range(game.getRows()):
            line = ""
            for j in range(game.getCols()):
                if game.cell_is_alive(i, j):
                    line += BLUE_DISK
                else:
                    line += RED_DISK
            print(line)
    else:
        print(game)


def endstats(game, timestep, totaltime):
    """show stats at the end"""
    rows = game.getRows()
    cols = game.getCols()
    print("resolution: %d x %d" % (rows, cols))
    print(" timesteps: %d" % (timestep))
    print("      time: %.2f sec" % (totaltime))
    print("     alive: %3d" % (game.alive()))
    print("      dead: %3d" % (game.dead()))


if __name__ == '__main__':
    main()
