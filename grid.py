import cell
import random

class Grid:

    def __init__(self, (gridWidth, gridHeight), (cellWidth, cellHeight),
                (xOffset, yOffset)):
        self.gridDimensions = (gridWidth, gridHeight)
        self.cellDimensions = (cellWidth, cellHeight)
        self.cells = [[_ for _ in range(gridWidth)] for _ in range(gridHeight)]
        self.start = None
        self.goal = None

        for r in range(gridHeight):
            for c in range(gridWidth):
                # Get cell coordinates
                x = xOffset + (cellWidth * c)
                y = yOffset + (cellHeight * r)

                coordinates = (x, y)
                index = (r, c)

                self.cells[r][c] = cell.Cell(coordinates, self.cellDimensions, index)

    def getDimensions(self):
        return self.gridDimensions

    def getStart(self):
        return self.start

    def getGoal(self):
        return self.goal

    def setStart(self, (x, y)):
        (width, height) = self.gridDimensions
        # if (0 <= x <= width) and (0 <= y <= height):
        start = self.cells[x][y]
        if start != self.goal:
            self.start = start
            self.start.setBGColor((98, 117, 200))
            self.start.showText = False
            self.start.isStart = True

    def setGoal(self, (x, y)):
        (width, height) = self.gridDimensions
        # if (0 <= x <= width) and (0 <= y <= height):
        goal = self.cells[x][y]
        if goal != self.start:
            self.goal = goal
            self.goal.setBGColor((98, 117, 200))
            self.goal.showText = False
            self.goal.isGoal = True

    def getNeighbours(self, cell):
        (x, y) = cell.getIndex()
        (height, width) = self.gridDimensions

        neighbours = []         # | (x - 1, y - 1) | (x, y - 1) | (x + 1, y - 1) |
                                # | (x - 1,   y  ) | (x,   y  ) | (x + 1,   y  ) |
                                # | (x - 1, y + 1) | (x, y + 1) | (x + 1, y + 1) |

                                # |      n1        |     n2     |       n3       |
                                # |      n4        |     n-     |       n5       |
                                # |      n6        |     n7     |       n8       |
        if x - 1 >= 0:
            neighbours.append(self.cells[x - 1][y])
            if y - 1 >= 0:
                neighbours.append(self.cells[x][y - 1])
                if (not self.cells[x - 1][y].isBlocked()) and (not self.cells[x][y - 1].isBlocked()):
                    neighbours.append(self.cells[x - 1][y - 1])
            if y + 1 < height:
                if (not self.cells[x - 1][y].isBlocked()) and (not self.cells[x][y + 1].isBlocked()):
                    neighbours.append(self.cells[x - 1][y + 1])
        if x + 1 < width:
            neighbours.append(self.cells[x + 1][y])
            if y + 1 < height:
                neighbours.append(self.cells[x][y + 1])
                if (not self.cells[x + 1][y].isBlocked()) and (not self.cells[x][y + 1].isBlocked()):
                    neighbours.append(self.cells[x + 1][y + 1])
            if y - 1 >= 0:
                if (not self.cells[x][y - 1].isBlocked()) and (not self.cells[x + 1][y].isBlocked()):
                    neighbours.append(self.cells[x + 1][y - 1])

        return neighbours

    def mousePress(self, position):
        (gridWidth, gridHeight) = self.gridDimensions
        (cellWidth, cellHeight) = self.cellDimensions

        y = position[0]
        x = position[1]

        row = x // ((gridWidth * cellWidth) // gridWidth)
        col = y // ((gridHeight * cellHeight) // gridHeight)
        cell = self.cells[row][col]

        if cell != self.start and cell != self.goal:
            cell.blocked = True

        cell.setBGColor((255, 255, 255))
        cell.showText = False
        return cell

    def setStartOrGoal(self, position):
        (gridWidth, gridHeight) = self.gridDimensions
        (cellWidth, cellHeight) = self.cellDimensions

        y = position[0]
        x = position[1]

        row = x // ((gridWidth * cellWidth) // gridWidth)
        col = y // ((gridHeight * cellHeight) // gridHeight)

        if self.start == None:
            self.start = self.cells[row][col]
            self.start.setBGColor((98, 117, 200))
            self.start.showText = False
            return self.start
        elif self.goal == None:
            self.goal = self.cells[row][col]
            self.goal.setBGColor((98, 117, 200))
            self.goal.showText = False
            return self.goal

    def toFile(self, fileName):
        file = open(fileName, 'w')
        file.write('A-STAR\n')

        (gw, gh) = self.gridDimensions
        (cw, ch) = self.cellDimensions
        file.write('GW {}\nGH {}\nCW {}\nCH {}\n'.format(gw, gh, cw, ch))

        startCell = self.start
        goalCell = self.goal
        file.write('S {}\n'.format(startCell.getIndex()))
        file.write('G {}\n'.format(goalCell.getIndex()))

        file.write('B')
        for row in self.cells:
            for cell in row:

                if cell.isBlocked():
                    file.write(' {}'.format(cell.getIndex()))

        file.close()

    def blockCell(self, (x, y)):
        cell = self.cells[x][y]

        if cell != self.start and cell != self.goal:
            cell.blocked = True

        cell.setBGColor((255, 255, 255))
        cell.showText = False
