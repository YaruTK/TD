import pygame

pygame.init()

# colours
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
darkBlue = (0, 0, 128)
white = (255, 255, 255)
black = (0, 0, 0)
pink = (255, 200, 200)

# int
blockSize = 61  # size of a block in grid + 1
perspective = 0.8  # 30% inclination

# str
ver = '0.0.9'

wind_width = 1200
wind_height = 800

fps = pygame.time.Clock()


class object2d(object):
    def __init__(self, x, y, width, height):
        self.level = 0  # level of a layer for future pseudo 3d
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.tlX = self.x
        self.tlY = self.y
        self.trX = self.x + self.width
        self.trY = self.y
        self.blX = self.x
        self.blY = self.y + self.height
        self.brX = self.x + self.width
        self.brY = self.y + self.height
        self.inclined = False
        self.z = 1

    def do_inclination(self, z):  # incline to z. if z = 1 straight, if z = 0 or 2 forms a line
        if (z <= 2) and (z >= 0) and (not self.inclined):
            self.z = z
            self.tlX += int((1 - self.z) * 2 * (wind_width / 2 - self.tlX) * (wind_height / 2 - self.tlY) / wind_height)
            self.trX += int((1 - self.z) * 2 * (wind_width / 2 - self.trX) * (wind_height / 2 - self.trY) / wind_height)
            self.blX += int((1 - self.z) * 2 * (wind_width / 2 - self.blX) * (wind_height / 2 - self.blY) / wind_height)
            self.brX += int((1 - self.z) * 2 * (wind_width / 2 - self.brX) * (wind_height / 2 - self.brY) / wind_height)
            # wind_height/2 is the  horizon line
            if z > 1:
                z = 2 - z
                self.z = z
                #  z = 0.9 and z = 1.1 its the same case
            self.tlY = int(wind_height / 2 - self.z * (wind_height / 2 - self.tlY) + self.level * (1 - self.z))
            self.trY = int(wind_height / 2 - self.z * (wind_height / 2 - self.trY) + self.level * (1 - self.z))
            self.blY = int(wind_height / 2 - self.z * (wind_height / 2 - self.blY) + self.level * (1 - self.z))
            self.brY = int(wind_height / 2 - self.z * (wind_height / 2 - self.brY) + self.level * (1 - self.z))
            if self.z != 1:
                self.inclined = True

    def undo_inclination(self):  # return to initial grid
        if (self.z <= 2) and (self.z >= 0) and self.inclined:
            self.tlX = self.x
            self.tlY = self.y
            self.trX = self.x + self.width
            self.trY = self.y
            self.blX = self.x
            self.blY = self.y + self.height
            self.brX = self.x + self.width
            self.brY = self.y + self.height
            self.z = 1
            self.inclined = False

    def draw(self, clr, window):
        pygame.draw.lines(window, clr, True,
                          [(self.tlX, self.tlY), (self.trX, self.trY), (self.brX, self.brY), (self.blX, self.blY)])


screen = pygame.display.set_mode((wind_width, wind_height))

pygame.display.set_caption("Tower defense v." + ver)

field = object2d(int(0.05 * wind_width), int(0.1 * wind_height), int(0.9 * wind_width), int(0.8 * wind_height))


# def drawGrid(z):
#     for y in range(field.y, field.height, blockSize):
#         for x in range(field.x, field.width, blockSize):
#             cell = object2d(x, y, blockSize - 1, blockSize - 1)
#             for i in range(-5, 5, 1):  # draw 10 layers
#                 cell.level = i * blockSize
#                 cell.undo_inclination()
#                 cell.do_inclination(z)
#                 cell.draw(screen)
#             cell.level = 0
def drawGrid():
    for y in range(field.y, field.height + blockSize - 1, blockSize):
        for x in range(field.x, field.width + blockSize - 1, blockSize):
            cellbot = object2d(x, y, blockSize - 1, blockSize - 1)
            celltop = object2d(x, y, blockSize - 1, blockSize - 1)
            cellbot.level = 0
            celltop.level = 2 * blockSize
            celltop.do_inclination(perspective)
            cellbot.do_inclination(perspective)
            cellbot.draw(white, screen)
            celltop.draw(red, screen)


def redrawGameWindow():
    screen.fill(darkBlue)
    drawGrid()
    pygame.display.update()


# main loop

run = True
a = 0
b = 0
c = 0
while run:
    fps.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    redrawGameWindow()
    # for real game
