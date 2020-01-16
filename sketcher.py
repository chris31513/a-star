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

        self.pygame.display.update()

    def updateCell(self, cell):
        (x, y) = cell.getCoordinates()
        (cW, cH) = cell.getDimensions()

        # Coloring cell
        self.pygame.draw.polygon(
            self.canvas,
            cell.getBGColor(),
            [(x + 2, y + 2), (x + cW - 3, y + 2),
            (x + cW - 2, y + cH - 3), (x + 3, y + cH - 3)]
        )

        if cell.showText:                                   # # # # # # # # # # # # # # #
            gScore = int(cell.getGScore())                  #                           #
            hScore = int(cell.getHScore())                  #  TTTT           T    T    #
            fScore = gScore + hScore                        #  T              T    T    #
                                                            #  T TTT          TTTTTT    #
            textG = str(gScore)                             #  T  TT          T    T    #
            textH = str(hScore)                             #  TTTTT          T    T    #
            textF = str(fScore)                             #                           #
                                                            #         TTTTTT            #
            txtColor = cell.getTxtColor()                   #         T                 #
                                                            #         TTT               #
            (fW, fH) = self.font.size(textF)                #         T                 #
                                                            # # # # # # # # # # # # # # #
            textsurface = self.font.render(textG, False, txtColor)
            self.canvas.blit(textsurface,(x + 5, y + 2 + fH * .15))

            (fW, fH) = self.font.size(textH)

            textsurface = self.font.render(textH, False, txtColor)
            self.canvas.blit(textsurface,(x + cW - fW - (fW * .50), y + 2 + (fH * .15)))

            (fW, fH) = self.font.size(textF)

            textsurface = self.font.render(textF, False, txtColor)
            self.canvas.blit(textsurface,(x + cW / 2 - fW / 2, y + cH / 2 - fH / 2))

        self.pygame.display.update()
