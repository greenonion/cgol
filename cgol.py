# Conway's Game of Life

import sys
import pygame
import random
import array

#** GLOBAL SETTINGS **
# Trying to use bit representation
# using python array module
version = "2.00"
bottom_border = 20
# Framerate of the Game
framerate = 18.2
# Cell dimensions
cell_dim = (5, 5)
# Colours
snow = (255, 250, 250)
black = (0, 0, 0)

class Grid:
    """The class for the cellgrid"""
    
    # Initialize grid
    def __init__(self, cells, density):
        # Store width and height dimensions
        self.width = cells[0]
        self.height = cells[1]
        self.density = density
        # Each byte stores 8 bits, so every cell will represent 8 squares
        self.width_in_bytes = cells[0]/8
        # Total length of the array
        self.length_in_bytes = self.width_in_bytes * self.height
        # Initialize array with zeroes
        self.cellmap = array.array('B', [0]*self.length_in_bytes) 
        # Randomize array
        self.randomize()
        
    # Set cell value to 1
    def set_cell(self, width, height):
        # Determine array index position. 
        # Every line contains width / 8 cells
        cell_idx = height * self.width_in_bytes + width / 8
        # Now the width modulo 8 operation will tell which bit
        # represents the cell
        self.cellmap[cell_idx] |= 0x80 >> (width & 0x07)

    # Set cell value to 0
    def unset_cell(self, width, height):
        # Determine array index position. 
        # Every line contains width / 8 cells
        cell_idx = height * self.width_in_bytes + width / 8
        # Now the width modulo 8 operation will tell which bit
        # represents the cell
        self.cellmap[cell_idx] &= ~(0x80 >> (width & 0x07))

    # Check if cell is set
    def check_set(self, x, y):
        # Determine array index position. 
        # Every line contains width / 8 cells
        cell_idx = y * self.width_in_bytes + x / 8
        # Now the width modulo 8 operation will tell which bit
        # represents the cell
        if (self.cellmap[cell_idx] & 0x80 >> (x & 0x07)):
            return True
        else:
            return False

    # Randomize grid to get unique starting generation
    def randomize(self):
        for i in xrange(self.width):
            for j in xrange(self.height):
                if random.uniform(0, 1) < self.density:
                    self.set_cell(i, j)

    # Get live neighbour cells
    def count_live_neighbours(self, x, y):
        # Wrap around the edges
        prev_x = (x-1) % self.width
        prev_y = (y-1) % self.height
        next_x = (x+1) % self.width
        next_y = (y+1) % self.height

        neighs = [(prev_x, prev_y), (x, prev_y), 
                  (next_x, prev_y), (prev_x, y), 
                  (next_x, y), (prev_x, next_y), 
                  (x, next_y), (next_x, next_y)]

        total = 0
        for (i, j) in neighs:
            if self.check_set(i, j):
                total += 1
    
        return total 

    # Update grid by applying game of life rules
    def update_grid(grid, bg):
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
                    draw_cell(grid, bg, index, black)
                else:
                    next_grid[index] = 1
            # Any dead cell        
            else:        
                # with three live neigbours becomes live
                if (neighbours == 3):
                    next_grid[index] = 1
                    draw_cell(grid, bg, index, snow)

        return next_grid


# Main program
def main(args):
    if len(args) != 4:
        print "USAGE: cgol.py cells_x cells_y density"
        exit(0)
    elif (int(args[1]) % 8 or int(args[2]) % 8):
        # TODO: silently round to closer multiple of 8
        print "INVALID ARGUMENT: cell number must be multiple of 8"
        exit(0)
    elif (float(args[3]) > 1 or float(args[3]) < 0):
        print "INVALID ARGUMENT: Density must be between 0 and 1"
        exit(0)
    else:
        cells = (int(args[2]), int(args[1]))
        density = float(args[3])
        

    # Initialize the grid
    #grid = grid_init(cells, density)
    grid = Grid(cells, density)
    # Initialize the graphics
    screen, bg, clock, font, textpos, screen_size = graph_init(cells)
    # Draw initial grid
    draw_grid(grid, bg, screen)

    running = True
    generation = 0
    
    while running:
        # Slow down
        clock.tick(framerate)

        # Compute and draw next generation
        #grid = update_grid(grid, bg)
        update_text(generation, textpos, bg, font, screen_size)
        screen.blit(bg, (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        generation += 1
    
def graph_init(cells):
    # Initialize screen and clock
    width = cells[1] * cell_dim[1]
    height = cells[0] * cell_dim[0]

    pygame.init()
    screen = pygame.display.set_mode((width, height + bottom_border))
    pygame.display.set_caption("Conway's Game of Life " + "v. "+ version)

    bg = screen.convert()
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("arial", 15)
    text = font.render("Generation 1", True, snow)
    textpos = text.get_rect()
    textpos.centerx = (width/2)
    textpos.centery = (height + bottom_border/2)
    bg.blit(text, textpos)
    screen_size = (width, height)
    
    return screen, bg, clock, font, textpos, screen_size

def update_text(gen, textpos, bg, font, screen_size):
    # Delete previous text
    pygame.draw.rect(bg, black, (0, screen_size[1], screen_size[0], bottom_border))
    # Draw new text
    text = font.render("Generation " + str(gen), True, snow)
    bg.blit(text, textpos)



# Helper function, prints neighbour counts
def print_neighbour_counts(grid):
    dims = grid.shape
    print dims
    for i in xrange(dims[0]):
        print
        for j in xrange(dims[1]):
            print count_live_neighbours(grid, (i, j)),

# Draw the grid
def draw_grid(grid, bg, screen):
    #for index, x in np.ndenumerate(grid):
    for i in xrange(grid.width):
        for j in xrange(grid.height):
            if grid.check_set(i, j):
                pygame.draw.rect(bg, snow, (j*cell_dim[1],
                    i*cell_dim[0], cell_dim[0], cell_dim[1]))

    screen.blit(bg, (0, 0))
    pygame.display.flip()

# Draw a single cell            
def draw_cell(grid, bg, pos, colour):
    pygame.draw.rect(bg, colour, (pos[1]*cell_dim[1], pos[0]*cell_dim[0], cell_dim[0], cell_dim[1]))

if __name__ == "__main__": main(sys.argv)
