import pygame
import time
import sys

class GameOfLifeScreensaver:
    def __init__(self, width, height, cell_size, fps):
        self.WIDTH, self.HEIGHT = width, height
        self.CELL_SIZE = cell_size
        self.ROWS, self.COLS = height // cell_size, width // cell_size
        self.FPS = fps

        pygame.init()
        pygame.display.init()

        # Get information about all available displays
        self.displays_info = [pygame.display.Info() for _ in range(pygame.display.get_num_displays())]

        # Use the total width of all displays for the fullscreen window
        total_width = sum(info.current_w for info in self.displays_info)
        self.screen = pygame.display.set_mode((total_width, max(info.current_h for info in self.displays_info)), pygame.FULLSCREEN)
        pygame.display.set_caption("Conway's Game of Life - Screensaver")

        self.grid = self.initialize_grid()
        self.clock = pygame.time.Clock()

    def initialize_grid(self):
            grid = [[0] * self.COLS for _ in range(self.ROWS)]
            
            # First pattern - A Star is Born
            pattern1 = [
                [0, 0, 1],
                [1, 0, 1],
                [0, 1, 1]
            ]
            center_row1, center_col1 = self.ROWS // 3, 2 * self.COLS // 3
            for i in range(3):
                for j in range(3):
                    grid[center_row1 + i][center_col1 + j] = pattern1[i][j]

            # Second pattern - Celestial Harmony
            pattern2 = [
                [1, 1, 1],
                [1, 0, 1],
                [1, 1, 1]
            ]
            center_row2, center_col2 = 2 * self.ROWS // 3, 2 * self.COLS // 3
            for i in range(3):
                for j in range(3):
                    grid[center_row2 + i][center_col2 + j] = pattern2[i][j]

            # Glider - A Spaceship
            glider = [
                [1, 0, 0],
                [0, 1, 1],
                [1, 1, 0]
            ]
            glider_row, glider_col = self.ROWS // 2, self.COLS // 2
            for i in range(3):
                for j in range(3):
                    grid[glider_row + i][glider_col + j] = glider[i][j]
                    
            return grid


    def draw_grid(self):
        self.screen.fill((0, 0, 0))
        
        display_offset = 0
        for display_info in self.displays_info:
            for row in range(self.ROWS):
                for col in range(self.COLS):
                    color = (255, 255, 255) if self.grid[row][col] else (0, 0, 0)
                    rect = (
                        col * self.CELL_SIZE + display_offset,
                        row * self.CELL_SIZE,
                        self.CELL_SIZE,
                        self.CELL_SIZE
                    )
                    pygame.draw.rect(self.screen, color, rect, 0)

            display_offset += display_info.current_w

        pygame.display.flip()


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
            stable_count = 0
            while stable_count < 10:  # Adjust the stability criterion as needed
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                self.draw_grid()
                pygame.display.flip()

                new_grid = self.update_grid()

                if self.grid == new_grid:
                    stable_count += 1
                else:
                    stable_count = 0

                self.grid = new_grid
                self.clock.tick(self.FPS)

            pygame.quit()

if __name__ == "__main__":
    game = GameOfLifeScreensaver(1920 * 2, 1080, 10, 60)  # Adjust parameters as needed for two 1080p monitors
    game.run_simulation()