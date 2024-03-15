import pygame
import numpy as np
import scipy

class GameOfLife:
    def __init__(self, width, height, cell_size, fps):
        self.WIDTH, self.HEIGHT = width, height
        self.CELL_SIZE = cell_size
        self.ROWS, self.COLS = height // cell_size, width // cell_size
        self.FPS = fps
        self.generation = 0  # Track current generation

        pygame.init()
        # Enable hardware acceleration
        self.screen = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("Conway's Game of Life - A Cosmic Dance of Cells")
        self.grid = self.initialize_grid()
        self.clock = pygame.time.Clock()
        # Load font for generation display
        self.font = pygame.font.SysFont(None, 36)
        # Track the generation where stability is reached
        self.stable_generation = None
        
        # Initialize neighbor counts array
        self.neighbor_counts = np.zeros((self.ROWS, self.COLS), dtype=int)

    def initialize_grid(self):
        grid = np.zeros((self.ROWS, self.COLS), dtype=int)
        # Methuselah - R-pentomino
        rpentomino = np.array([
            [0, 1, 1],
            [1, 1, 0],
            [0, 1, 0]
        ])
        rpentomino_row, rpentomino_col = self.ROWS // 2, self.COLS // 2 - 3
        grid[rpentomino_row:rpentomino_row+3, rpentomino_col:rpentomino_col+3] = rpentomino
        return grid

    def draw_grid(self):
            self.screen.fill((0, 0, 0))
            for row in range(self.ROWS):
                for col in range(self.COLS):
                    color = (255, 255, 255) if self.grid[row][col] else (0, 0, 0)
                    pygame.draw.rect(self.screen, color, (col * self.CELL_SIZE, row * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE), 0)

    def update_neighbor_counts(self):
        # Use convolution to efficiently calculate neighbor counts
        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]], dtype=int)
        self.neighbor_counts = scipy.signal.convolve2d(self.grid, kernel, mode='same', boundary='wrap')

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
        running = True
        previous_grids = [str(self.grid)]  # Initialize with the string representation of the initial grid configuration
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        if stable_count >= 10:
                            self.stable_generation = self.generation
                            running = False
                            end_reason = "Stable state"

            if stable_count < 10:
                self.draw_grid()
                # Display generation number
                text = self.font.render(f"Generation: {self.generation}", True, (255, 255, 255))
                self.screen.blit(text, (10, 10))
                pygame.display.flip()
                new_grid = self.update_grid()

                # Check for periodic grid only after a few generations
                if self.generation > 20:
                    if str(new_grid) in previous_grids:
                        print("Periodic grid reached at generation:", self.generation)
                        running = False
                        end_reason = "Periodic state"
                    else:
                        previous_grids.append(str(new_grid))

                    if len(previous_grids) > 10:  # Limit the number of previous grids to check
                        previous_grids.pop(0)

                self.grid = new_grid
                self.generation += 1  # Increment generation number
                self.clock.tick(self.FPS)
            else:
                self.draw_grid()
                pygame.display.flip()
                self.clock.tick(self.FPS)
        # Display simulation results
        report_text = f"Simulation ended at generation {self.generation} due to a {end_reason}. Press Space to exit."
        text = self.font.render(report_text, True, (0, 255, 0))
        text_rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT - 10))  # Bottom of screen
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        # Wait for user to press Enter or Space to exit
        exit_pressed = False
        while not exit_pressed:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        exit_pressed = True
        pygame.quit()

if __name__ == "__main__":
    # Set up the dimensions of the window
    width = 1920
    height = 1080
    # Simulation pixel size
    pixel_size= 10
    frame_rate = 60

    #Provide the parameters for simulation
    game = GameOfLife(width, height, pixel_size, frame_rate)
    game.run_simulation()
