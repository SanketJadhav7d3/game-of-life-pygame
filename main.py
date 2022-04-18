# game of life project
# Rules
# Any live cell with fewer than two live neighbours dies, as if by
# underpopulation. Any live cell with two or three live neighbours lives on to
# the next generation. Any live cell with more than three live neighbours
# dies, as if by overpopulation. Any dead cell with exactly three live
# neighbours becomes a live cell by reproduction.

from this import d
import pygame
import numpy as np
from pygame.locals import *

SCREEN_HEIGHT = 480
SCREEN_WIDTH = 480

cells = np.random.randint(2, size=(80, 80))

cell_size = 5

def get_info(i, j):
    global cells 
    info = 0
    for a in range(i-1, i+2):
        for b in range(j-1, j+2):
            if a == i and b == j: continue 
            if a < 0 or b < 0: continue
            if a >= cells.shape[0] or b >= cells.shape[1]: continue
            if cells[a][b] == None: continue
            info += cells[a][b]
    return info 

def update(cells):
    '''
        To update the cells lives
    '''
    for i in range(cells.shape[0]):
        for j in range(cells.shape[1]):
            # underpopulation
            if cells[i][j] == 1 and get_info(i, j) < 2:
                cells[i][j] = 0
            # overpopulation
            if cells[i][j] == 1 and get_info(i, j) > 3:
                cells[i][j] = 0
            # reproduction
            if cells[i][j] == 0 and (get_info(i, j) == 2 or get_info(i, j) == 3):
                cells[i][j] = 1



def draw(window, cells):
    '''
        To draw the new generation to the screen
    '''
    for i in range(cells.shape[0]):
        for j in range(cells.shape[1]):
            rectangle = pygame.Rect(i * (cell_size + 1), j * (cell_size + 1), cell_size, cell_size)
            if cells[i][j] == 1:
                pygame.draw.rect(window, (31, 81, 255), rectangle)
            else:
                pygame.draw.rect(window, (0, 0, 0), rectangle)

def main():
    drawing = False
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False 

            if event.type == pygame.MOUSEMOTION:
                cur_pos = pygame.mouse.get_pos()
                if drawing:
                    if cur_pos[0] % 5 == 0 and cur_pos[1] % 5 == 0:
                        rectangle = pygame.Rect(cur_pos[0], cur_pos[1], cell_size, cell_size)
                        pygame.draw.rect(screen, (255, 255, 255), rectangle)
                        print(cur_pos)

            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True

            if event.type == pygame.MOUSEBUTTONUP:
                drawing = False

        draw(screen, cells)

        update(cells)

        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()
