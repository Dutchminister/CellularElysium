import pygame
import time

# Define constants
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 10
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
FPS = 10

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life - Toroidal Grid")

# Function to initialize the grid with a glider at the center
def initialize_grid():
    grid = [[0] * COLS for _ in range(ROWS)]
    glider_pattern = [[0, 1, 0],
                      [0, 0, 1],
                      [1, 1, 1]]
    center_row, center_col = ROWS // 2, COLS // 2
    for i in range(3):
        for j in range(3):
            grid[center_row + i][center_col + j] = glider_pattern[i][j]
    return grid

# Function to draw the grid on the screen
def draw_grid(grid):
    screen.fill((255, 255, 255))
    for row in range(ROWS):
        for col in range(COLS):
            color = (0, 0, 0) if grid[row][col] else (255, 255, 255)
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 0)

# Function to update the grid based on Conway's rules with toroidal behavior
def update_grid(grid):
    new_grid = [[0] * COLS for _ in range(ROWS)]
    for row in range(ROWS):
        for col in range(COLS):
            neighbors = sum(grid[(row + i) % ROWS][(col + j) % COLS] for i in range(-1, 2) for j in range(-1, 2)) - grid[row][col]
            if grid[row][col] == 1 and (neighbors < 2 or neighbors > 3):
                new_grid[row][col] = 0
            elif grid[row][col] == 0 and neighbors == 3:
                new_grid[row][col] = 1
            else:
                new_grid[row][col] = grid[row][col]
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
