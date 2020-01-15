import grid
import argparse
import pygame
import random
import math
# from que import PriorityQueue
import heapq

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
        default=60,
    )

    parser.add_argument(
        '-ch', '--cellHeight',
        help='cells height',
        type=int,
        default=60,
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
    genGrid = grid.Grid(gridDimensions, cellDimensions, canvasOffset)

    # Pygame setup
    pygame.init()
    pygame.font.init() # you have to call this at the start,
                   # if you want to use this module.
    myfont = pygame.font.SysFont('Comic Sans MS', 20)
    canvas = pygame.display.set_mode(canvasDimensions)
    pygame.display.set_caption('A* Pathfinding')

    # Specifies when the program should finish
    done = False

    genGrid.draw(pygame, canvas)
    pygame.display.update()

    startCell = genGrid.getStart()
    goalCell = genGrid.getGoal()

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
            state = aStar(genGrid, state, pygame, canvas, myfont)
        else:
            done = True

def aStar(genGrid, (openSet, closedSet), pygame, canvas, font):

    tmpG = 0
    tmpH = 0
    tmpF = 0
    # While the open set is not empty
    if len(openSet) > 0:

        # Find the cell with the lowest f and pop it off
        (cellFScore, cell) = heapq.heappop(openSet)

        # Get cell neighbours
        cellNeighbours = genGrid.getNeighbours(cell)

        (x, y) = cell.index
        closedSet[x][y] = True

        # For each neighbour
        for neighbour in cellNeighbours:
            # genGrid.color(neighbour, pygame, canvas, (255, 255, 255))
            (nx, ny) = neighbour.index


            # If neighbour is goal, stop search
            if neighbour == genGrid.getGoal():
                genGrid.color(neighbour, pygame, canvas, (255, 0, 0))
                pygame.display.update()
                return

            print(neighbour.index)
            print(closedSet[nx][ny])
            if (not closedSet[nx][ny]) and (not neighbour.blocked):
                # print(neighbour.index)
                tmpG = cell.gScore + neighbour.value
                tmpH = heuristic(neighbour, genGrid.getGoal())

                tmpF = tmpG + tmpH

                if (neighbour.fScore == float("inf")) or (neighbour.fScore > tmpF):
                    heapq.heappush(openSet, (tmpF, neighbour))

                    neighbour.gScore = tmpG
                    neighbour.hScore = tmpH
                    neighbour.fScore = tmpF

                    genGrid.updateCell(neighbour, (0, 255, 0), pygame, canvas, font)
            pygame.display.update()

    return (openSet, closedSet)

main(defineArgs())
