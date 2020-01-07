class Cell:

    def __init__(self, (x, y), (width, height)):
        self.coordinates = (x, y)
        self.dimensions = (width, height)
        self.visited = False
        self.status = None

    def getCoordinates(self):
        return self.coordinates

    def getDimensions(self):
        return self.dimensions

    def visit(self):
        self.visited = True
