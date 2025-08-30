import pygame
import numpy as np
import scipy
import json
import time

PRESET_PATTERNS = {
    "Still Lifes": {
        "Block": {"pattern": [(0,0), (0,1), (1,0), (1,1)], "width": 2, "height": 2},
        "Beehive": {"pattern": [(0,1), (0,2), (1,0), (1,3), (2,1), (2,2)], "width": 4, "height": 3},
        "Loaf": {"pattern": [(0,1), (0,2), (1,0), (1,3), (2,1), (2,3), (3,2)], "width": 4, "height": 4},
        "Boat": {"pattern": [(0,0), (0,1), (1,0), (1,2), (2,1)], "width": 3, "height": 3},
    },
    "Oscillators": {
        "Blinker": {"pattern": [(0,0), (0,1), (0,2)], "width": 3, "height": 1},
        "Toad": {"pattern": [(0,1), (0,2), (0,3), (1,0), (1,1), (1,2)], "width": 4, "height": 2},
        "Beacon": {"pattern": [(0,0), (0,1), (1,0), (1,1), (2,2), (2,3), (3,2), (3,3)], "width": 4, "height": 4},
        "Pulsar": {"pattern": [(0,2),(0,3),(0,4),(0,8),(0,9),(0,10), (2,0),(2,5),(2,7),(2,12), (3,0),(3,5),(3,7),(3,12), (4,0),(4,5),(4,7),(4,12), (5,2),(5,3),(5,4),(5,8),(5,9),(5,10), (7,2),(7,3),(7,4),(7,8),(7,9),(7,10), (8,0),(8,5),(8,7),(8,12), (9,0),(9,5),(9,7),(9,12), (10,0),(10,5),(10,7),(10,12), (12,2),(12,3),(12,4),(12,8),(12,9),(12,10)], "width": 13, "height": 13},
    },
    "Spaceships": {
        "Glider": {"pattern": [(0,1), (1,2), (2,0), (2,1), (2,2)], "width": 3, "height": 3},
        "LWSS": {"pattern": [(0,0), (0,3), (1,4), (2,0), (2,4), (3,1), (3,2), (3,3), (3,4)], "width": 5, "height": 4},
    },
    "Methuselahs": {
        "R-pentomino": {"pattern": [(0,1), (0,2), (1,0), (1,1), (2,1)], "width": 3, "height": 3},
        "Acorn": {"pattern": [(0,1), (1,3), (2,0), (2,1), (2,4), (2,5), (2,6)], "width": 7, "height": 3},
    },
    "Guns": {
        "Gosper Glider Gun": {"pattern": [(0,24),(1,22),(1,24),(2,12),(2,13),(2,20),(2,21),(2,34),(2,35),(3,11),(3,15),(3,20),(3,21),(3,34),(3,35),(4,0),(4,1),(4,10),(4,16),(4,20),(4,21),(5,0),(5,1),(5,10),(5,14),(5,16),(5,17),(5,22),(5,24),(6,10),(6,16),(6,24),(7,11),(7,15),(8,12),(8,13)], "width": 36, "height": 9},
    }
}

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
        self.countdown_timer = 15
        self.start_time = None
        self.show_countdown_prompt = True
        self.current_pattern_data = None
        self.placing_pattern_mode = False
        self.pattern_preview_pos = None
        self.show_pattern_library = False
        self.pattern_library_buttons = []
        self.PATTERN_LIBRARY_AREA_RECT = pygame.Rect(50, 50, 250, self.HEIGHT - 100)
        
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

        button_labels = ["Start", "Clear", "Save", "Load", "Load Default", "Library"] # Added "Library"
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
                        color = (0, 255, 0)  # Bright green for newborn
                    elif age == 2:
                        color = (255, 255, 0)  # Yellow for young
                    elif age == 3:
                        color = (255, 165, 0)  # Orange for mature
                    elif age == 4:
                        color = (255, 0, 0)  # Red for old
                    else:
                        color = (128, 0, 128)  # Purple for very old
                else:
                    color = (0, 0, 0)  # Black for dead cells
                pygame.draw.rect(self.screen, color, (col * self.CELL_SIZE, row * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE), 0)

        if self.editing_mode and self.placing_pattern_mode and self.current_pattern_data and self.pattern_preview_pos:
            pattern_cells = self.current_pattern_data['pattern']
            preview_origin_row, preview_origin_col = self.pattern_preview_pos
            for rel_row, rel_col in pattern_cells:
                draw_row = preview_origin_row + rel_row
                draw_col = preview_origin_col + rel_col
                if 0 <= draw_row < self.ROWS and 0 <= draw_col < self.COLS:
                    cell_rect = pygame.Rect(
                        draw_col * self.CELL_SIZE,
                        draw_row * self.CELL_SIZE,
                        self.CELL_SIZE,
                        self.CELL_SIZE
                    )
                    pygame.draw.rect(self.screen, (100, 100, 150), cell_rect)  # Solid light blue/purple for preview


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
        live_cells = []
        for r in range(self.ROWS):
            for c in range(self.COLS):
                if self.grid[r, c] == 1:
                    live_cells.append((r, c))

        if not live_cells:
            print("No pattern to save. Grid is empty.")
            return

        min_row = min(r for r, c in live_cells)
        max_row = max(r for r, c in live_cells)
        min_col = min(c for r, c in live_cells)
        max_col = max(c for r, c in live_cells)

        pattern_width = max_col - min_col + 1
        pattern_height = max_row - min_row + 1

        relative_pattern_cells = []
        for r, c in live_cells:
            relative_pattern_cells.append((r - min_row, c - min_col))

        save_data = {
            "name": "user_saved_pattern", # Placeholder name
            "pattern": relative_pattern_cells,
            "width": pattern_width,
            "height": pattern_height
        }

        try:
            with open(filename, 'w') as f:
                json.dump(save_data, f, indent=4)
            print(f"Pattern successfully saved to {filename}")
        except (IOError, OSError) as e:
            print(f"Error saving pattern to {filename}: {e}")

    def load_grid_from_file(self, filename):
        try:
            with open(filename, 'r') as f:
                loaded_data = json.load(f)

            # Validate loaded data structure
            if not isinstance(loaded_data, dict):
                print(f"Error: Invalid pattern file format in {filename}. Data should be a dictionary.")
                return

            required_keys = ["pattern", "width", "height"]
            for key in required_keys:
                if key not in loaded_data:
                    print(f"Error: Invalid pattern file format in {filename}. Missing key: '{key}'.")
                    return

            if not isinstance(loaded_data["pattern"], list):
                print(f"Error: Invalid pattern file format in {filename}. 'pattern' should be a list.")
                return
            if not isinstance(loaded_data["width"], int):
                print(f"Error: Invalid pattern file format in {filename}. 'width' should be an integer.")
                return
            if not isinstance(loaded_data["height"], int):
                print(f"Error: Invalid pattern file format in {filename}. 'height' should be an integer.")
                return

            # Store pattern data and enter placement mode
            self.current_pattern_data = loaded_data
            self.placing_pattern_mode = True
            self.pattern_preview_pos = None # Or (0,0) - will be updated by mouse move

            pattern_name = loaded_data.get("name", "Unnamed Pattern")
            print(f"Pattern '{pattern_name}' loaded from {filename}. Move mouse to position and click to place.")

        except FileNotFoundError:
            print(f"Error: File {filename} not found.")
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {filename}. File might be corrupted or not valid JSON.")
        except (IOError, OSError) as e:
            print(f"Error loading pattern from {filename}: {e}")
        except Exception as e: # Catch any other unexpected errors
            print(f"An unexpected error occurred while loading pattern from {filename}: {e}")


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

        if self.show_pattern_library:
            # Draw a background for the library panel
            library_bg_color = (50, 50, 50) # Dark grey
            pygame.draw.rect(self.screen, library_bg_color, self.PATTERN_LIBRARY_AREA_RECT)

            self.pattern_library_buttons = [] # Clear old buttons
            item_y_offset = self.PATTERN_LIBRARY_AREA_RECT.top + 10
            item_x_pos = self.PATTERN_LIBRARY_AREA_RECT.left + 10
            item_height = 30 # Approximate height of a text item
            item_padding = 5

            for category_name, category_patterns in PRESET_PATTERNS.items():
                # Draw category name
                cat_surf = self.button_font.render(f"[{category_name}]", True, (200, 200, 200)) # Lighter color for category
                cat_rect = cat_surf.get_rect(topleft=(item_x_pos, item_y_offset))
                self.screen.blit(cat_surf, cat_rect)
                item_y_offset += item_height # Spacing for category title

                for pattern_name, pattern_data in category_patterns.items():
                    if item_y_offset + item_height > self.PATTERN_LIBRARY_AREA_RECT.bottom - 10: # Check for overflow
                        # TODO: Add a visual cue or logging if items are being truncated.
                        break

                    pat_text_surf = self.button_font.render(pattern_name, True, (255, 255, 255))
                    # Create a rect for the pattern name for click detection and highlighting
                    pat_rect = pat_text_surf.get_rect(topleft=(item_x_pos + 10, item_y_offset)) # Indent pattern names

                    self.pattern_library_buttons.append({
                        'label': pattern_name,
                        'rect': pat_rect,
                        'action': 'select_pattern',
                        'pattern_data': pattern_data.copy() # Store a copy of the pattern data
                    })

                    # Highlight if mouse is over this specific pattern button
                    if pat_rect.collidepoint(pygame.mouse.get_pos()):
                        pygame.draw.rect(self.screen, (70, 70, 70), pat_rect) # Highlight background

                    self.screen.blit(pat_text_surf, pat_rect)
                    item_y_offset += item_height + item_padding

                item_y_offset += item_height // 2 # Extra spacing between categories
                if item_y_offset + item_height > self.PATTERN_LIBRARY_AREA_RECT.bottom - 10: # Check again for category overflow
                    break

        if self.editing_mode and self.placing_pattern_mode and self.current_pattern_data:
            pattern_name = self.current_pattern_data.get("name", "Unnamed Pattern")
            placement_text = f"Placing: {pattern_name}. Left-click: place. Right-click/Esc: cancel."
            text_surf = self.font.render(placement_text, True, (255, 255, 0)) # Yellow text
            text_rect = text_surf.get_rect(centerx=self.WIDTH // 2, top=10)
            self.screen.blit(text_surf, text_rect)

    def run_simulation(self):
        running = True
        #Start a timer
        self.start_time = time.time()  # Initialize self.start_time
        # previous_grids is for periodic state detection in simulation mode
        previous_grids = []
        end_reason = "Simulation ended" # Default end reason

        while running:
            # Moved the event loop inside the 'if self.editing_mode:' block or 'else:' block
            # This top-level event loop is being restructured.

            if self.editing_mode:
                # Update pattern preview position if in placement mode
                if self.placing_pattern_mode and self.current_pattern_data:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    grid_row = mouse_y // self.CELL_SIZE
                    grid_col = mouse_x // self.CELL_SIZE
                    self.pattern_preview_pos = (grid_row, grid_col)

                self.screen.fill((0,0,0)) # Clear screen
                self.draw_grid() # This will now also draw the preview if active

                if self.show_countdown_prompt:
                    elapsed_time = time.time() - self.start_time
                    if elapsed_time >= self.countdown_timer:
                        self.editing_mode = False
                        self.show_countdown_prompt = False
                    else:
                        remaining_time = int(self.countdown_timer - elapsed_time) + 1
                        prompt_text = f"Simulation starts in {remaining_time}s. Press any key for edit mode."
                        text_surface = self.font.render(prompt_text, True, (255, 255, 255))
                        text_rect = text_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
                        self.screen.blit(text_surface, text_rect)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        end_reason = "User quit editor" if self.editing_mode else "User quit simulation"
                        break # Break from event loop

                    # Handle ESC key press for cancelling placement or countdown prompt
                    if event.type == pygame.KEYDOWN:
                        if self.placing_pattern_mode and event.key == pygame.K_ESCAPE:
                            self.placing_pattern_mode = False
                            self.current_pattern_data = None
                            self.pattern_preview_pos = None
                            print("Pattern placement cancelled.")
                            # Consider event handled to prevent other keydown actions
                        elif self.show_countdown_prompt: # Original logic for countdown
                             self.show_countdown_prompt = False
                             # Optional: Reset self.start_time = time.time() if any key should reset countdown

                    if not self.show_countdown_prompt and event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        button_clicked_in_editor = False # General flag for UI interaction

                        # 1. Pattern Placement Logic (Left Click)
                        if self.placing_pattern_mode and event.button == 1 and \
                           self.current_pattern_data and self.pattern_preview_pos and \
                           not (self.show_pattern_library and self.PATTERN_LIBRARY_AREA_RECT.collidepoint(mouse_pos)):

                            place_origin_row, place_origin_col = self.pattern_preview_pos
                            pattern_cells = self.current_pattern_data['pattern']

                            for rel_row, rel_col in pattern_cells:
                                target_row = place_origin_row + rel_row
                                target_col = place_origin_col + rel_col
                                if 0 <= target_row < self.ROWS and 0 <= target_col < self.COLS:
                                    self.grid[target_row, target_col] = 1
                                    self.cell_ages[target_row, target_col] = 1

                            self.placing_pattern_mode = False
                            self.current_pattern_data = None
                            self.pattern_preview_pos = None
                            print("Pattern placed.")
                            button_clicked_in_editor = True # Consumed the click

                        # 2. Pattern Placement Cancellation (Right Click)
                        elif self.placing_pattern_mode and event.button == 3:
                            self.placing_pattern_mode = False
                            self.current_pattern_data = None
                            self.pattern_preview_pos = None
                            print("Pattern placement cancelled.")
                            button_clicked_in_editor = True # Consumed the click

                        # 3. Pattern Library Interaction
                        elif self.show_pattern_library and self.PATTERN_LIBRARY_AREA_RECT.collidepoint(mouse_pos):
                            button_clicked_in_editor = True
                            for lib_button in self.pattern_library_buttons:
                                if lib_button['rect'].collidepoint(mouse_pos):
                                    if lib_button['action'] == 'select_pattern':
                                        self.current_pattern_data = lib_button['pattern_data']
                                        self.placing_pattern_mode = True
                                        self.show_pattern_library = False
                                        self.pattern_preview_pos = None
                                        print(f"Pattern '{lib_button['label']}' selected. Click on grid to place.")
                                        break

                        # 4. Main UI Buttons
                        elif self.show_buttons:
                            for button in self.buttons:
                                if button['rect'].collidepoint(mouse_pos):
                                    button_clicked_in_editor = True
                                    action = button.get('action')

                                    if action == 'start':
                                        self.editing_mode = False
                                        self.show_countdown_prompt = False
                                        self.generation = 0
                                        self.stable_count = 0
                                        self.stable_generation = None
                                        previous_grids = [str(self.grid.tolist())]
                                        self.cell_ages[ (self.grid == 1) & (self.cell_ages == 0) ] = 1
                                    elif action == 'clear':
                                        self.grid.fill(0)
                                        self.cell_ages.fill(0)
                                        self.placing_pattern_mode = False # Cancel pattern placement on clear
                                        self.current_pattern_data = None
                                    elif action == 'save':
                                        if self.placing_pattern_mode:
                                            self.placing_pattern_mode = False
                                            self.current_pattern_data = None
                                            self.pattern_preview_pos = None
                                            print("Pattern placement cancelled before saving.")
                                        self.save_grid_to_file("custom_pattern.json")
                                    elif action == 'load':
                                        if self.placing_pattern_mode:
                                            self.placing_pattern_mode = False
                                            self.current_pattern_data = None
                                            self.pattern_preview_pos = None
                                            print("Pattern placement cancelled before loading new pattern.")
                                        self.load_grid_from_file("custom_pattern.json")
                                    elif action == 'load_default':
                                        default_pattern_name = "Acorn"
                                        acorn_data = None
                                        for category, patterns_in_category in PRESET_PATTERNS.items():
                                            if default_pattern_name in patterns_in_category:
                                                acorn_data = patterns_in_category[default_pattern_name]
                                                break

                                        if acorn_data:
                                            self.current_pattern_data = acorn_data.copy() # Use a copy
                                            self.placing_pattern_mode = True
                                            self.show_pattern_library = False
                                            self.pattern_preview_pos = None
                                            self.show_countdown_prompt = False
                                            print(f"Default pattern '{default_pattern_name}' loaded. Click on grid to place.")
                                        else:
                                            print(f"Error: Default pattern '{default_pattern_name}' not found in PRESET_PATTERNS.")
                                            self.grid.fill(0)
                                            self.cell_ages.fill(0)
                                        # Ensure editing_mode remains true, other states reset as needed
                                        self.editing_mode = True
                                    elif action == 'toggle_library':
                                        self.show_pattern_library = not self.show_pattern_library
                                        if self.show_pattern_library:
                                            self.placing_pattern_mode = False # Cancel placement when opening library
                                            self.current_pattern_data = None
                                    break # Exit button loop

                        if not button_clicked_in_editor and not self.placing_pattern_mode:
                            # Grid cell toggling, only if not placing a pattern and click wasn't on a button
                            # Ensure click is above buttons if they are shown
                            no_buttons_visible_or_click_above_buttons = not self.show_buttons or \
                                                                    (self.buttons and mouse_pos[1] < self.buttons[0]['rect'].top)
                            # And also ensure not clicking inside library area if it's open
                            click_outside_library = not self.show_pattern_library or \
                                                    (self.show_pattern_library and not self.PATTERN_LIBRARY_AREA_RECT.collidepoint(mouse_pos))

                            if no_buttons_visible_or_click_above_buttons and click_outside_library:
                                clicked_col = mouse_pos[0] // self.CELL_SIZE
                                clicked_row = mouse_pos[1] // self.CELL_SIZE
                                if 0 <= clicked_row < self.ROWS and 0 <= clicked_col < self.COLS:
                                    self.grid[clicked_row, clicked_col] = 1 - self.grid[clicked_row, clicked_col]
                                    if self.grid[clicked_row, clicked_col] == 1:
                                        self.cell_ages[clicked_row, clicked_col] = 1
                                    else:
                                        self.cell_ages[clicked_row, clicked_col] = 0

                if not running: # If QUIT event was processed from within editor event loop
                    break

                if self.show_buttons: # Draw buttons after event handling and other draws
                    self.draw_editor_ui()

                pygame.display.flip()
                self.clock.tick(self.FPS)

            else: # Simulation Mode
                # Event handling for simulation mode (mostly just QUIT)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        end_reason = "User quit simulation"
                        break # Break from event loop
                if not running: # If QUIT event was processed
                    break

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
        print("Simulation ended due to:", end_reason)
        time.sleep(5)
        pygame.quit()

if __name__ == "__main__":
    # Set up the dimensions of the window
    width = 2160
    height = 1920
    # Simulation pixel size
    pixel_size= 7
    frame_rate = 74.97

    #Provide the parameters for simulation
    game = GameOfLife(width, height, pixel_size, frame_rate)
    game.run_simulation()
