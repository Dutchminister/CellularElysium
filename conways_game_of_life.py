import pygame
import numpy as np
import scipy
import json
import time

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
        self.stable_count = 0  # Initialize stable_count as a class member
        
        # Initialize neighbor counts array
        self.neighbor_counts = np.zeros((self.ROWS, self.COLS), dtype=int)
        # Initialize cell ages array
        self.cell_ages = np.zeros((self.ROWS, self.COLS), dtype=int)

        # Editor mode and UI
        self.editing_mode = True
        self.show_buttons = True # Controls visibility of editor buttons

        # Button definitions
        button_font_size = 30 # Smaller font for buttons
        self.button_font = pygame.font.SysFont(None, button_font_size)
        button_height = 40
        button_width = 100
        button_padding = 10
        margin_bottom = 10

        button_y = self.HEIGHT - button_height - margin_bottom

        button_labels = ["Start", "Clear", "Save", "Load", "Load Default"] # Added "Load Default"
        num_buttons = len(button_labels)
        total_buttons_width = (num_buttons * button_width) + ((num_buttons - 1) * button_padding)
        start_x_buttons = (self.WIDTH - total_buttons_width) // 2

        self.buttons = []
        for i, label in enumerate(button_labels):
            action_label = label.lower().replace(" ", "_") # e.g., "load_default"
            rect_x = start_x_buttons + i * (button_width + button_padding)
            rect = pygame.Rect(rect_x, button_y, button_width, button_height)
            self.buttons.append({'label': label, 'rect': rect, 'action': action_label})

    def initialize_grid(self):
        grid = np.zeros((self.ROWS, self.COLS), dtype=int)
        
        # Methuselah - Acorn
        acorn = [
            (0, 1), (1, 3),
            (2, 0), (2, 1), (2, 4), (2, 5), (2, 6)
        ]
        
        start_row = self.ROWS // 2 - 1
        start_col = self.COLS // 2 - 3
        
        for r, c in acorn:
            grid[start_row + r, start_col + c] = 1

        return grid

    def draw_grid(self):
            self.screen.fill((0, 0, 0))
            for row in range(self.ROWS):
                for col in range(self.COLS):
                    if self.grid[row, col] == 1:
                        age = self.cell_ages[row, col]
                        if age == 1:
                            color = (255, 255, 255)  # Bright white for new cells
                        elif age == 2:
                            color = (220, 220, 220)
                        elif age == 3:
                            color = (180, 180, 180)
                        else:  # age >= 4
                            color = (140, 140, 140)  # Darker grey for older cells
                    else:
                        color = (0, 0, 0)  # Black for dead cells
                    pygame.draw.rect(self.screen, color, (col * self.CELL_SIZE, row * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE), 0)

    def update_neighbor_counts(self):
        # Use convolution to efficiently calculate neighbor counts
        kernel = np.array([[1, 1, 1],
                           [1, 0, 1],
                           [1, 1, 1]], dtype=int)
        self.neighbor_counts = scipy.signal.convolve2d(self.grid, kernel, mode='same', boundary='wrap')

    def update_grid(self):
        self.update_neighbor_counts()  # Populate self.neighbor_counts

        new_grid = np.zeros_like(self.grid) # Initialize new_grid as a NumPy array of zeros

        for row in range(self.ROWS):
            for col in range(self.COLS):
                current_cell_state = self.grid[row, col] # Use tuple indexing for NumPy arrays
                num_neighbors = self.neighbor_counts[row, col]

                if current_cell_state == 1:  # Alive cell
                    if num_neighbors < 2 or num_neighbors > 3:
                        new_grid[row, col] = 0  # Dies
                    else:
                        new_grid[row, col] = 1  # Survives
                else:  # Dead cell
                    if num_neighbors == 3:
                        new_grid[row, col] = 1  # Becomes alive
                    else:
                        new_grid[row, col] = 0  # Stays dead

        # Update cell ages based on the transition from self.grid to new_grid
        next_cell_ages = np.zeros_like(self.cell_ages)
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if new_grid[row, col] == 1:  # Cell is alive in new_grid
                    if self.grid[row, col] == 1:  # Cell was also alive in current self.grid (it aged)
                        next_cell_ages[row, col] = self.cell_ages[row, col] + 1
                    else:  # Cell was dead and just became alive (newborn)
                        next_cell_ages[row, col] = 1
                # If new_grid[row, col] == 0, age remains 0 (already initialized by np.zeros_like)
        self.cell_ages = next_cell_ages
        
        return new_grid # new_grid is already a NumPy array

    def save_grid_to_file(self, filename):
        try:
            grid_list = self.grid.tolist()
            with open(filename, 'w') as f:
                json.dump(grid_list, f)
            print(f"Grid successfully saved to {filename}")
        except (IOError, OSError) as e:
            print(f"Error saving grid to {filename}: {e}")

    def load_grid_from_file(self, filename):
        try:
            with open(filename, 'r') as f:
                grid_list = json.load(f)

            # Validate structure and dimensions
            if not isinstance(grid_list, list):
                print(f"Error: Data in {filename} is not a list.")
                return
            if len(grid_list) != self.ROWS:
                print(f"Error: Row count in {filename} ({len(grid_list)}) does not match simulation ({self.ROWS}).")
                return
            if self.ROWS > 0:
                if not isinstance(grid_list[0], list):
                    print(f"Error: Data in {filename} is not a list of lists.")
                    return
                if len(grid_list[0]) != self.COLS:
                    print(f"Error: Column count in {filename} ({len(grid_list[0])}) does not match simulation ({self.COLS}).")
                    return
            elif self.COLS != 0 : # ROWS is 0, but COLS is not, inconsistent
                print(f"Error: Column count in {filename} ({len(grid_list[0]) if self.ROWS > 0 and len(grid_list) > 0 else 'N/A'}) does not match simulation ({self.COLS}).")
                return


            loaded_grid = np.array(grid_list, dtype=int)
            self.grid = loaded_grid

            # Update cell ages for the loaded grid
            self.cell_ages.fill(0) # Clear existing ages
            self.cell_ages[self.grid == 1] = 1 # Set age to 1 for all live cells

            print(f"Grid successfully loaded from {filename}")

        except FileNotFoundError:
            print(f"Error: File {filename} not found.")
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {filename}. File might be corrupted or not valid JSON.")
        except (IOError, OSError) as e:
            print(f"Error loading grid from {filename}: {e}")
        except Exception as e: # Catch any other unexpected errors during loading/validation
            print(f"An unexpected error occurred while loading {filename}: {e}")


    def draw_editor_ui(self):
        if not self.show_buttons:
            return

        button_color = (100, 100, 100)
        text_color = (255, 255, 255)

        for button in self.buttons:
            pygame.draw.rect(self.screen, button_color, button['rect'])
            text_surf = self.button_font.render(button['label'], True, text_color)
            text_rect = text_surf.get_rect(center=button['rect'].center)
            self.screen.blit(text_surf, text_rect)

    def run_simulation(self):
        running = True
        #Start a timer       
        start_time = time.time()
        # previous_grids is for periodic state detection in simulation mode
        previous_grids = []
        end_reason = "Simulation ended" # Default end reason

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    if self.editing_mode: # if quitting from editor, just quit
                        end_reason = "User quit editor"
                    else: # if quitting during simulation, normal quit procedure
                        end_reason = "User quit simulation"

                if self.editing_mode:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        button_clicked_in_editor = False
                        if self.show_buttons:
                            for button in self.buttons:
                                if button['rect'].collidepoint(mouse_pos):
                                    button_clicked_in_editor = True
                                    if button['action'] == 'start':
                                        self.editing_mode = False
                                        # self.show_buttons = False # Keep buttons visible or hide? For now, let's hide.
                                        self.generation = 0
                                        self.stable_count = 0
                                        self.stable_generation = None
                                        # Reset previous_grids for new simulation session
                                        previous_grids = [str(self.grid.tolist())]
                                        # Ensure cell ages are consistent if starting with a pre-drawn pattern
                                        # If grid has live cells not set by user, their age might be 0.
                                        # For simplicity, assume user is happy with ages or uses clear.
                                        # A more robust way: iterate self.grid, if cell is 1 and age is 0, set age to 1.
                                        self.cell_ages[ (self.grid == 1) & (self.cell_ages == 0) ] = 1

                                    elif button['action'] == 'clear':
                                        self.grid.fill(0)
                                        self.cell_ages.fill(0)
                                    elif button['action'] == 'save':
                                        self.save_grid_to_file("custom_grid.json")
                                    elif button['action'] == 'load':
                                        self.load_grid_from_file("custom_grid.json")
                                    elif button['action'] == 'load_default':
                                        self.grid = self.initialize_grid()
                                        self.cell_ages.fill(0)
                                        self.cell_ages[self.grid == 1] = 1
                                        print("Default R-pentomino pattern loaded.")
                                    break # Exit button loop once a button is clicked

                        if not button_clicked_in_editor:
                            # Grid cell toggling if click was not on a button
                            # Ensure click is within grid display area (if UI takes up other space)
                            # For now, assuming buttons don't overlap clickable grid area significantly
                            # or are outside typical drawing region if screen is larger than grid
                            if mouse_pos[1] < self.buttons[0]['rect'].top: # Basic check: click is above buttons
                                clicked_col = mouse_pos[0] // self.CELL_SIZE
                                clicked_row = mouse_pos[1] // self.CELL_SIZE
                                if 0 <= clicked_row < self.ROWS and 0 <= clicked_col < self.COLS:
                                    self.grid[clicked_row, clicked_col] = 1 - self.grid[clicked_row, clicked_col] # Toggle
                                    if self.grid[clicked_row, clicked_col] == 1:
                                        self.cell_ages[clicked_row, clicked_col] = 1 # New cells start with age 1
                                    else:
                                        self.cell_ages[clicked_row, clicked_col] = 0

            if not running: # Exit if QUIT event was processed (either from editor or simulation)
                break

            if self.editing_mode:
                self.screen.fill((0,0,0)) # Clear screen
                self.draw_grid()
                if self.show_buttons:
                    self.draw_editor_ui()
                pygame.display.flip()
                self.clock.tick(self.FPS) # Keep editor responsive
            else: # Simulation Mode
                self.draw_grid()
                # Display generation number on top of the grid
                gen_text_surf = self.font.render(f"Generation: {self.generation}", True, (255, 255, 255))
                self.screen.blit(gen_text_surf, (10, 10))
                pygame.display.flip()

                previous_grid_state = np.copy(self.grid)
                # update_grid also updates self.cell_ages for the new state
                new_grid_array = self.update_grid()

                if np.array_equal(new_grid_array, previous_grid_state):
                    self.stable_count += 1
                else:
                    self.stable_count = 0

                self.grid = new_grid_array

                if self.stable_count >= 10:
                    print("Stable state reached at generation:", self.generation)
                    self.stable_generation = self.generation
                    running = False # Ends simulation loop
                    end_reason = "Stable state"
                elif self.generation > 20:
                    current_grid_str = str(self.grid.tolist())
                    if current_grid_str in previous_grids:
                        print("Periodic grid reached at generation:", self.generation)
                        running = False # Ends simulation loop
                        end_reason = "Periodic state"
                    else:
                        previous_grids.append(current_grid_str)
                    if len(previous_grids) > 10:
                        previous_grids.pop(0)

                if running: # If not ended by stability or periodicity
                    self.generation += 1
                    self.clock.tick(self.FPS)

        # --- Post-simulation report screen (or if user quit editor) ---
        if end_reason == "User quit editor": # If user quit from editor, just close
             pass # pygame.quit() will be called finally
        elif end_reason != "User quit simulation" or self.generation > 0: # Show report unless user quit sim immediately
            # This block will also show if simulation ended due to stable/periodic state
            report_text_str = f"Sim ended: Gen {self.generation}, {end_reason}. SPACE to exit."
            if self.stable_generation is not None and end_reason == "Stable state": # more specific
                 report_text_str = f"Stable state at Gen {self.stable_generation}. SPACE to exit."

            report_surf = self.font.render(report_text_str, True, (0, 255, 0))
            report_rect = report_surf.get_rect(center=(self.WIDTH // 2, self.HEIGHT - 30)) # Adjusted y for clarity

            # Need to redraw grid one last time if simulation ended, then blit text
            self.draw_grid() # Show final state
            self.screen.blit(report_surf, report_rect)
            pygame.display.flip()

            exit_pressed = False
            while not exit_pressed:
                for event_report in pygame.event.get():
                    if event_report.type == pygame.QUIT:
                        exit_pressed = True
                    if event_report.type == pygame.KEYDOWN:
                        if event_report.key == pygame.K_RETURN or event_report.key == pygame.K_SPACE:
                            exit_pressed = True

        pygame.quit()

if __name__ == "__main__":
    # Set up the dimensions of the window
    width = 2160
    height = 1920
    # Simulation pixel size
    pixel_size= 5
    frame_rate = 299.88

    #Provide the parameters for simulation
    game = GameOfLife(width, height, pixel_size, frame_rate)
    game.run_simulation()
