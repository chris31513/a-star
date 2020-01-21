import math
import random
class Cell:

    def __init__(self, x_y, w_h, index):
        x, y = x_y
        w, h = w_h
        self.coordinates = (x, y)
        self.dimensions = (w, h)
        self.index = index
        self.gScore = 0
        self.hScore = 0
        self.fScore = float("inf")
        self.value = 1
        self.blocked = False
        self.bgColor = (0, 0, 0)
        self.txtColor = (255, 255, 255)
        self.showText = True
        self.parent = None
        self.isStart = False
        self.isGoal = False

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

    def updateBlockedState(self):
        if self.blocked:
            self.bgColor = (255, 255, 255)
            self.showText = False
        else:
            self.bgColor = (0, 0, 0)
            self.showText = True
