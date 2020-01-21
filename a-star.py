import argparse
import pygame
import random
import math
import heapq
import grid as Grid
import sketcher as Sketcher
import re

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

    parser.add_argument(
        '-o', '--output',
        help='output file',
        type=str,
        default='o.star',
    )

    parser.add_argument(
        '-f', '--fromF',
        help='output file',
        type=str,
    )

    return parser.parse_args()

def heuristic(currentCell, goalCell):
    (cx, cy) = currentCell.index
    (gx, gy) = goalCell.index
    return math.sqrt((gx - cx)**2 + (gy - cy)**2)

def main(args):

    # Get canvas dimensions based on cells width and heigth
    properties = getProperties(args)

    gridDim = properties['gridDim']
    cellDim = properties['cellDim']
    canvasOff = properties['canvasOff']
    grid = Grid.Grid(gridDim, cellDim, canvasOff)

    if args.fromF is not None:
        grid.setStart(properties['startIndex'])
        grid.setGoal(properties['goalIndex'])

        for coordinates in properties['blockedCells']:
            grid.blockCell(coordinates)

    # Pygame setup
    pygame.init()
    pygame.font.init()

    font = pygame.font.SysFont(None, 20)
    canvasDim = properties['canvasDim']
    canvas = pygame.display.set_mode(canvasDim)
    pygame.display.set_caption('A* Pathfinding')

    sketcher = Sketcher.Sketcher(pygame, canvas, font)
    sketcher.drawGrid(grid)

    start = args.fromF is not None
    setStartOrGoal = False
    while not start:
        ev = pygame.event.get()

        for event in ev:
            if event.type == pygame.QUIT:
                pygame.quit()
            if pygame.mouse.get_pressed()[0] and not setStartOrGoal:
                try:
                    pos = pygame.mouse.get_pos()
                    cell = grid.mousePress(pos)
                    sketcher.updateCell(cell)
                except AttributeError:
                    pass
            elif pygame.mouse.get_pressed()[0]:
                try:
                    pos = pygame.mouse.get_pos()
                    cell = grid.setStartOrGoal(pos)
                    sketcher.updateCell(cell)
                except AttributeError:
                    pass
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = True
                    break
                elif event.key == pygame.K_s:
                    setStartOrGoal = not setStartOrGoal

    startCell = grid.getStart()
    goalCell = grid.getGoal()

    # Set of discovered cells, initially with start
    openSet = []
    heapq.heappush(openSet, (0, startCell))

    closedSet = [[False for _ in range(args.gridWidth)] for _ in range(args.gridHeight)]

    done = False
    state = (openSet, closedSet, done)


    while not done:
        (_, _, done) = aStar(grid, state, sketcher)

    createPath(grid, sketcher)

    grid.toFile(args.output)

def aStar(grid, openSet_closedSet_done, sketcher):

    tmpG = 0
    tmpH = 0
    tmpF = 0
    # While the open set is not empty
    if len(openSet) > 0:

        # Find the cell with the lowest f and pop it off
        (cellFScore, cell) = heapq.heappop(openSet)

        # Get cell neighbours
        cellNeighbours = grid.getNeighbours(cell)

        # For each neighbour
        for neighbour in cellNeighbours:
            (nx, ny) = neighbour.getIndex()

            # If neighbour is goal, stop search
            if neighbour == grid.getGoal():
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

        (x, y) = cell.getIndex()
        closedSet[x][y] = True

        cell.setBGColor((215, 61, 124))
        sketcher.updateCell(cell)

    return (openSet, closedSet, False)

def createPath(grid, sketcher):
    startCell = grid.getStart()
    goalCell = grid.getGoal()

    startCell.setBGColor((98, 117, 200))
    startCell.showText = True
    sketcher.updateCell(goalCell)

    goalCell.setBGColor((98, 117, 200))
    goalCell.showText = True
    sketcher.updateCell(goalCell)

    parent = goalCell.parent
    while parent != None:
        parent.setBGColor((98, 117, 200))
        sketcher.updateCell(parent)

        parent = parent.parent

def getProperties(args):

    extraWidth = 20
    extraHeight = 20
    canvasOff = (extraWidth / 2, extraHeight / 2)

    properties = {'canvasOff' : canvasOff}

    if args.fromF:
        file = open(args.fromF, "r")
        try:
            checkNGet(re.compile('A-STAR'), file, None)

            gW = int(checkNGet(re.compile('GW \d+'), file, (3, None)))
            gH = int(checkNGet(re.compile('GH \d+'), file, (3, None)))
            cW = int(checkNGet(re.compile('CW \d+'), file, (3, None)))
            cH = int(checkNGet(re.compile('CH \d+'), file, (3, None)))

            gridDim = (gW, gH)
            properties['gridDim'] = gridDim

            cellDim = (cW, cH)
            properties['cellDim'] = cellDim

            canvasWidth = (gW * cW) + extraWidth
            canvasHeigth = (gH * cH) + extraHeight
            canvasDim = (canvasWidth, canvasHeigth)
            properties['canvasDim'] = canvasDim

            index = checkNGet(re.compile('S \(\d+, \d+\)'), file, (3, -1))
            startIndex = tuple(int(i) for i in index.split(', '))
            properties['startIndex'] = startIndex

            index = checkNGet(re.compile('G \(\d+, \d+\)'), file, (3, -1))
            goalIndex = tuple(int(i) for i in index.split(', '))
            properties['goalIndex'] = goalIndex

            pairs = checkNGet(re.compile('B *'), file, (3, -1)).split(') (')
            blockedCells = []
            for pair in pairs:
                blockedCells.append(tuple(int(i) for i in pair.split(', ')))

            properties['blockedCells'] = blockedCells

            return properties
        except Exception as e:
            print(e)
        finally:
            file.close()
    else:
        canvasWidth = (args.gridWidth * args.cellWidth) + extraWidth
        canvasHeigth = (args.gridHeight * args.cellHeight) + extraHeight
        canvasDim = (canvasWidth, canvasHeigth)

        # Generate grid
        gridDim = (args.gridWidth, args.gridHeight)
        cellDim = (args.cellWidth, args.cellHeight)

        properties['gridDim'] = gridDim
        properties['cellDim'] = cellDim
        properties['canvasDim'] = canvasDim

        return properties

def checkNGet(regex, file, range = None):
    toCheck = file.readline().strip()

    if regex.match(toCheck):
        if range:
            (fromI, toI) = range
            return toCheck[fromI:toI]
        else:
            return
    else:
        raise Exception('Corrupted file in "' + toCheck + '"')

main(defineArgs())
