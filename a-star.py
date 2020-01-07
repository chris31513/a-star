import grid
import argparse
import pygame
import random

def defineArgs():
    parser = argparse.ArgumentParser(
        description='simple script to find an optimal path using A*'
    )

    parser.add_argument(
        '-gw', '--gridWidth',
        help='grid width',
        type=int,
        default=50,
    )

    parser.add_argument(
        '-gh', '--gridHeight',
        help='grid heigth',
        type=int,
        default=50,
    )

    parser.add_argument(
        '-cw', '--cellWidth',
        help='cells width',
        type=int,
        default=20,
    )

    parser.add_argument(
        '-ch', '--cellHeight',
        help='cells height',
        type=int,
        default=20,
    )

    return parser.parse_args()

def main(args):

    # Get canvas dimensions based on cells width and heigth
    canvasWidth = args.gridWidth * args.cellWidth + 30
    canvasHeigth = args.gridHeight * args.cellHeight + 10
    canvasDimensions = (canvasWidth, canvasHeigth)

    # Generate grid
    gridDimensions = (args.gridWidth, args.gridHeight)
    cellDimensions = (args.cellWidth, args.cellHeight)
    genGrid = grid.Grid(gridDimensions, cellDimensions)

    # Pygame setup
    pygame.init()
    canvas = pygame.display.set_mode(canvasDimensions)
    pygame.display.set_caption('A* Pathfinding')

    done = False

    genGrid.draw(pygame, canvas)
    pygame.display.update()

    while not done:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            done = True
            pygame.quit()

main(defineArgs())
