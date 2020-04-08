import pygame
import numpy as np
import image_transformation as it
import cv2
import os

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
blockSize = 81  # size of a block in grid + 1
perspective = 0.87  # 30% inclination

wind_width, wind_height = 1200, 800


class IterRegistry(type):
    def __iter__(cls):
        return iter(cls._registry)


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


class textures(object):
    __metaclass__ = IterRegistry
    _reg = []

    def __init__(self, name):
        self._reg.append(self)
        self.name = name
        self.raw = 'resources/textures/raw/' + self.name + '.png'
        self.folder = 'resources/textures/' + self.name + '/'
        self.letter = ''


grass = textures('grass')
grass.letter = 'g'
stone = textures('stone_tile')
stone.letter = 's'
water = textures('water')
water.letter = 'w'
wood = textures('wood')
wood.letter = 'd'


def correlate(letter):
    for texitem in textures._reg:
        if texitem.letter == letter:
            return texitem
    else:
        pass


for texitem in textures._reg:  # create those folders
    if not os.path.exists(texitem.folder):
        os.makedirs(texitem.folder)


#stick to such grid
grid_height, grid_width = 9, 13
#stick to such field
field = object2d(int(0.06 * wind_width), int(0.03 * wind_height), int(0.83 * wind_width), int(0.81 * wind_height))

top_tiles = np.zeros((grid_height*grid_width, 4, 2), dtype = "float32")
extra_grid = np.zeros((grid_width, 4, 2), dtype = "float32")
plottop = np.zeros((grid_height, grid_width, 4), dtype=tuple)


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


def calcGrid():
    temp = 0
    for i in range(0, grid_height):
        y = field.y + i * blockSize
        for j in range(0, grid_width):
            x = field.x + j * blockSize
            # cellbot = object2d(x, y, blockSize - 1, blockSize - 1)
            celltop = object2d(x, y, blockSize - 1, blockSize - 1)
            # cellbot.level = 3 * blockSize
            celltop.level = 0
            celltop.do_inclination(perspective)
            # cellbot.do_inclination(perspective)

            plottop[i][j] = to_plot(celltop)
            # plotbot[i][j] = to_plot(cellbot)

            til(top_tiles, temp, celltop)
            til(extra_grid, j, celltop)
            extra_grid[j][0] = extra_grid[j][3]
            extra_grid[j][1] = extra_grid[j][2]
            extra_grid[j][2] = (extra_grid[j][2][0], extra_grid[j][2][1] + 0.9 * blockSize)
            extra_grid[j][3] = (extra_grid[j][3][0], extra_grid[j][3][1] + 0.9 * blockSize)
            # til(bot_tiles, temp, cellbot)
            temp += 1


def create(texture):
    calcGrid()
    if len(os.listdir(texture.folder)) == 0:
        empty = True
    else:
        empty = False
    if empty:  # if resource folder is empty
        temp = top_tiles
        for i in range(0, grid_width*grid_height):
            erase_0 = min(temp[i][0][0], temp[i][3][0])
            erase_1 = min(temp[i][0][1], temp[i][1][1])
            for j in range(0, 4):
                temp[i][j][0] -= erase_0
                temp[i][j][1] -= erase_1
            picture = it.transpar(it.transform(cv2.imread(texture.raw), temp[i]))
            cv2.imwrite(texture.folder + str(i) + ".png", picture)
    temp2 = extra_grid
    erase_0, erase_1 = temp2[0][0][0], temp2[0][0][1]
    for j in range(0, 4):
        temp2[0][j][0] -= erase_0
        temp2[0][j][1] -= erase_1
    picture = it.transform(cv2.imread(texture.raw), temp2[0])
    picture = it.adjust_gamma(picture, 0.3)
    cv2.imwrite(texture.folder + "bottom.png", picture)