import pygame
import numpy as np
import time

# Define constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 10
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
FPS = 10

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life - Gosper Glider Gun")

# Function to initialize the grid with a Gosper glider gun at the center
def initialize_grid():
    grid = np.zeros((ROWS, COLS), dtype=int)
    gun_pattern = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    center_row, center_col = ROWS // 2 - len(gun_pattern) // 2, COLS // 2 - len(gun_pattern[0]) // 2
    grid[center_row:center_row + len(gun_pattern), center_col:center_col + len(gun_pattern[0])] = gun_pattern
    return grid

# Function to draw the grid on the screen
def draw_grid(grid):
    screen.fill((255, 255, 255))
    for row in range(ROWS):
        for col in range(COLS):
            color = (0, 0, 0) if grid[row, col] else (255, 255, 255)
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 0)

# Function to update the grid based on Conway's rules with toroidal behavior
def update_grid(grid):
    new_grid = np.copy(grid)
    for row in range(ROWS):
        for col in range(COLS):
            neighbors = np.sum(grid[(row - 1) % ROWS:(row + 2) % ROWS, (col - 1) % COLS:(col + 2) % COLS]) - grid[row, col]
            if grid[row, col] == 1 and (neighbors < 2 or neighbors > 3):
                new_grid[row, col] = 0
            elif grid[row, col] == 0 and neighbors == 3:
                new_grid[row, col] = 1
    return new_grid

# Main function to run the simulation
def main():
    grid = initialize_grid()
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_grid(grid)
        pygame.display.flip()
        grid = update_grid(grid)

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
