import math
import random
class Cell:

    def __init__(self, (x, y), index):
        self.index = index
        self.coordinates = (x, y)
        self.visited = False
        self.status = None
        self.gScore = 0
        self.hScore = 0
        self.fScore = float("inf")
        self.value = 1
        self.blocked = False

    def getCoordinates(self):
        return self.coordinates

    def visit(self):
        self.visited = True
