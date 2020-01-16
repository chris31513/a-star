class Sketcher:

    def __init__(self, pygame, canvas, font):
        self.pygame = pygame
        self.canvas = canvas
        self.font = font

    def drawGrid(self, grid):
        (w, h) = grid.cellDimensions

        for row in grid.cells:
            for cell in row:
                # Creating actual cell
                (x, y) = cell.getCoordinates()
                rect = self.pygame.Rect(x, y, w, h)

                # Drawing cell
                self.pygame.draw.rect(self.canvas, (255, 255, 255), rect, 4)

        self.updateCell(grid.getStart())
        self.updateCell(grid.getGoal())

    def updateCell(self, cell):
        (x, y) = cell.getCoordinates()
        (w, h) = cell.getDimensions()

        # Coloring cell
        self.pygame.draw.polygon(
            self.canvas,
            cell.getBGColor(),
            [(x + 2, y + 2), (x + w - 3, y + 2),
            (x + w - 2, y + h - 3), (x + 3, y + h - 3)]
        )

        textG = str(int(cell.getGScore()))
        textH = str(int(cell.getHScore()))
        textF = None
        if cell.getFScore() == float("inf"):
            textF = "inf"
        else:
            textF = str(int(cell.getFScore()))

        txtColor = cell.getTxtColor()

        textsurface = self.font.render(textG, False, txtColor)
        self.canvas.blit(textsurface,(x + 5, y))

        textsurface = self.font.render(textH, False, txtColor)
        self.canvas.blit(textsurface,(x + w - 10, y))

        textsurface = self.font.render(textF, False, txtColor)
        self.canvas.blit(textsurface,(x + w / 2 - 3, y + h / 2))

        self.pygame.display.update()
