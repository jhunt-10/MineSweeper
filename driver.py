"""Driver module

Drives all processes in view and model modules"""
from view import MineSweeperGUI, Tile
from model import Grid
import numpy as np
from PIL import Image, ImageTk

BOMB_PATHS = ["bombc3.png", "bomb2.png", "bomb1.png"]
GREEN1 = "#20B718"
GREEN2 = "#28E41E"
MENU_COLOR = "#134B00"
TAN1 = "#C3BA8C"
TAN2 = "#DFD59F"
HIGHLIGHT_GREEN = "#68FF60"
HIGHLIGHT_TAN = "#F4E9AF"


class MineSweeperDriver():
    """Driver class

    Instances are a driver that drives all processes for MineSweeper """

    def __init__(self):
        # initialize tkinter window by intitializing an instance of MineSweeperGUI
        self.window = MineSweeperGUI(self)
        # run the inifinite that shows the window until closed
        self.window.mainloop()

        self.model_grid = None
        self.visual_grid = None

    def play(self, dif_number):
        """Method that drives the play

        Initiliazes numerical and visual grids"""
        # initializes the numerical grid by creating instance of Grid class
        self.model_grid = Grid((dif_number+1)*15, 45*((dif_number+1)**2))

        # initializes the visual grid by creating
        self.visual_grid = np.ndarray(
            (dif_number, dif_number), dtype=np.dtype(object))

        self.window.bomb_image = ImageTk.PhotoImage(
            Image.open(BOMB_PATHS[dif_number]))

        square_sizes = [50, 27, 18]

        self.window.play_screen()

        for row in range(dif_number):
            for col in range(dif_number):
                self.visual_grid[row][col] = Tile(
                    self.window.grid_frame, square_sizes[dif_number], col, row, self)
                if (row+col) % 2 == 0:  # determine whcih background color to use for the square
                    color = GREEN1
                else:
                    color = GREEN2
                print("right here")

                # set the background color fo the square
                self.visual_grid[row][col].set_bg_color(color)
                print(self.visual_grid[row][col])
                self.visual_grid[row][col].grid(
                    row=row, column=col)    # grid the square on screen

        print("end of play")

    def square_click(self, x, y):
        pass

    def square_right_click(self, x, y):
        pass

    def square_highlight(self, x, y):
        states = self.model_grid.grid[y][x]
        if states.covered and not states.flag:
            self.visual_grid[y][x].set_bg_color(HIGHLIGHT_GREEN)

    def square_unhighlight(self, x, y):
        states = self.model_grid.grid[y][x]  # retrieve states for this square
        if states.covered and not states.flag:    # check to see if sqaure is covered and not flagged
            if (x+y) % 2 == 0:  # determine which background color to use for the square
                color = GREEN1
            else:
                color = GREEN2
                self.visual_grid[y][x].set_bg_color(color)


driver = MineSweeperDriver()
