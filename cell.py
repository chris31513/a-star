import math
import random
class Cell:

    def __init__(self, (x, y), (w, h), index):
        self.coordinates = (x, y)
        self.dimensions = (w, h)
        self.index = index
        self.gScore = 0
        self.hScore = 0
        self.fScore = float("inf")
        self.value = 1
        self.blocked = False
        self.bgColor = None
        self.txtColor = (0, 0, 0)

    def getCoordinates(self):
        return self.coordinates

    def getDimensions(self):
        return self.dimensions

    def getIndex(self):
        return self.index

    def getGScore(self):
        return self.gScore

    def getHScore(self):
        return self.hScore

    def getFScore(self):
        return self.fScore

    def getValue(self):
        return self.value

    def isBlocked(self):
        return self.blocked

    def getBGColor(self):
        return self.bgColor

    def setBGColor(self, bgColor):
        self.bgColor = bgColor

    def getTxtColor(self):
        return self.txtColor

    def setTxtColor(self, txtColor):
        self.txtColor = txtColor
