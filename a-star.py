import grid as Grid
import argparse
import pygame
import random
import math
import heapq
import sketcher as Sketcher

def defineArgs():
    parser = argparse.ArgumentParser(
        description='simple script to find an optimal path using A*'
    )

    parser.add_argument(
        '-gw', '--gridWidth',
        help='grid width',
        type=int,
        default=10,
    )

    parser.add_argument(
        '-gh', '--gridHeight',
        help='grid heigth',
        type=int,
        default=10,
    )

    parser.add_argument(
        '-cw', '--cellWidth',
        help='cells width',
        type=int,
        default=70,
    )

    parser.add_argument(
        '-ch', '--cellHeight',
        help='cells height',
        type=int,
        default=70,
    )

    return parser.parse_args()

def heuristic(currentCell, goalCell):
    (cx, cy) = currentCell.index
    (gx, gy) = goalCell.index
    return math.sqrt((gx - cx)**2 + (gy - cy)**2)

def main(args):

    # Get canvas dimensions based on cells width and heigth
    extraWidth = 20
    extraHeight = 20
    canvasWidth = args.gridWidth * args.cellWidth + extraWidth
    canvasHeigth = args.gridHeight * args.cellHeight + extraHeight
    canvasDimensions = (canvasWidth, canvasHeigth)
    canvasOffset = (extraWidth / 2, extraHeight / 2)

    # Generate grid
    gridDimensions = (args.gridWidth, args.gridHeight)
    cellDimensions = (args.cellWidth, args.cellHeight)
    grid = Grid.Grid(gridDimensions, cellDimensions, canvasOffset)

    # Pygame setup
    pygame.init()
    pygame.font.init()

    font = pygame.font.SysFont('Comic Sans MS', 20)
    canvas = pygame.display.set_mode(canvasDimensions)
    pygame.display.set_caption('A* Pathfinding')

    sketcher = Sketcher.Sketcher(pygame, canvas, font)

    # Specifies when the program should finish
    done = False

    sketcher.drawGrid(grid)

    startCell = grid.getStart()
    goalCell = grid.getGoal()

    # Set of discovered cells, initially with start
    openSet = []
    heapq.heappush(openSet, (0, startCell))

    closedSet = [[False for _ in range(args.gridWidth)] for _ in range(args.gridHeight)]

    state = (openSet, closedSet)

    while not done:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            done = True
            pygame.quit()

        if state:
            state = aStar(grid, state, sketcher)
        else:
            done = True

def aStar(grid, (openSet, closedSet), sketcher):

    tmpG = 0
    tmpH = 0
    tmpF = 0
    # While the open set is not empty
    if len(openSet) > 0:

        # Find the cell with the lowest f and pop it off
        (cellFScore, cell) = heapq.heappop(openSet)

        # Get cell neighbours
        cellNeighbours = grid.getNeighbours(cell)

        (x, y) = cell.getIndex()

        # For each neighbour
        for neighbour in cellNeighbours:
            (nx, ny) = neighbour.getIndex()

            # If neighbour is goal, stop search
            if neighbour == grid.getGoal():
                neighbour.setBGColor((255, 0, 0))
                sketcher.updateCell(neighbour)
                return

            if (not closedSet[nx][ny]) and (not neighbour.blocked):
                tmpG = cell.getGScore() + neighbour.getValue()
                tmpH = heuristic(neighbour, grid.getGoal())

                tmpF = tmpG + tmpH

                if (neighbour.fScore == float("inf")) or (neighbour.fScore > tmpF):
                    heapq.heappush(openSet, (tmpF, neighbour))

                    neighbour.gScore = tmpG
                    neighbour.hScore = tmpH
                    neighbour.fScore = tmpF

                    neighbour.setBGColor((0, 255, 0))
                    sketcher.updateCell(neighbour)

        closedSet[x][y] = True
        cell.setBGColor((215, 61, 124))
        sketcher.updateCell(cell)

    return (openSet, closedSet)

main(defineArgs())
