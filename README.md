# Conways Game of Life ScreenSaver

## Description

This program is an implementation of Conway's Game of Life, a classic cellular automaton devised by the British mathematician John Horton Conway in 1970. The simulation is built using the Pygame library to visualize the evolving patterns of live and dead cells on a grid.

### What is Conway's Game of Life?

Conway's Game of Life is a zero-player game, meaning that its evolution is determined by its initial state, requiring no further input. One interacts with the Game of Life by creating an initial configuration and observing how it evolves. It is Turing complete and can simulate a universal constructor or any other Turing machine.

The "game" takes place on a two-dimensional grid of square cells, each of which can be in one of two possible states: alive or dead. Every cell interacts with its eight neighbours (horizontally, vertically, or diagonally adjacent). At each step in time, the following transitions occur:

1.  **Underpopulation:** Any live cell with fewer than two live neighbours dies.
2.  **Survival:** Any live cell with two or three live neighbours lives on to the next generation.
3.  **Overpopulation:** Any live cell with more than three live neighbours dies.
4.  **Reproduction:** Any dead cell with exactly three live neighbours becomes a live cell.

These simple rules lead to a wide variety of complex and fascinating patterns.

## Simulation Details

### Initial State and Evolution

The simulation typically starts with a predefined pattern of live cells on the grid. In this implementation, the grid is initialized with a common small pattern known as the **R-pentomino**. This pattern is placed near the center of the grid.

The grid then evolves step by step, with each step representing a new generation. The state of each cell (alive or dead) in the next generation is determined by the rules of Conway's Game of Life, as described in the "What is Conway's Game of Life?" section above.

### Visual Representation

The Pygame window displays the grid of cells:
*   **Live cells** are typically drawn in one color (e.g., white or bright).
*   **Dead cells** are drawn in another color (e.g., black or dark), forming the background.
*   The display is updated after each generation to show the current state of the grid, allowing the user to observe the patterns as they change over time.

## Termination Conditions

The simulation can end in several ways:

*   **Periodic State Detection:** The simulation keeps track of a history of grid states. If the current grid state matches a state from the recent history, it indicates that the simulation has entered a periodic cycle (a repeating pattern). When such a cycle is detected, the simulation terminates to prevent an endless loop.

*   **Stable State Detection (Note: Currently Non-Functional):** The simulation intends to detect stable states (where the grid pattern no longer changes). Logic for this involves a variable `stable_count` (within the `GameOfLife` class's `run_simulation` method). This variable is initialized to 0 but is not correctly updated during the simulation loop when the grid state remains unchanged across generations. As a result, the condition to terminate the simulation due to stability (`stable_count >= 10`) is never met through the natural evolution of the grid, and this feature does not currently work as intended. The simulation will not automatically stop for all stable patterns based on this mechanism.

*   **User Intervention:** The user can manually terminate the simulation at any time by closing the Pygame window (e.g., by clicking the close button or using a system command like Alt+F4).

## Installation

0. Install python 3:
    ```bash
    winget install -e --id Python.Python.3.10
    ```

    
1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Run the program:
    ```bash
    python ./conways_game_of_life.py
    ```

## Build
1. Build executable:
    ```bash
    pyinstaller --onefile conways_game_of_life.py
    ```

## Install as Screensaver (Windows)
1. After building the executable, rename the executable file to have a `.scr` extension. For example, if your executable is named `conways_game_of_life.exe`, rename it to `conways_game_of_life.scr`.
2. Copy the renamed `.scr` file into the `System32` directory. This directory is typically located at `C:\Windows\System32`. You may need administrative privileges to copy files into this directory.

## Set Screensaver
1. Right-click on your desktop and select "Personalize" from the context menu.
2. In the Personalization window, click on "Lock screen" in the left sidebar.
3. Scroll down and click on "Screen saver settings" in the Related settings section.
4. In the Screen Saver Settings window, find and select your screensaver from the drop-down menu.
5. Click "Apply" and then "OK" to set your screensaver.


## Create your own patterns!

### 1. Define the pattern matrix:
Create a 2D matrix representing the pattern you want to add. Each element of the matrix should represent a cell in the pattern, where 1 indicates a live cell and 0 indicates a dead cell.

### 2. Choose a position to place the pattern:
Decide where you want to place the pattern on the grid. You can specify the row and column indices where the top-left corner of the pattern will be located.

### 3. Update the `initialize_grid` method:
Modify the `initialize_grid` method to include the new pattern. You can add multiple nested loops to iterate over the pattern matrix and place it onto the grid at the desired position.


## License
Shield: [![CC BY 4.0][cc-by-shield]][cc-by]

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg