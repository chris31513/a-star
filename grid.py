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
        self.goal = self.cells[gridHeight - 1][gridWidth - 1]

        self.start.setBGColor((98, 117, 200))
        self.start.showText = False

        self.goal.setBGColor((98, 117, 200))
        self.goal.showText = False

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

    def setGoal(self, (x, y)):
        (width, height) = self.gridDimensions
        if (0 <= x <= width) and (0 <= y <= height):
            goal = self.cells[x][y]
            if goal != self.start:
                self.goal = goal

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

        # n1, n2, n3, n4, n5, n6, n7, n8 = None, None, None, None, None, None, None, None
        #
        #
        # if x - 1 >= 0:
        #     n4 = self.cells[x - 1][y]
        #     neighbours.append(n4)
        #     if y - 1 >= 0:
        #         n2 = self.cells[x][y - 1]
        #         neighbours.append(n2)
        #         if (not n4.isBlocked()) and (not n2.isBlocked()):
        #             n1 = self.cells[x - 1][y - 1]
        #             neighbours.append(n1)
        #     if y + 1 < height:
        #         if (not n4.isBlocked()) and (not n7.isBlocked()):
        #             n6 = self.cells[x - 1][y + 1]
        #             neighbours.append(n6)
        # if x + 1 < width:
        #     n5 = self.cells[x + 1][y]
        #     neighbours.append(n5)
        #     if y + 1 < height:
        #         n7 = self.cells[x][y + 1]
        #         neighbours.append(n7)
        #         if (not n5.isBlocked()) and (not n7.isBlocked()):
        #             n8 = self.cells[x + 1][y + 1]
        #             neighbours.append(n8)
        #     if y - 1 >= 0:
        #         if (not n2.isBlocked()) and (not n5.isBlocked()):
        #             n3 = self.cells[x + 1][y - 1]
        #             neighbours.append(n3)

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
