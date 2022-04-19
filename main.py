#!/Users/sanketjadhav/opt/miniconda3/envs/QuantumProgramming/bin/python

# game of life project
# Rules
# Any live cell with fewer than two live neighbours dies, as if by
# underpopulation. Any live cell with two or three live neighbours lives on to
# the next generation. Any live cell with more than three live neighbours
# dies, as if by overpopulation. Any dead cell with exactly three live
# neighbours becomes a live cell by reproduction.

import math
import pygame
import numpy as np
from pygame.locals import *

SCREEN_HEIGHT = 500
SCREEN_WIDTH = 500

cell_size = 5

rows = SCREEN_HEIGHT // cell_size
cols = SCREEN_WIDTH // cell_size


def get_info(i, j, cells):
    info = 0
    for a in range(i-1, i+2):
        for b in range(j-1, j+2):
            if a == i and b == j: continue
            if a < 0 or b < 0: continue
            if a >= cells.shape[0] or b >= cells.shape[1]: continue
            if cells[a][b] == None: continue
            info += cells[a][b]
    return info

def positionByGrid(grid_size, x, y):
    '''
        To get at which position of mouse by grid
    '''
    x = x // grid_size
    y = y // grid_size
    return x, y 

def update(cells):
    '''
        To update the cells lives
    '''
    next_gen = np.zeros((rows, cols))
    for i in range(cells.shape[0]):
        for j in range(cells.shape[1]):
            # underpopulation
            if cells[i][j] == 1 and get_info(i, j, cells) < 2:
                continue
            # overpopulation
            elif cells[i][j] == 1 and get_info(i, j, cells) > 3:
                continue
            # any life cell with 2 or 3 neighbours lives on to the next generation
            elif cells[i][j] == 1 and (get_info(i, j, cells) == 2 or get_info(i, j, cells) == 3): 
                next_gen[i][j] = 1
            # reproduction
            elif cells[i][j] == 0 and get_info(i, j, cells) == 3:
                next_gen[i][j] = 1

    return next_gen

def draw(window, cells_):
    '''
        To draw the new generation to the screen
    '''
    for i in range(cells_.shape[0]):
        for j in range(cells_.shape[1]):
            rectangle = pygame.Rect(i * cell_size, j * cell_size, cell_size - 1, cell_size - 1)
            if cells_[i][j] == 1:
                pygame.draw.rect(window, (31, 81, 255), rectangle)
            else:
                pygame.draw.rect(window, (0, 0, 0), rectangle)


def main():
    cells = np.zeros((rows, cols))
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    running = True
    drawing = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

                # start the generations
                if event.key == K_RETURN:
                    while event.key != K_ESCAPE:
                        update(cells)
                        draw(screen, cells)

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    # get the curpos of the mouse
                    cur_pos = pygame.mouse.get_pos()
                    # get the position of the mouse by grid
                    x, y = positionByGrid(cell_size, cur_pos[0], cur_pos[1])
                    # set the cells value alive
                    cells[x][y] = 1
                    # convert x and y coordinates to its previous multiple of 5
                    cur_pos = list(map(lambda x: math.floor(x / 5) * 5, cur_pos))
                    # draw the rectangle
                    rectangle = pygame.Rect(cur_pos[0], cur_pos[1], cell_size - 1, cell_size - 1)
                    pygame.draw.rect(screen, (31, 81, 255), rectangle)

            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True

            if event.type == pygame.MOUSEBUTTONUP:
                drawing = False

        if not drawing:
            draw(screen, cells)
            cells = update(cells)

        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()
