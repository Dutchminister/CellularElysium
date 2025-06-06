# Program Description: Conway's Game of Life Screensaver

## Introduction

This program is an implementation of Conway's Game of Life, a classic cellular automaton devised by the British mathematician John Horton Conway in 1970. It is designed to function as a visually engaging screensaver, simulating the complex patterns that emerge from simple rules. The simulation is built using the Pygame library to create the visual display of live and dead cells on a grid.

## Understanding Conway's Game of Life

Conway's Game of Life is a "zero-player game," meaning its evolution is determined entirely by its initial state, without needing further user input once started. The game unfolds on a two-dimensional grid of cells, each of which can be either 'alive' or 'dead'. The state of each cell in the next generation is determined by the following rules, based on its eight immediate neighbors (horizontal, vertical, and diagonal):

1.  **Underpopulation:** A live cell with fewer than two live neighbours dies.
2.  **Survival:** A live cell with two or three live neighbours survives to the next generation.
3.  **Overpopulation:** A live cell with more than three live neighbours dies.
4.  **Reproduction:** A dead cell with exactly three live neighbours becomes a live cell.

These rules can lead to an astonishing variety of dynamic and intricate patterns.

## Simulation Details

### Initial State and Evolution

The simulation typically begins with a specific pattern of live cells. In this implementation, the grid is initialized with the "R-pentomino," a small, well-known pattern that exhibits complex behavior for many generations. This pattern is placed near the center of the grid.

From this starting point, the grid evolves generation by generation according to the rules of Conway's Game of Life.

### Visual Representation

The program uses Pygame to render the grid:
*   Live cells are typically displayed in a bright color (e.g., white).
*   Dead cells form the background, usually in a dark color (e.g., black).
The display is updated with each new generation, allowing observation of the evolving patterns.

## Running the Simulation

To run the simulation, ensure you have Python and the necessary dependencies (listed in `requirements.txt`, primarily Pygame) installed. Then, execute the main script from your terminal:

```bash
python ./conways_game_of_life.py
```

## Termination Conditions

The simulation can conclude in a few ways:

*   **Periodic State Detection:** The program monitors the history of grid states. If a grid configuration repeats one seen in the recent past, it signifies a periodic cycle, and the simulation terminates to avoid an infinite loop.
*   **User Intervention:** You can manually stop the simulation at any point by closing the Pygame window (e.g., clicking the 'X' button or using Alt+F4).
*   **Stable State Detection (Known Issue):** The program includes logic intended to detect stable states (where the grid no longer changes). This relies on a `stable_count` variable within the simulation code. However, this variable is initialized to 0 and is not correctly updated when the grid becomes stable. Consequently, the condition for the simulation to automatically terminate due to stability is not currently met as intended, and this feature does not reliably work.

## Advanced Usage

### Building an Executable

You can build a standalone executable from the script using PyInstaller:

```bash
pyinstaller --onefile conways_game_of_life.py
```
This creates an `.exe` file in the `dist` directory.

### Installing as a Screensaver (Windows)

1.  After building the executable (`conways_game_of_life.exe`), rename it to have a `.scr` extension (e.g., `conways_game_of_life.scr`).
2.  Copy this `.scr` file to your `C:\Windows\System32` directory (administrator privileges may be required).
3.  You can then select it in Windows Screen Saver Settings:
    *   Right-click your desktop, choose "Personalize."
    *   Go to "Lock screen," then "Screen saver settings."
    *   Select your new screensaver from the list.

### Creating Custom Starting Patterns

You can modify the simulation to start with your own patterns:

1.  **Define the Pattern:** Create a 2D matrix (list of lists in Python) where `1` represents a live cell and `0` a dead cell.
2.  **Choose Position:** Decide the row and column on the main grid where the top-left of your pattern will be placed.
3.  **Update Code:** Modify the `initialize_grid` method within the `conways_game_of_life.py` script to include your pattern at the chosen position. This typically involves iterating over your pattern matrix and assigning its values to the corresponding cells in the simulation's main grid.
