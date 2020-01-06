class Cell:

    def __init__(self, (x, y), (width, height)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visited = False
        self.status = None

    def draw(self, pygame, canvas):
        pygame.draw.polygon(
            canvas,
            (255, 255, 255),
            pygame.Rect(self.x, self.y, self.width, self.height),
            1
        )

    def visit(self):
        self.visited = True
