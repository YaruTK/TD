import pygame
import map_read as mr
import field_calc as fp

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

# str
ver = '0.1.7'

wind_width, wind_height = 1200, 800

fps = pygame.time.Clock()

screen = pygame.display.set_mode((wind_width, wind_height))

pygame.display.set_caption("Tower defence v." + ver)

MAP = mr.read('resources/map0')

grid_width, grid_height = 13, 9


def plot(ar, color, window):
    pygame.draw.aalines(window, color, True, ar)


def drawGrid(layer, colour):
    # calcGrid(field)
    for i in range(0, grid_height):
        for j in range(0, grid_width):
            plot(layer[i][j], colour, screen)
            if i == grid_height - 1:
                plot(fp.extra_grid[j], black, screen)


def draw_tiles(array):
    fp.calcGrid()
    for i in range(0, grid_width*grid_height):
        x = int(min(array[i][0][0], array[i][3][0]))
        y = int(min(array[i][0][1], array[i][1][1]))
        row = i // grid_width
        col = i % grid_width
        texture = fp.correlate(MAP[row][col])
        temp = pygame.image.load(texture.folder + str(i) + '.png')
        screen.blit(temp, (x, y))
    for i in range(0, grid_width):
        x = int(fp.extra_grid[i][0][0])
        y = int(fp.extra_grid[i][0][1])
        texture = fp.correlate(MAP[grid_height-1][i])
        temp = pygame.image.load(texture.folder + 'bottom.png')
        screen.blit(temp, (x, y))


def redrawGameWindow():
    screen.fill(darkBlue)
    screen.blit(pygame.image.load('resources/background.jpg'), (0, 0))
    # drawGrid(plotbot, white)
    draw_tiles(fp.top_tiles)
    drawGrid(fp.plottop, black)
    pygame.display.update()


fp.calcGrid()
for texitem in fp.textures._reg:
    fp.create(texitem)


# main loop
run = True
while run:
    fps.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    redrawGameWindow()  # for real game
