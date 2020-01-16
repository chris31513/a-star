import cell
import random

class Grid:

    def __init__(self, (gridWidth, gridHeight), (cellWidth, cellHeight),
                (xOffset, yOffset)):
        self.gridDimensions = (gridWidth, gridHeight)
        self.cellDimensions = (cellWidth, cellHeight)
        self.cells = [[_ for _ in range(gridWidth)] for _ in range(gridHeight)]

        for r in range(gridHeight):
            for c in range(gridWidth):
                # Get cell coordinates
                x = xOffset + (cellWidth * c)
                y = yOffset + (cellHeight * r)

                coordinates = (x, y)
                index = (r, c)

                self.cells[r][c] = cell.Cell(coordinates, self.cellDimensions, index)

        self.start = self.cells[0][0]
        self.goal = self.cells[gridWidth - 1][gridHeight - 1]

        self.start.setBGColor((98, 117, 200))
        self.goal.setBGColor((98, 117, 200))

    def getDimensions(self):
        return self.gridDimensions

    def getStart(self):
        return self.start

    def getGoal(self):
        return self.goal

    def setStart(self, (x, y)):
        (width, height) = self.gridDimensions
        if (0 <= x <= width) and (0 <= y <= height):
            start = self.cells[x][y]
            if start != self.goal:
                self.start = start

    def setStart(self, (x, y)):
        (width, height) = self.gridDimensions
        if (0 <= x <= width) and (0 <= y <= height):
            goal = self.cells[x][y]
            if goal != self.start:
                self.goal = goal

    def getNeighbours(self, cell):
        (x, y) = cell.getIndex()
        (width, height) = self.gridDimensions

        neighbours = []          # | (x - 1, y - 1) | (x, y - 1) | (x + 1, y - 1) |
                                 # | (x - 1,   y  ) | (x,   y  ) | (x + 1,   y  ) |
        if x - 1 >= 0:           # | (x - 1, y + 1) | (x, y + 1) | (x + 1, y + 1) |
            neighbours.append(self.cells[x - 1][y])
            if y - 1 >= 0:
                neighbours.append(self.cells[x][y - 1])
                neighbours.append(self.cells[x - 1][y - 1])
            if y + 1 < height:
                neighbours.append(self.cells[x - 1][y + 1])
        if x + 1 < width:
            neighbours.append(self.cells[x + 1][y])
            if y + 1 < height:
                neighbours.append(self.cells[x][y + 1])
                neighbours.append(self.cells[x + 1][y + 1])
            if y - 1 >= 0:
                neighbours.append(self.cells[x + 1][y - 1])

        return neighbours
