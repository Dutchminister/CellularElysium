import pygame
import time

class GameOfLife:
    def __init__(self, width, height, cell_size, fps):
        self.WIDTH, self.HEIGHT = width, height
        self.CELL_SIZE = cell_size
        self.ROWS, self.COLS = height // cell_size, width // cell_size
        self.FPS = fps

        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Conway's Game of Life - Toroidal Grid")

        self.grid = self.initialize_grid()
        self.clock = pygame.time.Clock()

    def initialize_grid(self):
        grid = [[0] * self.COLS for _ in range(self.ROWS)]
        
        # First pattern
        pattern1 = [
            [0, 0, 1],
            [1, 0, 1],
            [0, 1, 1]
        ]
        center_row1, center_col1 = self.ROWS // 3, 2* self.COLS // 3
        for i in range(3):
            for j in range(3):
                grid[center_row1 + i][center_col1 + j] = pattern1[i][j]

        # Second pattern
        pattern2 = [
            [1, 1, 1],
            [1, 0, 1],
            [1, 1, 1]
        ]
        center_row2, center_col2 = 2 * self.ROWS // 3, 2 * self.COLS // 3
        for i in range(3):
            for j in range(3):
                grid[center_row2 + i][center_col2 + j] = pattern2[i][j]

        return grid

    def draw_grid(self):
        self.screen.fill((255, 255, 255))
        for row in range(self.ROWS):
            for col in range(self.COLS):
                color = (0, 0, 0) if self.grid[row][col] else (255, 255, 255)
                pygame.draw.rect(self.screen, color, (col * self.CELL_SIZE, row * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE), 0)

    def update_grid(self):
        new_grid = [[0] * self.COLS for _ in range(self.ROWS)]
        for row in range(self.ROWS):
            for col in range(self.COLS):
                neighbors = sum(self.grid[(row + i) % self.ROWS][(col + j) % self.COLS] for i in range(-1, 2) for j in range(-1, 2)) - self.grid[row][col]
                if self.grid[row][col] == 1 and (neighbors < 2 or neighbors > 3):
                    new_grid[row][col] = 0
                elif self.grid[row][col] == 0 and neighbors == 3:
                    new_grid[row][col] = 1
                else:
                    new_grid[row][col] = self.grid[row][col]
        return new_grid

    def run_simulation(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.draw_grid()
            pygame.display.flip()
            self.grid = self.update_grid()

            self.clock.tick(self.FPS)

        pygame.quit()

if __name__ == "__main__":
    game = GameOfLife(1920, 1080, 10, 60)
    game.run_simulation()
