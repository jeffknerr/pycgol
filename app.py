#! /usr/bin/python3

"""
game of life application (uses GOL class)

J. Knerr
Nov 2021
"""

import click
import gol


@click.command()
@click.option("--res", default=5, help="grid resolution")
@click.option("--nts", default=10, help="number of time steps")
def main(res, nts):
    """make a game object, play the game"""
    rows = res
    cols = res
    game = gol.GOL(rows, cols)
    timestep = 0
#   game.initialconditions("random")
#   game.initialconditions("oscillator")
    game.initialconditions("glider")
    print(game)
    running = True
    while running:
        game.step()
        timestep += 1
        print(timestep)
        print(game)
        if timestep >= nts:
            running = False
    print(game.alive())


if __name__ == '__main__':
    main()
