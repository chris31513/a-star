import cell
import random

class Grid:

    def __init__(self, (gridWidth, gridHeight), (cellWidth, cellHeight),
                (xOffset, yOffset)):
        self.gridDimensions = (gridWidth, gridHeight)
        self.cellDimensions = (cellWidth, cellHeight)
        self.cells = [[_ for _ in range(gridWidth)] for _ in range(gridHeight)]
        self.cellsVisited = 0

        for row in range(gridHeight):
            for col in range(gridWidth):
                # Get cell coordinates
                x = xOffset + cellWidth * col
                y = yOffset + cellHeight * row
                coordinates = (x, y)
                self.cells[row][col] = cell.Cell(coordinates, (row, col))

        self.start = self.cells[0][0]
        self.goal = self.cells[gridWidth - 1][gridHeight - 1]

    def getDimensions(self):
        return self.gridDimensions

    def hasUnvisitedCells(self):
        (w, h) = self.gridDimensions
        return self.cellsVisited < w * h

    def draw(self, pygame, canvas):
        for row in self.cells:
            for cell in row:
                # Creating actual cell
                (x, y) = cell.getCoordinates()
                (w, h) = self.cellDimensions
                rect = pygame.Rect(x, y, w, h)

                # Drawing cell
                pygame.draw.rect(canvas, (255, 255, 255), rect, 1)

        self.color(self.start, pygame, canvas, (255, 255, 255))
        self.color(self.goal, pygame, canvas, (0, 0, 255))

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
        (x, y) = cell.index
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

    def color(self, cell, pygame, canvas, color):
        (x, y) = cell.getCoordinates()
        (w, h) = self.cellDimensions

        # Coloring cell
        pygame.draw.polygon(
            canvas,
            color,
            [(x, y), (x + w, y),
            (x + w, y + h), (x, y + h)]
        )

    def updateCell(self, cell, color, pygame, canvas, font):
        (x, y) = cell.getCoordinates()
        (w, h) = self.cellDimensions

        # Coloring cell
        pygame.draw.polygon(
            canvas,
            color,
            [(x, y), (x + w, y),
            (x + w, y + h), (x, y + h)]
        )

        textg = "G:{}".format(int(cell.gScore))
        texth = "H:{}".format(int(cell.hScore))
        textf = "F:{}".format(int(cell.fScore))

        textsurface = font.render(textg, False, (255, 255, 255))
        canvas.blit(textsurface,(x,y))

        textsurface = font.render(texth, False, (255, 255, 255))
        canvas.blit(textsurface,(x,y + 15))

        textsurface = font.render(textf, False, (255, 255, 255))
        canvas.blit(textsurface,(x,y + 30))
