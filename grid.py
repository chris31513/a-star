import graph
import cell
import random

class Grid:

    def __init__(self, (width, height), (cellWidth, cellHeight)):
        self.width = width
        self.height = height
        self.cellWidth = cellWidth
        self.cellHeight = cellHeight
        self.cellsGraph = graph.Graph()
        self.cells = [[]]
        self.cells = [[0 for x in range(width)] for y in range(height)]
        self.cellsVisited = 0

        for row in range(0, height):
            for col in range(0, width):
                x = cellWidth * col
                y = cellHeight * row
                newCell = cell.Cell((x, y), (self.cellWidth, self.cellHeight))

                self.cells[row][col]

    def existsUnvisitedCells(self):
        return self.cellsVisited < self.width * self.height

    def draw(self, pygame, canvas):
        for row in range(0, self.height):
            for col in range(0, self.width):
                self.cells[row][col].draw(pygame, canvas)
