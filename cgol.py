# Conway's Game of Life

import sys
import pygame
import random
import numpy as np

#** GLOBAL SETTINGS **
# Framerate of the Game
framerate = 240
# Cell dimensions
cell_dim = (5, 5)
# Initial probability
# Colours
snow = (255, 250, 250)
black = (0, 0, 0)

# Main program
def main(args):
    if len(args) != 4:
        print "USAGE: cgol.py cells_x cells_y density"
        exit(0)
    if (float(args[3]) > 1 or float(args[3]) < 0):
        print "density must be between 0 and 1"
        exit(0)
    else:
        cells = (int(args[2]), int(args[1]))
        density = float(args[3])
        

    # Initialize the grid
    grid = init(cells, density)
    # Initialize the graphics
    screen, bg, clock = graph_init(cells)

    running = True
    
    while running:
        # Slow down
        clock.tick(framerate)

        # Draw current generation
        draw_grid(grid, bg)
        screen.blit(bg, (0, 0))
        pygame.display.flip()

        # Compute next generation
        grid = update_grid(grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


def graph_init(cells):
    # Initialize screen and clock
    width = cells[1] * cell_dim[1]
    height = cells[0] * cell_dim[0]

    screen = pygame.display.set_mode((width, height))
    bg = screen.convert()
    clock = pygame.time.Clock()
    
    return screen, bg, clock

# Initialize grid
def init(cells, density):
    grid = np.random.sample(cells)
    for index, x in np.ndenumerate(grid):
        if x < density:
            grid[index] = 1
        else:
            grid[index] = 0

    return grid

# Update grid by applying game of life rules
def update_grid(grid):
    dims = grid.shape
    next_grid = np.zeros(dims)
    for index, x in np.ndenumerate(grid):
        neighbours = count_live_neighbours(grid, index)
        # Any live cell 
        if (x == 1):
            # with fewer than two or more than three
            # living neighours dies
            if (neighbours < 2 or neighbours > 3):
                next_grid[index] = 0
            else:
                next_grid[index] = 1
        # Any dead cell        
        else:        
            # with three live neigbours becomes live
            if (neighbours == 3):
                next_grid[index] = 1

    return next_grid


# Helper function, returns live neighbour cells
def count_live_neighbours(grid, cell):
    dims = grid.shape
    x = cell[0]
    y = cell[1]
    neighs = [(x-1, y-1), (x, y-1), (x+1, y-1),
              (x-1, y), (x+1, y),
              (x-1, y+1), (x, y+1), (x+1, y+1)]

    total = 0
    for (x, y) in neighs:
        if (x < 0): x = dims[0] - 1
        if (y < 0): y = dims[1] - 1
        if (x == dims[0]): x = 0
        if (y == dims[1]): y = 0
        if grid[(x, y)] == 1:
                total += 1
    
    return total 

# Helper function, prints neighbour counts
def print_neighbour_counts(grid):
    dims = grid.shape
    print dims
    for i in xrange(dims[0]):
        print
        for j in xrange(dims[1]):
            print count_live_neighbours(grid, (i, j)),

# Draw the grid
def draw_grid(grid, bg):
    for index, x in np.ndenumerate(grid):
        if x == 1:
            pygame.draw.rect(bg, snow, (index[1]*cell_dim[1],
                 index[0]*cell_dim[0], cell_dim[0], cell_dim[1]))
        elif x == 0:
            pygame.draw.rect(bg, black, (index[1]*cell_dim[1],
                 index[0]*cell_dim[0], cell_dim[0], cell_dim[1]))

if __name__ == "__main__": main(sys.argv)
