import graph
import cell
import random

class Grid:

    def __init__(self, (gridWidth, gridHeight), (cellWidth, cellHeight)):
        self.gridDimensions = (gridWidth, gridHeight)
        self.cellDimensions = (cellWidth, cellHeight)
        self.cells = [[_ for _ in range(gridWidth)] for _ in range(gridHeight)]
        self.cellsVisited = 0

        for row in range(gridHeight):
            for col in range(gridWidth):
                coordinates = (cellWidth * col, cellHeight * row)
                self.cells[row][col] = cell.Cell(coordinates, self.cellDimensions)

    def getDimensions(self):
        return self.gridDimensions
        
    def hasUnvisitedCells(self):
        return self.cellsVisited < self.width() * self.height()

    def draw(self, pygame, canvas):
        for row in self.cells:
            for cell in row:
                # Creating actual cell
                (x, y) = cell.getCoordinates()
                (w, h) = cell.getDimensions()
                rect = pygame.Rect(x, y, w, h)

                # Draw cell
                pygame.draw.rect(canvas, (255, 255, 255), rect, 1)
