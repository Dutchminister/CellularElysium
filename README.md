# Conways Game of Life ScreenSaver

## Description
Give life to your screensaver! <br>
Tested on Windows 10

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