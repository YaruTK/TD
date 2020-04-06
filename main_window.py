import pygame
import numpy as np
import image_transformation as it
import cv2

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
blockSize = 127  # size of a block in grid + 1
perspective = 0.87  # 30% inclination

# str
ver = '0.1.7'

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
        pygame.draw.aalines(window, clr, True,
                          [(self.tlX, self.tlY), (self.trX, self.trY), (self.brX, self.brY), (self.blX, self.blY)])


def plot(ar, color, window):
    pygame.draw.aalines(window, color, True, ar)


screen = pygame.display.set_mode((wind_width, wind_height))

pygame.display.set_caption("Tower defense v." + ver)

field = object2d(int(0.08 * wind_width), int(0.03 * wind_height), int(0.83 * wind_width), int(0.81 * wind_height))

grid_height = 1 + int((field.height + 0.5 * blockSize - field.y - 1) / blockSize)
grid_width = 1 + int((field.width + 0.5 * blockSize - field.x - 1) / blockSize)

top_tiles = np.empty((grid_height*grid_width + 1, 4, 2), dtype = "float32")
bot_tiles = np.empty((grid_height*grid_width + 1, 4, 2), dtype = "float32")

plottop = np.zeros((grid_height, grid_width, 4), dtype=tuple)
plotbot = np.zeros((grid_height, grid_width, 4), dtype=tuple)


def til(array, t, a):
    tiles = np.zeros((4, 2), dtype = "float32")
    tiles[0] = (float(a.tlX), float(a.tlY))
    tiles[1] = (float(a.trX), float(a.trY))
    tiles[2] = (float(a.brX), float(a.brY))
    tiles[3] = (float(a.blX), float(a.blY))
    array[t] = tiles


def to_plot(a):
    area = ((a.tlX, a.tlY), (a.trX, a.trY), (a.brX, a.brY), (a.blX, a.blY))
    return area


def calcGrid(f):
    temp = 0
    for i in range(0, grid_height):
        y = f.y + i * blockSize
        for j in range(0, grid_width):
            x = f.x + j * blockSize
            cellbot = object2d(x, y, blockSize - 1, blockSize - 1)
            celltop = object2d(x, y, blockSize - 1, blockSize - 1)
            cellbot.level = 3 * blockSize
            celltop.level = 0
            celltop.do_inclination(perspective)
            cellbot.do_inclination(perspective)

            plottop[i][j] = to_plot(celltop)
            plotbot[i][j] = to_plot(cellbot)

            til(top_tiles, temp, celltop)
            til(bot_tiles, temp, cellbot)

            temp += 1


def drawGrid(layer, colour):
    calcGrid(field)
    for i in range(0, grid_height):
        for j in range(0, grid_width):
            plot(layer[i][j], colour, screen)


def create(array):
    calcGrid(field)
    temp = array
    for i in range(0, grid_width*grid_height):
        erase_0 = min(temp[i][0][0], temp[i][3][0])
        erase_1 = min(temp[i][0][1], temp[i][1][1])
        for j in range(0, 4):
            temp[i][j][0] -= erase_0
            temp[i][j][1] -= erase_1
            #print(str((temp[i][j][0], temp[i][j][1])))
        picture = it.transpar(it.transform(cv2.imread('test.png'), temp[i]))
        cv2.imwrite("resources/" + str(i) + ".png", picture)


def draw_tiles(array):
    calcGrid(field)
    for i in range(0, grid_width*grid_height):
        x = int(min(array[i][0][0], array[i][3][0]))
        y = int(min(array[i][0][1], array[i][1][1]))
        temp = pygame.image.load('resources/' + str(i) + '.png')
        screen.blit(temp, (x, y))


def redrawGameWindow():
    #screen.fill(darkBlue)
    screen.blit(pygame.image.load('background.jpg'), (0, 0))
    drawGrid(plotbot, white)
    draw_tiles(top_tiles)
    drawGrid(plottop, black)
    pygame.display.update()


create(top_tiles)

# main loop

run = True
while run:
    fps.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    redrawGameWindow()  # for real game
