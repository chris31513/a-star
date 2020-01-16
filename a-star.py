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
        default=30,
    )

    parser.add_argument(
        '-gh', '--gridHeight',
        help='grid heigth',
        type=int,
        default=20,
    )

    parser.add_argument(
        '-cw', '--cellWidth',
        help='cells width',
        type=int,
        default=50,
    )

    parser.add_argument(
        '-ch', '--cellHeight',
        help='cells height',
        type=int,
        default=50,
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

    canvasWidth = (args.gridWidth * args.cellWidth) + extraWidth
    canvasHeigth = (args.gridHeight * args.cellHeight) + extraHeight
    canvasDimensions = (canvasWidth, canvasHeigth)
    canvasOffset = (extraWidth / 2, extraHeight / 2)

    # Generate grid
    gridDimensions = (args.gridWidth, args.gridHeight)
    cellDimensions = (args.cellWidth, args.cellHeight)
    grid = Grid.Grid(gridDimensions, cellDimensions, canvasOffset)

    # Pygame setup
    pygame.init()
    pygame.font.init()

    font = pygame.font.SysFont(None, 20)
    canvas = pygame.display.set_mode(canvasDimensions)
    pygame.display.set_caption('A* Pathfinding')

    sketcher = Sketcher.Sketcher(pygame, canvas, font)

    sketcher.drawGrid(grid)

    startCell = grid.getStart()
    goalCell = grid.getGoal()

    # Set of discovered cells, initially with start
    openSet = []
    heapq.heappush(openSet, (0, startCell))

    closedSet = [[False for _ in range(args.gridWidth)] for _ in range(args.gridHeight)]

    start = False
    done = False
    state = (openSet, closedSet, done)

    while not start:
        ev = pygame.event.get()

        for event in ev:
            if event.type == pygame.QUIT:
                pygame.quit()
            if pygame.mouse.get_pressed()[0]:
                try:
                    pos = pygame.mouse.get_pos()
                    cell = grid.mousePress(pos)
                    sketcher.updateCell(cell)
                except AttributeError:
                    pass
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = True
                    break

    while not done:
        (_, _, done) = aStar(grid, state, sketcher)

    createPath(grid, sketcher, grid.getGoal())

def aStar(grid, (openSet, closedSet, done), sketcher):

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
                neighbour.parent = cell
                return (None, None, True)

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
                    neighbour.parent = cell

        closedSet[x][y] = True
        cell.setBGColor((215, 61, 124))
        sketcher.updateCell(cell)

    return (openSet, closedSet, False)

def createPath(grid, sketcher, goalCell):
    goalCell.setBGColor((98, 117, 200))
    sketcher.updateCell(goalCell)

    parent = goalCell.parent
    while parent != None:
        parent.setBGColor((98, 117, 200))
        sketcher.updateCell(parent)

        parent = parent.parent

main(defineArgs())
